######################################################
# Names: Andrew Maurice, Cody Johnson, Lindsay Cason
# Date: 5/16/18
# Description: DOES SOME PRETTY COOL STUFF
#####################################################

from Tkinter import *

#Game superclass to manage the program's implementation
class Game(Frame):
        
    tiles = {}
    
    #define all instance varibables in constructor to be edited by the class functions
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.result = []

        
        
        #stores pieces in play
        self.blackPieces = []
        self.whitePieces = []
        #stores discard pieces
        #type:number discarded
        self.blackDiscard = {"King":0, "Queen":0, "Bishop":0, "Knight":0, "Rook":0, "Pawn":0}
        self.whiteDiscard = {"King":0, "Queen":0, "Bishop":0, "Knight":0, "Rook":0, "Pawn":0}
        #make instances of the Player class for each color to store in instance variables for the Game class
        self.blackPlayer = Player("black", 0)
        self.whitePlayer = Player("white", 0)
        #variable to hold value of if a piece is already highlighted (for process function to utilize) (maybe make it
        #hold the piece instance itself, where the process function can check if the variable is None to see if it is 
        #not holding a piece)
        self.pieceSelected = None
        #variable to hold the color matching the current player whose turn it is (traditionally starts with white)
        self.currentTurn = "white"

        #values for the clock times for both players
        self.p1Time = 900
        self.p2Time = 900

        
    ########################################
    # Accessors and Mutators for Game Class#
    ########################################
    @property
    def result (self):
        return self._result
    @result.setter
    def result (self, value):
        self._result = value

    @property
    def blackPieces (self):
        return self._blackPieces
    @blackPieces.setter
    def blackPieces (self, value):
        self._blackPieces = value

    @property
    def whitePieces (self):
        return self._whitePieces
    @whitePieces.setter
    def whitePieces (self, value):
        self._whitePieces = value
	
    @property
    def blackDiscard (self):
        return self._blackDiscard
    @blackDiscard.setter
    def blackDiscard (self, value):
        self._blackDiscard = value

    @property
    def whiteDiscard (self):
        return self._whiteDiscard
    @whiteDiscard.setter
    def whiteDiscard (self, value):
        self._whiteDiscard = value

    @property
    def pieceSelected (self):
        return self._pieceSelected
    @pieceSelected.setter
    def pieceSelected (self, value):
        self._pieceSelected = value

    @property
    def currentTurn (self):
        return self._currentTurn
    @currentTurn.setter
    def currentTurn (self, value):
        self._currentTurn = value

    @property
    def p1Time(self, value):
        return self._p1Timer
    @p1Time.setter
    def p1Time(self, value):
        self._p1Time = value
        
    @property
    def p2Time(self):
        return self._p2Time
    @p2Time.setter
    def p2Time(self, value):
        self._p2Time = value
        
    #sets up the majority of the GUI
    def setupGUI(self):
        # creates buttons for each of the chess board tiles, initialized with the image of the piece located
        # on each tile by default (or the blank image for the other tiles)
        # tiles are numbered with two digit codes, where the first number represents the row
        # and the second digit represents the column. The coordinate is stored as the key in the tiles dictionary
        #with the buttons as the values
        
        #outer for loop iterates through values for the row (1-8)
        for r in range (1,9):
            #inner for loop iterates through column values (1-8) (column zero utilized for labels)
            for c in range (1,9):
                #set coordinate with the ten's place digit as row and the one's for the column
                coord = (r*10) + c
                
                #get image to set for the tile
                #row 2 is all black pawns
                if (r == 2):
                    img = blackPawn
                #coordinates 11 and 18 are black rooks
                elif (coord==11 or coord==18):
                    img = blackRook
                #coordinates 12 and 17 are black knights
                elif (coord==12 or coord==17):
                    img = blackKnight
                #coordinates 13 and 16 are black bishops
                elif (coord==13 or coord==16):
                    img = blackBishop
                #coordinate 14 is black king
                elif (coord==14):
                    img = blackKing
                #coordinate 15 is black queen
                elif (coord==15):
                    img = blackQueen
                #row 7 is all white pawns
                elif (r == 7):
                    img = whitePawn
                #coordinates 81 and 88 are white rooks
                elif (coord==81 or coord==88):
                    img = whiteRook
                #coordinates 82 and 87 are white knights
                elif (coord==82 or coord==87):
                    img = whiteKnight
                #coordinates 83 and 86 are white bishops
                elif (coord==83 or coord==86):
                    img = whiteBishop
                #coordinate 84 is white queen
                elif (coord==84):
                    img = whiteQueen
                #coordinate 85 is white king
                elif (coord==85):
                    img = whiteKing
                #all others are blank 
                else:
                    img = blank
                
                #add a new instance of the Button class to the dictionary with the coordinate as the key
                #the "coord=coord" line in the lambda stores the current iteration of the coord with the instance of the Button class so each individual button will
                #use the proper value it was meant to have instead of the last value of coord defined when clicked
                self.tiles[coord] = Button(self.master, image = img, bg = "grey", bd = 1, command = lambda coord=coord: self.process(self.tiles[coord]))
                #this may be typed wrong, but meant to place the newly made button on the GUI grid
                self.tiles[coord].grid(row = r, column = c)
        
        # top player headers
        p1Title = Label(self.master, text = " Player One ", font = ("TkDefaultFont", 12))
        p1Title.grid(row = 9, column = 1, columnspan = 3)
        p2Title = Label(self.master, text = " Player Two ", font = ("TkDefaultFont", 12))
        p2Title.grid(row = 0, column = 1, columnspan = 3)

        #"Your Turn" text (default to only show for white)
        #set as class variables to be editted in displayTurn function
        self.p1Turn = Label(self.master, text = "Your Turn", font = ("TkDefaultFont", 12))
        self.p1Turn.grid(row = 9, column = 4, columnspan = 2)
        self.p2Turn = Label(self.master, text = "", font = ("TkDefaultFont", 12))
        self.p2Turn.grid(row = 0, column = 4, columnspan = 2)

        # timer text (set as class variables to be editted in countdown function
        self.timer1 = Label(self.master, text = "Time:   {}:{}".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)), font = ("TkDefaultFont", 12))
        self.timer1.grid(row = 9, column = 6, columnspan = 3, sticky = E)

        self.timer2 = Label(self.master, text = "Time:   {}:{}".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)), font = ("TkDefaultFont", 12))
        self.timer2.grid(row = 0, column = 6, columnspan = 3, sticky = E)

        
        # instruction side panel
        instructions = Label(self.master, text = "Instructions", font = ("TkDefaultFont", 12), width = 22)
        instructions.grid(row = 0, rowspan = 8, column = 0)
        
        # highlight checkbutton
        highlight = Checkbutton(self.master, text = "Highlight?", font = ("TkDefaultFont", 12))
        highlight.grid(row = 9, column = 0)
        
        # discard side panel
        discardTitle = Label(self.master, text = "Discard", font = ("TkDefaultFont", 12), width = 22)
        discardTitle.grid(row = 1, column = 10, columnspan = 3, sticky = N)
        
        dWhiteLabel = Label(self.master, text = "White", font = ("TkDefaultFont", 12))
        dWhiteLabel.grid(row = 2, column = 10)

        dBlackLabel = Label(self.master, text = "Black", font = ("TkDefaultFont", 12))
        dBlackLabel.grid(row = 2, column = 12)

        # use the list dictionaries of discard white pieces in game class to display the number of discarded pieces
        # next to the image of the type

        # i is used to keep up with the row
        i = 3
        for key in self.whiteDiscard.keys():
            # creates a label using dictionary
            key = Label(self.master, text = "x{}".format(self.whiteDiscard[key], font = ("TkDefaultFont",12)))
            key.grid(row = i, column = 10)
            # increment i
            i += 1

        # add discard images
        # can probably be made more efficient
        img = discardKing
        dKing = Button(self.master, bg = "grey", image = img)
        dKing.grid(row = 3, column = 11)
        
        img = discardQueen
        dQueen = Button(self.master, bg = "grey", image = img)
        dQueen.grid(row = 4, column = 11)

        img = discardBishop
        dBishop = Button(self.master, bg = "grey", image = img)
        dBishop.grid(row = 5, column = 11)

        img = discardKnight
        dKnight = Button(self.master, bg = "grey", image = img)
        dKnight.grid(row = 6, column = 11)

        img = discardRook
        dRook = Button(self.master, bg = "grey", image = img)
        dRook.grid(row = 7, column = 11)

        img = discardPawn
        dPawn = Button(self.master, bg = "grey", image = img)
        dPawn.grid(row = 8, column = 11)

        
        # use the dictionary of discard black pieces in the game class to display the number of discards next to the
        # type
        # i is used to keep up with the row
        i = 3
        for key in self.blackDiscard.keys():
            # creates label using dictionary
            key = Label(self.master, text = "x{}".format(self.blackDiscard[key], font = ("TkDefaultFont",12)))
            key.grid(row = i, column = 12)
            # increment i
            i += 1
        
    #instantiate all pieces (black and white) and the two players    
    def setupGame(self):
        #hold all active black pieces in the blackPieces array (as they are defeated, they can be taken out of the array)
        #use for loops to make pawns, iterate through column values (1-8)
        for c in range (1,9):
            #set coordinate with the ten's place digit as row and the one's for the column (row is two, so the
            #cooridnate position is just the column value plus 20
            self.blackPieces.append(Pawn(blackPawn, "black", (20 + c)))
        #all non-pawn black pieces are in row 1, so the position coordinate is just the column value plus 10
        #make two rooks
        for p in [1, 8]:
            self.blackPieces.append(Rook(blackRook, "black", (10+p)))
        #make two knights
        for p in [2, 7]:
            self.blackPieces.append(Knight(blackKnight, "black", (10+p)))
        #make two bishops
        for p in [3, 6]:
            self.blackPieces.append(Bishop(blackBishop, "black", (10+p)))
        #make the queen and king
        self.blackPieces.append(Queen(blackQueen, "black", 15))
        self.blackPieces.append(King(blackKing, "black", 14))
        
        #hold all active white pieces in the whitePieces array (as they are defeated, they can be taken out of the array)
        #use for loops to make pawns, iterate through column values (1-8)
        for c in range (1,9):
            #set coordinate with the ten's place digit as row and the one's for the column (row is six, so the
            #cooridnate position is just the column value plus 70
            self.whitePieces.append(Pawn(whitePawn, "white", (70 + c)))
        #all non-pawn white pieces are in row, so the position coordinate is just the column value plus 80
        #make two rooks
        for p in [1, 8]:
            self.whitePieces.append(Rook(whiteRook, "white", (80+p)))
        #make two knights
        for p in [2, 7]:
            self.whitePieces.append(Knight(whiteKnight, "white", (80+p)))
        #make two bishops
        for p in [3, 6]:
            self.whitePieces.append(Bishop(whiteBishop, "white", (80+p)))
        #make the queen and king
        self.whitePieces.append(Queen(whiteQueen, "white", 84))
        self.whitePieces.append(King(whiteKing, "white", 85))
        
    def play(self):
        #would return a result of victor in the end
        pass
    
    #function to allow Buttons to be processed after being clicked (NOTE: this function processes a button being
    #pressed, so it takes a button as the input, not the piece, though the piece and button have the same coordinate
    #so a function can be made to return the piece based on the button)
    def process(self, button):
        #check if a piece has already been selected
        if (self.pieceSelected == None):
            #set the pieceSelected variable to the piece at the same position as the button
            self.pieceSelected = self.getPiece(button)
            
            #if no piece was selected, skip the rest of the code
            if (self.pieceSelected != None):

                #check that the color of the piece selected matches the current player
                if(self.currentTurn == self.pieceSelected.color):
                
                    #get the list of possible moves the piece can perform
                    self.pieceSelectedMoves = self.pieceSelected.possibleMoves()

                    #highlight the button holding the selected piece and possible moves
                    self.highlight(button)

                #piece selected is not current player's piece, deselect pieces
                else:
                    self.pieceSelected = None
            
        else:
            #a piece to move has been selected already, so determine if the second input is valid place to move (if not, keep possible
            #moves highlighted to allow player to select a different piece. However, if the same piece is selected again, this would
            #mean the player wishes to deselect the first piece so highlights should be removed; similarly, if the player selects
            #another piece that is also theirs, the first piece can be deselected and the second can be used instead as the "initial
            #selection")
            
            #check to see if the second button selected corresponds to a valid place for the initial piece selected to move
            #local variable to temporarily hold the piece located on the second space (if there is one)
            secondPiece = self.getPiece(button)

            #check to see if the second button is blank
            if (secondPiece == None):
                #if no piece, get the coordinate of the tile to make sure it fits in the range of possible moves
                blankPosition = self.buttonPosition(button)

                pieceValid = False
                for i in range(len(self.pieceSelectedMoves)):
                    if(blankPosition == self.pieceSelectedMoves[i]):
                        pieceValid = True
                        break

                if (pieceValid):
                    #remove highlight from the button holding the selected piece and possible moves
                    self.removeHighlight(self.tiles[self.pieceSelected.position])
                    
                    #call the change position function using the pieceSelected as the initial selection
                    #and the button of the blank tile as the second
                    self.changePosition(button)
		
		    #if piece is pawn, check to see if it reached the end of the board and should be swapped
                    if((self.pieceSelected.image == whitePawn and self.pieceSelected.row == 1) or\
                       (self.pieceSelected.image == blackPawn and self.pieceSelected.row == 8)):
                        pawnSwap()
                    
                    #set the pieceSelected to none
                    self.pieceSelected = None
                    #change the turn to the other player
                    self.changeTurn()

            #if the same piece was clicked a second time, deselect it and unhighlight everything
            elif (secondPiece == self.pieceSelected):
                    #remove highlight from the button holding the selected piece and possible moves
                    self.removeHighlight(self.tiles[self.pieceSelected.position])

                    #set the piece selected to None
                    self.pieceSelected = None
                
            #there is a piece on the second tile selected, so check to see if the piece selected
            #is in the valid range of pieceSelectedMoves
            elif (secondPiece.position in self.pieceSelectedMoves):
                #remove highlight from the button holding the selected piece and possible moves
                self.removeHighlight(self.tiles[self.pieceSelected.position])
				
                #change the position of the moving piece to that of the one being overtaken
                self.changePosition(button)

                #call the overtake function to remove the second piece from play and place it on
                #the column where it belongs
                self.overtake(secondPiece)

                #if piece is pawn, check to see if it reached the end of the board and should be swapped
                if((self.pieceSelected.image == whitePawn and self.pieceSelected.row == 1) or\
                    (self.pieceSelected.image == blackPawn and self.pieceSelected.row == 8)):
                    pawnSwap()

                #set the piece selected to None
                self.pieceSelected = None
                #change the turn to the other player
                self.changeTurn()

            #check if the second piece selected is the same color as the first
            elif (secondPiece.color == self.pieceSelected.color):
                #deselect the first piece and remove all its highlights, then select the new
                #piece and display its highlights

                #remove highlight from the button holding the selected piece and possible moves
                self.removeHighlight(self.tiles[self.pieceSelected.position])

                #set the initial selected piece to the new choice
                self.pieceSelected = secondPiece
                
                #get the list of possible moves the piece can perform
                self.pieceSelectedMoves = self.pieceSelected.possibleMoves()
				
                #remove highlight from the button holding the selected piece and possible moves
                self.highlight(self.tiles[self.pieceSelected.position])			
				
    ###############special cases
    #if a black pawn gets to row 8 or a white pawn gets to row 1 as a result of moving,
    #then process changing the piece
    def pawnSwap(self):
            pass


    ###############end of special cases

    ########highlight buttons as needed with these functions
    #highlight initially selected piece green, and all possible moves
    #yellow (blank) or red (occupied)
    def highlight(self, button):
        #highligh initial selection
        button.config(bg = "green")

        #highlight all possible moves
        for i in self.pieceSelectedMoves:
            #if no piece on the specified tile, highlight yellow
            if (self.getPiece(self.tiles[i]) == None):
                self.tiles[i].config(bg = "yellow")

            #else highlight red (overtake color)
            else:
                self.tiles[i].config(bg = "red")

    #remove all highlights (located on the initially selected button
    #and all possible move buttons) (grey is unhighlighted color)
    def removeHighlight(self, button):
        #unhighlight initial selection
        button.config(bg = "grey")

        #unhighlight all possible moves
        for i in self.pieceSelectedMoves:
            self.tiles[i].config(bg = "grey")
        
                
    ########end of highlight functions

    #change the current turn to the opposite player
    def changeTurn(self):
        if (self.currentTurn == "white"):
            self.currentTurn = "black"
        else:
            self.currentTurn = "white"
    
    #function to return the coordinate of the inputted button as a row-column pair
    def buttonPosition(self, button):
        row = int(button.grid_info()["row"])
        column = int(button.grid_info()["column"])
        return (row*10 + column)
            
    #function to return the piece at the same coordinate as the inputted button
    def getPiece(self, button):
        #get the position coordinate of the button
        bPosition = self.buttonPosition(button)

        #loop through all black pieces to see if one is at the same
        #position as the button
        for i in range (len(self.blackPieces)):
            if (self.blackPieces[i].position == bPosition):
                #return the piece at the button's position
                return self.blackPieces[i]

        #loop through all white pieces to see if one is at the same
        #position as the button
        for i in range (len(self.whitePieces)):
            if (self.whitePieces[i].position == bPosition):
                #return the piece at the button's position
                return self.whitePieces[i]
            
        #no piece was found, so return None
        return None
        
    #change position of the piece to the newly chosen coordinate (initial selection is the pieceSelected instance of the piece
    #class, while the secondary selection is the button of the second spot selected)
    def changePosition(self, secondButton):
        #get the piece (if any)
        secondPiece = self.getPiece(secondButton)

        #blank tile, so simply move the intial selection to the secondary location, updating the pictures for both
        if (secondPiece == None):
            #set the button at the coordinate with the piece to have a blank image
            self.tiles[self.pieceSelected.position].configure(image = blank)

            #get the position of the blank button
            button2Position = self.buttonPosition(secondButton)
            
            #set the button with the blank to have the image of the piece
            self.tiles[button2Position].configure(image = self.pieceSelected.image)
            #update the piece instance to have the correct position (including row and column)
            self.pieceSelected.updatePiecePosition(button2Position)
			
	    #check for special case of pawn's first move (if it was the first move for a pawn
            if (self.pieceSelected.image == blackPawn or self.pieceSelected.image == whitePawn):
                if (self.pieceSelected.firstMove == True):
                    self.pieceSelected.firstMove = False
    
    #function to overtake piece (the changePosition function could have logic to check if a piece is already inhabiting
    #the tile and call this function for the piece being overtaken to remove it)
    def overtake(self, initialSelection, secondarySelection):
        pass

    # function that counts down and updates player timers on a loop
    def countdown(self):
        # counts down selected player's timer
        if (self.currentTurn == "white"):
            self.p1Time -= 1
            self.timer1.config(text = "Time:   {}:{}".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)))
             
        else:
            self.p2Time -= 1
            self.timer2.config(text = "Time:   {}:{}".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)))
            
        # loops the function every second
        self.after(1000, self.countdown)

    #function to display whose turn it is currently
    def displayTurn(self):
        if (self.currentTurn == "white"):
            self.p1Turn.config(bg = "red", text = "Your Turn")
            self.p2Turn.config(bg = "SystemButtonFace", text = "")
            
        else:
            self.p1Turn.config(bg = "SystemButtonFace", text = "")
            self.p2Turn.config(bg = "red", text = "Your Turn")

        # loops the function every millisecond
        self.after(1, self.displayTurn)

#Player class: inherits from Game, to be instantiated twice to make the two players
class Player(Game):
        def __init__(self, color, moveNumber):
                #string variable to hold which color a player corresponds to (only black or white)
                self.color = color
                #integer to hold what current move the player is on
                self.moveNumber = moveNumber
                
        #accessors and mutators for Player class variables
        @property
        def color(self):
                return self._color
        @color.setter
        def color(self, value):
                self._color = value
                
        @property
        def moveNumber(self):
                return self._moveNumber
        @moveNumber.setter
        def moveNumber(self, value):
                self._moveNumber = value


#Piece class: biggest class in center of program, (need to implement "hasa" relationship under Tile and Player classes
#possibly byincluding an instance of the piece class in the Tile and Player classes?)
class Piece(Game):
    #instance variables for piece class
    def __init__(self, image, color, position):
        #all pieces will be in play by default until overtaken
        self.inPlay = True
        #have image stored with the instance for easy correlation between the piece and the button holding the image
        self.image = image
        #define what color the piece is
        self.color = color
        #call function to set the full position coordinate, along with the individual row and column values for easy access to each seperately
        self.position = position
        #set the values of row and column based on the position
        self.row = self.position / 10
        self.column = self.position % 10

	#accessors and mutators for position, row, and column
    @property
    def position(self):
        return self._position

    #set the position of the piece to the full coordiate
    @position.setter
    def position(self, value):
        self._position = value

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    #function to easily change the row and column at the same time as a position change
    def updatePiecePosition(self, position):
        self.position = position
        self.row = position / 10
        self.column = position %10
    
    # function to determine if tile is in proper range
    def isValidTile(self, row, column, color):
        #uses the passed in values for row and column to see if the values match to a valid location on the board
        #rows are numbered 1-8 and columns 1-8
        if ((row in range(1,9)) and (column in range(1,9))):
            #use the getPiece function from game to get either the instance
            #of the piece at the tile (if any)
            piece = Game.getPiece(game, Game.tiles[row*10+column])

            #if no piece, tile is valid, return True
            if(piece == None):
                return True

            #if the piece is not the same color as the piece trying to be
            #moved, the tile is valid so return True
            elif(piece.color != color):
                return True

            #tile in range of board but piece of same color, so can't move there
            #return False
            else:
                return False

        #coordinate out of range of board, so invalid
        else:
            return False

	#possible moves for the bishop (located here because Queen and Bishop classes both utilize this function)
    def bishopPossibleMoves(self):
        moves = []

        #move NE
        i = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row + i, self.column - i, self.color)):
            #append the next move to the moves list
            moves.append((self.row+i)*10 + self.column-i)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row+i)*10+(self.column-i)]) != None):
                break
            
            #increment the counter for i
            i = i + 1

        #move SE
        i = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row + i, self.column + i, self.color)):
            #append the next move to the moves list
            moves.append((self.row+i)*10 + self.column+i)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row+i)*10+(self.column+i)]) != None):
                break
            
            #increment the counter for i
            i = i + 1
        

        #move SW
        i = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row - i, self.column + i, self.color)):
            #append the next move to the moves list
            moves.append((self.row-i)*10 + self.column+i)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row-i)*10+(self.column+i)]) != None):
                break
            
            #increment the counter for i
            i = i + 1

        #move NW
        i = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row - i, self.column - i, self.color)):
            #append the next move to the moves list
            moves.append((self.row-i)*10 + self.column-i)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row-i)*10+(self.column-i)]) != None):
                break
            
            #increment the counter for i
            i = i + 1
        
        return moves
	
	#possible moves for the rook (located here because Queen and Rook classes both utilize this function)
    def rookPossibleMoves(self):
        moves = []
        
        #move up(up screen is negative y direction)
        r = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row - r, self.column, self.color)):
            #append the next move to the moves list
            moves.append((self.row-r)*10 + self.column)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row-r)*10+(self.column)]) != None):
                break

            #increment counter for the row
            r = r + 1

        #move down screen, positive y
        r = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row + r, self.column, self.color)):
            #append the next move to the moves list
            moves.append((self.row+r)*10 + self.column)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row+r)*10+(self.column)]) != None):
                break

            #increment counter for the row
            r = r + 1

        #move left
        c = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row, self.column-c, self.color)):
            #append the next move to the moves list
            moves.append((self.row)*10 + self.column-c)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row)*10+(self.column-c)]) != None):
                break

            #increment counter for the column
            c = c + 1
        

        #move right
        c = 1
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row, self.column+c, self.color)):
            #append the next move to the moves list
            moves.append((self.row)*10 + self.column+c)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row)*10+(self.column+c)]) != None):
                break

            #increment counter for the column
            c = c + 1

        return moves
    
    #####instead of having variables for initial and secondary select here, we may need to implement a system to work in conjunction
    #####with the GUI, where the play function in the Game class can take the tile clicked and call the possibleMoves function of 
    #####the appropriate piece
#All the individual types of pieces have classes defined below (concrete functions)
#King class
class King(Piece):
    #utilize the Piece class constructor, in addition to the contested variable (False by default)
    def __init__(self, image, color, position):
        #King only, if in check, the move options will be limited for the Player's next turn
        self.contested = False
        Piece.__init__(self, image, color, position)

        @property
        def contested (self):
            return self._contested
        @contested.setter
        def contested(self, value):
            self._contested = value
    
    #function to determine the possible moves a piece can make (takes contested state into account as well, but can be accessed
    #using self.contested when needed)
    def possibleMoves(self):
        ##########################needs to be updated to take into account limiting the moves based on if the player
        ##########################is contested or would become contested from a certain move (maybe have a condition
        ##########################in the isValidTile, or have a seperate isValidTile for the King specifically 
        ##########################because the logic may get to be complex
        moves = []
        #double for loop to determine list of moves
        #outer for loop to iterate through row values (-1, 0, 1), and same thing for columns in inner loop
        for r in range(-1,2):
            for c in range(-1,2):
                #only invalid combination is 0, 0 for the changes (wouldn't move) (if either r or c
				#have a non-zero value (not necessarily both) it can be processed)
                if (r!=0 or c!=0):
                    if (self.isValidTile(self.row+r, self.column+c, self.color)):
                        moves.append((self.row + r)*10 + (self.column + c))
                        
        #return the list of possible moves
        return moves
    
    
#Queen class
class Queen(Piece):
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #queen moves = rook moves + bishop moves
        return self.rookPossibleMoves() + self.bishopPossibleMoves()
    
    
#Rook class
class Rook(Piece):
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #call the function for rookPossibleMoves in the Pieces class and return the result
        return self.rookPossibleMoves()
    
    
#Bishop class
class Bishop(Piece):
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #call the function for bishopPossibleMoves in the Pieces class and return the result
        return self.bishopPossibleMoves()
      
        
#Knight class
class Knight(Piece):
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        moves = []

        #use double for loop to iterate through all possible values for moves
        #outer loop for all possible ways the knight can move between rows
        for r in [-2,-1,1,2]:
            #inner loop for all possible ways the knight can move between columns
            for c in [-2,-1,1,2]:
                #the knight must move a combination of 2 and 1, so if the values of r and c are the same, 
                #then the move would be invalid and is thus skipped
                if(abs(r) != abs(c)):
                    #check that the move would correlate to a valid tile
                    if (self.isValidTile(self.row + r, self.column + c, self.color)):
                        moves.append((self.row + r)*10 + (self.column + c))
                            
        #return the list of all valid moves
        return moves
    
    
#Pawn class
class Pawn(Piece):
    #utilize the Piece class constructor, in addition to the firstMove variable (True by default)
    def __init__(self, image, color, position):
        self.firstMove = True
        Piece.__init__(self, image, color, position)

    # Accessors and Mutators for Pawn Class
    @property
    def firstMove (self):
        return self._firstMove
    @firstMove.setter
    def firstMove (self, value):
        self._firstMove = value

    #function to determine the possible moves a piece can make (takes firstMove state into account as well)
    def possibleMoves(self):
        #hold list of possible coordinates
        moves = []
        
        if self.color == 'white':
            #GUI coordinates work from top-left corner, so moving bottom to top decreases Y-value
            advance = -1
        else:
            advance = 1
          
        #attack left
        if (self.isValidTile((self.row + advance), (self.column - 1), self.color)):
            #tile is valid, but make sure it is not blank
            if (Game.getPiece(game, Game.tiles[(self.row+advance)*10+(self.column-1)]) != None):
                moves.append((self.row + advance)*10 + (self.column - 1))

        #attack right
        if (self.isValidTile((self.row + advance), (self.column + 1), self.color)):
            #tile is valid, but make sure it is not blank
            if (Game.getPiece(game, Game.tiles[(self.row+advance)*10+(self.column+1)]) != None):
                moves.append((self.row + advance)*10 + (self.column + 1))

        #move straight
        if (self.isValidTile((self.row + advance), self.column, self.color)):
            #tile is valid, but make sure it is blank
            if (Game.getPiece(game, Game.tiles[(self.row+advance)*10+(self.column)]) == None):
                moves.append((self.row + advance)*10 + self.column)
            #if it is the pawn's first move and the tile is available, it also has the option to move forward two tiles
            if(self.firstMove and self.isValidTile((self.row + advance*2), self.column, self.color)):
                #tile is valid, but make sure it is blank
                if (Game.getPiece(game, Game.tiles[(self.row+advance*2)*10+(self.column)]) == None):
                    moves.append((self.row + advance*2)*10 + self.column)
            
        #return the list of valid moves
        return moves
      
###################################################################
#Main part of program
###################################################################
window = Tk()

#########possible move into a class?
# initialize all images for later usage
blank = PhotoImage(file = "images/blank.gif")
whiteKing = PhotoImage(file = "images/whiteKing.gif")
whiteQueen = PhotoImage(file = "images/whiteQueen.gif")
whiteBishop = PhotoImage(file = "images/whiteBishop.gif")
whiteKnight = PhotoImage(file = "images/whiteKnight.gif")
whiteRook = PhotoImage(file = "images/whiteRook.gif")
whitePawn = PhotoImage(file = "images/whitePawn.gif")
blackKing = PhotoImage(file = "images/blackKing.gif")
blackQueen = PhotoImage(file = "images/blackQueen.gif")
blackBishop = PhotoImage(file = "images/blackBishop.gif")
blackKnight = PhotoImage(file = "images/blackKnight.gif")
blackRook = PhotoImage(file = "images/blackRook.gif")
blackPawn = PhotoImage(file = "images/blackPawn.gif")
discardKing = PhotoImage(file = "images/discardKing.gif")
discardQueen = PhotoImage(file = "images/discardQueen.gif")
discardBishop = PhotoImage(file = "images/discardBishop.gif")
discardKnight = PhotoImage(file = "images/discardKnight.gif")
discardRook = PhotoImage(file = "images/discardRook.gif")
discardPawn = PhotoImage(file = "images/discardPawn.gif")

window.title("Chess Reloaded")
game = Game(window)
game.setupGUI()
game.setupGame()
game.countdown()
game.displayTurn()
window.mainloop()
