######################################################
# Names: Andrew Maurice, Cody Johnson, Lindsay Cason
# Date: 5/16/18
# Description: PiMaster Chess: A fully operational chess game for two players designed around making a fun experience for new
#                   chess players with the ability to highlight all possible moves and have unlimited play time, as well as
#                   having an option to disable these features for the more experienced players. The game also features a
#                   information tab to show what is happening, such as whose turn it is. The game can be exited at any time
#                   using the exit buttons on either menu or the main game.
######################################################
from Tkinter import *

DEBUG = True
MUSIC = True
GPIO = False

#only import the pygame library if music is desired (meant for turning it off
#during testing, or if pygame not compatable with user's device)
if (MUSIC):
    import pygame

if (GPIO):
    import RPi.GPIO as GPIO

#class for the main menu displayed before starting the game
class Menu(Frame):
    def __init__(self, master):
        self.master = master
        self.timerType = IntVar()
        self.timerType.set(1)
        self.timerCheckboxType = IntVar()
        self.timerCheckboxType.set(0)
        self.timerChosen = None

    @property
    def timerType (self):
        return self._timerType
    @timerType.setter
    def timerType (self, value):
        self._timerType = value

    @property
    def timers (self):
        return self._timers
    @timers.setter
    def timers (self, value):
        self._timers = value

    def setupGUI(self):
        header = Label(self.master, text = "\nWelcome to Pimaster Chess!\n", font = ("TkDefaultFont", 20), height = 2)
        header.grid(row = 0, column = 0, padx = (40, 20))
        info = Label(self.master, text = "Pimaster Chess is a simple python chess program created by three people: Andrew Maurice, Cody Johnson, and \
Lindsay Cason. To the right are a couple of options. The button labeled \"Play\" will start the game. The checkbox labeled \"Timer?\" will decide whether \
or not you will have a timer while playing, and if so, which timer you wish to have. The button labeled \"Quit\" will exit the program. Thank you for playing!", \
                     font = ("TkDefaultFont", 12), wraplength = 380, height = 10)
        info.grid(row = 1, rowspan = 4, column = 0)
        playButton = Button(self.master, text = "Play", font = ("TkDefaultFont", 16), width = 10, height = 1, command = lambda : self.startGame())
        playButton.grid(row = 0, column = 1, padx = 20)
        self.timer = Checkbutton(self.master, text = "Timer?", font = ("TkDefaultFont", 16), width = 10, height = 1, variable = self.timerCheckboxType, command = lambda : self.switchTimers())
        self.timer.grid(row = 1, column = 1)
        timerNormal = Radiobutton(self.master, text = "Normal", font = ("TkDefaultFont", 12), state = DISABLED, variable = self.timerType, value = 1)
        timerNormal.grid(row = 2, column = 1, sticky = W, padx = (50, 0))
        timerBlitz = Radiobutton(self.master, text = "Blitz", font = ("TkDefaultFont", 12), state = DISABLED, variable = self.timerType, value = 2)
        timerBlitz.grid(row = 3, column = 1, sticky = W, padx = (50, 0))
        self.timers = [timerNormal, timerBlitz]
        quitButton = Button(self.master, text = "Quit", font = ("TkDefaultFont", 16), width = 10, height = 1, command = lambda : self.quitProgram())
        quitButton.grid(row = 4, column = 1, padx = 20, pady = (0, 10))
        
    def switchTimers(self):
        newState = DISABLED
        if (self.timers[0].cget("state") == DISABLED):
            newState = NORMAL
        for t in self.timers:
            t.config(state = newState)
        
        if DEBUG:
            print self.timerCheckboxType.get()
        
    def quitProgram(self):
        if (MUSIC):
            pygame.mixer.music.stop()
        self.master.destroy()
        exit()

    #once the button to start the game is clicked, call the function in the main to store the value of the timer selected
    #by the player before destroying the window to make a new one
    def startGame(self):

        #store global variables with the values of the checkbox and radio buttons so after this window is deleted, the
        #second window will be able to use these for setting up the timer
        global timerCheck, timerType
        timerCheck = self.timerCheckboxType.get()
        timerType = self.timerType.get()
        
        self.master.destroy()

#Game superclass to manage the program's implementation
class Game(Frame):
        
    tiles = {}
    
    #define all instance varibables in constructor to be edited by the class functions
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        
        #variable utilized for displaying highlight (or not)
        self.highlightActive = True
        
        #stores pieces in play
        self.blackPieces = []
        self.whitePieces = []
        
        #stores discard pieces
        #type:number discarded
        self.discardType = ["Queen", "Bishop", "Knight", "Rook", "Pawn"]
        self.whiteDiscard = [0, 0, 0, 0, 0]
        self.blackDiscard = [0, 0, 0, 0, 0]
        #dictionaries to hold labels for discard panel
        self.blackDiscardLabels = {}
        self.whiteDiscardLabels = {}
        
        #variable to hold value of if a piece is already highlighted (for process function to utilize) (maybe make it
        #hold the piece instance itself, where the process function can check if the variable is None to see if it is 
        #not holding a piece)
        self.pieceSelected = None
        #variable to hold the color matching the current player whose turn it is (traditionally starts with white)
        self.currentTurn = "white"
        #boolean to hold if the current player's king is contested
        self.currentPlayerContested = False

        # variable to keep up with pawnSwap
        self.pawnSwap = False

        #values for the clock times for both players (default to normal 15 min time)
        self.p1Time = 900
        self.p2Time = 900

        
    ########################################
    # Accessors and Mutators for Game Class#
    ########################################
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
    def discardType (self):
        return self._discardType
    @discardType.setter
    def discardType (self, value):
        self._discardType = value
    
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
    def whiteDiscardLabels(self):
        return self._whiteDiscardLabels
    @whiteDiscardLabels.setter
    def whiteDiscardLabels(self, value):
        self._whiteDiscardLabels = value

    @property
    def blackDiscardLabels(self):
        return self._blackDiscardLabels
    @blackDiscardLabels.setter
    def blackDiscardLabels(self, value):
        self._blackDiscardLabels = value

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
    def pawnSwap (self):
        return self._pawnSwap
    @pawnSwap.setter
    def pawnSwap (self, value):
        self._pawnSwap = value

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
                #coordinate 14 is black queen
                elif (coord==14):
                    img = blackQueen
                #coordinate 15 is black king
                elif (coord==15):
                    img = blackKing
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
        p1Title = Label(self.master, text = "Player One", font = ("TkDefaultFont", 12))
        p1Title.grid(row = 9, column = 1, columnspan = 3, sticky = W)
        p2Title = Label(self.master, text = "Player Two", font = ("TkDefaultFont", 12))
        p2Title.grid(row = 0, column = 1, columnspan = 3, sticky = W)

        #"Your Turn" text (default to only show for white)
        #set as class variables to be editted in displayTurn function
        self.p1Turn = Label(self.master, text = "Your Turn", font = ("TkDefaultFont", 12))
        self.p1Turn.grid(row = 9, column = 4, columnspan = 2)
        self.p2Turn = Label(self.master, text = "", font = ("TkDefaultFont", 12))
        self.p2Turn.grid(row = 0, column = 4, columnspan = 2)

        # timer text (set as class variables to be editted in countdown function)
        self.timer1 = Label(self.master, text = "Time:   {}:{}".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)), font = ("TkDefaultFont", 12))
        self.timer1.grid(row = 9, column = 6, columnspan = 3, sticky = E)

        self.timer2 = Label(self.master, text = "Time:   {}:{}".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)), font = ("TkDefaultFont", 12))
        self.timer2.grid(row = 0, column = 6, columnspan = 3, sticky = E)

        
        ##information side panel
        #make the label saying "Information"
        infoTitle = Label(self.master, text = "Information", font = ("TkDefaultFont", 12), width = 22)
        infoTitle.grid(row = 1, rowspan = 8, column = 0, sticky = N)
        #make the place for the actual information to display. Set to the string for the white player's turn to start with
        self.information = Label(self.master, text = "Player One's turn.\nSelect a white piece to move.", font = ("TkDefaultFont", 12), width = 22, bg = "red")
        self.information.grid(row = 1, rowspan = 8, column = 0)
        
        # highlight checkbutton
        self.highlightBox = Checkbutton(self.master, text = "Highlight?", font = ("TkDefaultFont", 12), command = lambda: self.highlightCheck())
        self.highlightBox.grid(row = 9, column = 0)
        #set the button to on by default
        self.highlightBox.select()
        
        ##discard side panel
        discardTitle = Label(self.master, text = "Discard", font = ("TkDefaultFont", 12), width = 22)
        discardTitle.grid(row = 1, column = 9, columnspan = 3, sticky = N)
        #white discard labels
        dWhiteLabel = Label(self.master, text = "White", font = ("TkDefaultFont", 12))
        dWhiteLabel.grid(row = 2, column = 9)
        #black discard labels
        dBlackLabel = Label(self.master, text = "Black", font = ("TkDefaultFont", 12))
        dBlackLabel.grid(row = 2, column = 11)

        #text to hold the number of each piece type discarded for the white player
        i = 3
        for p in range(0, len(self.discardType)):
            self.whiteDiscardLabels[self.discardType[p]] = Label(self.master, text = "x{}".format(self.whiteDiscard[p]), font = ("TkDefaultFont",12))
            self.whiteDiscardLabels[self.discardType[p]].grid(row = i, column = 9)
            i += 1

        #text to hold the number of each piece type discarded for the black player
        i = 3
        for p in range(0, len(self.discardType)):
            self.blackDiscardLabels[self.discardType[p]] = Label(self.master, text = "x{}".format(self.blackDiscard[p]), font = ("TkDefaultFont",12))
            self.blackDiscardLabels[self.discardType[p]].grid(row = i, column = 11)
            i += 1

        #add discard buttons with images (used for pawn swap)
        img = discardQueen
        dQueen = Button(self.master, bg = "grey", bd = 1, image = img)
        dQueen.grid(row = 3, column = 10)
        dQueen.config(command = lambda:  self.process(dQueen))

        img = discardBishop
        dBishop = Button(self.master, bg = "grey", bd = 1, image = img)
        dBishop.grid(row = 4, column = 10)
        dBishop.config(command = lambda: self.process(dBishop))

        img = discardKnight
        dKnight = Button(self.master, bg = "grey", bd = 1, image = img)
        dKnight.grid(row = 5, column = 10)
        dKnight.config(command = lambda: self.process(dKnight))

        img = discardRook
        dRook = Button(self.master, bg = "grey", bd = 1, image = img)
        dRook.grid(row = 6, column = 10)
        dRook.config(command = lambda: self.process(dRook))

        img = discardPawn
        dPawn = Button(self.master, bg = "grey", bd = 1, image = img)
        dPawn.grid(row = 7, column = 10)
        dPawn.config(command = lambda: self.process(dPawn))

        quitButton = Button(self.master, text = "Quit", font = ("TkDefaultFont", 12), width = 10, height = 1, command = lambda : self.quitProgram())
        quitButton.grid(row = 9, column = 10)

    def quitProgram(self):
        if (MUSIC):
            pygame.mixer.music.stop()
        if (GPIO):
            GPIO.cleanup()
        self.master.destroy()
        
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
        self.blackPieces.append(Queen(blackQueen, "black", 14))
        self.blackPieces.append(King(blackKing, "black", 15))
        
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

        if (GPIO):
            #light led line accordingly
            self.setupGPIO()

    def red(self, led):
        GPIO.output(led[0], GPIO.LOW)
        GPIO.output(led[1], GPIO.HIGH)

    def blue(self, led):
        GPIO.output(led[0], GPIO.HIGH)
        GPIO.output(led[1], GPIO.LOW)

    def purple(self, led):
        GPIO.output(led[0], GPIO.HIGH)
        GPIO.output(led[1], GPIO.HIGH)
        
    def setupGPIO(self):
        #setup GPIO mode
        GPIO.setmode(GPIO.BCM)
        #setup pins[blue, red]
        led0 = [17, 18]
        led1 = [16, 19]
        led2 = [13, 20]
        led3 = [12, 21]
        led4 = [6, 22]
        #store leds in a list
        ledLine = [led0, led1, led2, led3, led4]
        #set all pins connected to leds as output
        for led in range(len(ledLine)):
            for pin in range(0,2):
                GPIO.setup(ledLine[led][pin], GPIO.OUT)
        
        #determine player scores based on pieces in play
        redScore = 0
        blueScore = 0
        for piece in range(len(self.whitePieces)):
            redScore += self.whitePieces[piece].pieceValue
        for piece in range(len(self.blackPieces)):
            blueScore += self.blackPieces[piece].pieceValue

        #find total by summing two scores, then find the red player's percent
        total = redScore + blueScore
        redPercent = (float(redScore)/total) * 100

        #store what led should be purple based on range
        percentRange = {"range(0,20)":0, "range(20,40)":1, "range(40,60)":2,\
                     "range(60,80)":3, "range(80,100)":4}

        #look through ranges until one is found that contains the red percent
        for key in percentRange.keys():
            if (int(redPercent) in eval(key)):
                for led in range(len(ledLine)):
                    #if it is before the purple led, it is red
                    if (led < percentRange[key]):
                        stringLED = "self.red(led" + str(led) + ")"
                        eval(stringLED)
                    #if it is the purple led, it is purple
                    elif (led == percentRange[key]):
                        stringLED = "self.purple(led" + str(led) + ")"
                        eval(stringLED)
                    #if it is after the purple led, it is blue
                    else:
                        stringLED = "self.blue(led" + str(led) + ")"
                        eval(stringLED)
        
    def play(self):
        #would return a result of victor in the end
        pass


    #process function for the highlight check box, where clicking it will turn highlighting on or off
    def highlightCheck(self):
        if DEBUG:
            print "this is the highlight check function"
        #turn highlighting on if it is already active else turn it on. Adjust highlights on or off appropriately
        if (self.highlightActive):
            if DEBUG:
                print "the button is active, so turn it off"
                    
            self.highlightActive = False
            #if there is a piece selected, remove the highlights from it and all possible moves 
            if (self.pieceSelected != None):
                self.removeHighlight(self.tiles[self.pieceSelected.position])
                self.tiles[self.pieceSelected.position].config(bg = "green")
                
        else:
            if DEBUG:
                print "the button is inactive, so turn it on"
            self.highlightActive = True
            #if there is a piece selected, remove the highlights from it and all possible moves 
            if (self.pieceSelected != None):
                self.highlight(self.tiles[self.pieceSelected.position])


    #function to allow Buttons to be processed after being clicked (NOTE: this function processes a button being
    #pressed, so it takes a button as the input, not the piece, though the piece and button have the same coordinate
    #so a function can be made to return the piece based on the button)
    def process(self, button):

        #if a pawn swap is currenly in place, it must be finished before any other
        #processes can be handled (must select a piece to swap with
        if (self.pawnSwap):
            #go through and see if the button selected is in column 10 first (all discard buttons are there)
            if (int(button.grid_info()["column"]) == 10):
                #because the button clicked is in the correct column, get the row value to check which piece
                #the player is trying to gain
                row = int(button.grid_info()["row"])
                #hold the position of the pawn in case it is needed to swap with another piece
                pawnPosition = self.pieceSelected.position

                #if the row matches the row value of any of the four pieces possible to swap with, then
                #add in that piece
                if(row >= 3 and row <=6):
                    #subtract 3 so the row value will match the indexes of the discardType list
                    self.addPiece(row-3, pawnPosition)

            #check if pawn swap already occured during this passthrough
            if (not self.pawnSwap):
                #check the king for the player not currently moving to see if that player will be in check
                #for their turn (color of the other player is the opposite of the color of the currently
                #selected piece)
                if(self.pieceSelected.color == "white"):
                    king = self.getBlackKing()
                else:
                    king = self.getWhiteKing()

                #check if the player about to move is in check as a result of the move just made by the opponent
                if (self.kingCheck(king)):
                    if (DEBUG):
                        print "The king is contested!"
                        
                    #see if the player would be in checkmate, and end the game if they are
                    if (self.checkMate()):
                        pass

                    #in check, but not checkmate. set currentPlayerContested to True to reflect this, which
                    #will modify what possibleMoves are allowed to be kept as valid
                    self.currentPlayerContested = True

                #player is not contested, so reflect that in the boolean
                else:
                    self.currentPlayerContested = False

                #set the piece selected to None
                self.pieceSelected = None
                self.pieceSelectedMoves = []
                
                #change the turn to the other player
                self.changeTurn()

                #make the text in the info pannel reference the player being in check (if applicable)
                if (self.currentPlayerContested):
                    self.information.config(text = "You are in Check!\nYou must move a piece\nto exit this state.")

        #not currently in a pawnSwap state, continue normally with logic
        else:
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
                        if DEBUG:
                            print "possible moves of selected piece: {}".format(self.pieceSelectedMoves)

                        #if the player is contested, check if the possibleMoves of the selected piece
                        #would result in the player no longer being selected (logic in playerContested()
                        #function)
                        self.playerContested()
                            
                        #add line to skip highlighting and deselect piece if no valid moves
                        if (self.pieceSelectedMoves == []):
                            self.pieceSelected = None
                            #update info pannel to reflect this
                            self.information.config(text = "You can't move that piece\nTry moving a different one.")
                        
                        #only highlight if there are any possible moves
                        if (self.pieceSelectedMoves != []):
                            #highlight the button holding the selected piece and possible moves
                            self.highlight(button)
                            #update info pannel to reflect this
                            self.information.config(text = "Select where you\nwill move this piece.")

                    #piece selected is not current player's piece, deselect pieces
                    else:
                        self.pieceSelected = None
                        self.pieceSelectedMoves = []
                
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
                            self.pawnSwap = True
                            # prompt user about pawnSwap in info
                            self.information.config(text = "Click a piece in\nthe right column to\npromote your pawn to.")
                        else:
                            #check the king for the player not currently moving to see if that player will be in check
                            #for their turn (color of the other player is the opposite of the color of the currently
                            #selected piece)
                            if(self.pieceSelected.color == "white"):
                                king = self.getBlackKing()
                            else:
                                king = self.getWhiteKing()

                            #check if the player about to move is in check as a result of the move just made by the opponent
                            if (self.kingCheck(king)):
                                if (DEBUG):
                                    print "The king is contested!"
                                    
                                #see if the player would be in checkmate, and end the game if they are
                                if (self.checkMate()):
                                    pass

                                #in check, but not checkmate. set currentPlayerContested to True to reflect this, which
                                #will modify what possibleMoves are allowed to be kept as valid
                                self.currentPlayerContested = True

                            #player is not contested, so reflect that in the boolean
                            else:
                                self.currentPlayerContested = False
                                
                            #set the pieceSelected to none and remove all indexes from the piece selected list
                            self.pieceSelected = None
                            self.pieceSelectedMoves = []
                            #change the turn to the other player
                            self.changeTurn()

                            #make the text in the info pannel reference the player being in check (if applicable)
                            if (self.currentPlayerContested):
                                self.information.config(text = "You are in Check!\nYou must move a piece\nto exit this state.")

                    #invalid blank tile selected, inform player they cannot move there
                    else:
                        self.information.config(text = "You can't move\nyour piece there.")

                #if the same piece was clicked a second time, deselect it and unhighlight everything
                elif (secondPiece == self.pieceSelected):
                        #remove highlight from the button holding the selected piece and possible moves
                        self.removeHighlight(self.tiles[self.pieceSelected.position])

                        #set the piece selected to None
                        self.pieceSelected = None
                        self.pieceSelectedMoves = []
                        
                        #update info back to the default start of turn text
                        #default text is for player being in check (if applicable)
                        if (self.currentPlayerContested):
                            self.information.config(text = "You are in Check!\nYou must move a piece\nto exit this state.")
                        #player is not in check, so use basic turn start text based on the current player's turn
                        elif (self.currentTurn == "white"):
                            self.information.config(text = "Player One's turn.\nSelect a white piece to move.")
                        else:
                            self.information.config(text = "Player Two's turn.\nSelect a black piece to move.")
                    
                #there is a piece on the second tile selected, so check to see if the piece selected
                #is in the valid range of pieceSelectedMoves
                elif (secondPiece.position in self.pieceSelectedMoves):
                    #remove highlight from the button holding the selected piece and possible moves
                    self.removeHighlight(self.tiles[self.pieceSelected.position])

                    #call the overtake function to remove the second piece from play and place it on
                    #the column where it belongs
                    self.overtake(secondPiece)

                    #change the position of the moving piece to that of the one being overtaken
                    self.changePosition(button)

                    #if piece is pawn, check to see if it reached the end of the board and should be swapped
                    if((self.pieceSelected.image == whitePawn and self.pieceSelected.row == 1) or\
                        (self.pieceSelected.image == blackPawn and self.pieceSelected.row == 8)):
                        self.pawnSwap = True
                        # prompt user about pawnSwap in info
                        self.information.config(text = "Click a piece in\nthe right column to\npromote your pawn to.")
                    else:
                        #check the king for the player not currently moving to see if that player will be in check
                        #for their turn (color of the other player is the opposite of the color of the currently
                        #selected piece)
                        if(self.pieceSelected.color == "white"):
                            king = self.getBlackKing()
                        else:
                            king = self.getWhiteKing()

                        #check if the player about to move is in check as a result of the move just made by the opponent
                        if (self.kingCheck(king)):
                            if (DEBUG):
                                print "The king is contested!"
                                
                            #see if the player would be in checkmate, and end the game if they are
                            if (self.checkMate()):
                                pass

                            #in check, but not checkmate. set currentPlayerContested to True to reflect this, which
                            #will modify what possibleMoves are allowed to be kept as valid
                            self.currentPlayerContested = True

                        #player is not contested, so reflect that in the boolean
                        else:
                            self.currentPlayerContested = False

                        #set the piece selected to None
                        self.pieceSelected = None
                        self.pieceSelectedMoves = []
                        
                        #change the turn to the other player
                        self.changeTurn()

                        #make the text in the info pannel reference the player being in check (if applicable)
                        if (self.currentPlayerContested):
                            self.information.config(text = "You are in Check!\nYou must move a piece\nto exit this state.")

                #check if the second piece selected is the same color as the first
                elif (secondPiece.color == self.pieceSelected.color):
                    #deselect the first piece and remove all its highlights, then select the new
                    #piece and display its highlights

                    #remove highlight from the button holding the selected piece and possible moves
                    self.removeHighlight(self.tiles[self.pieceSelected.position])

                    #set the initial selected piece to the new choice
                    self.pieceSelected = secondPiece
                    self.pieceSelectedMoves = []
                    
                    #get the list of possible moves the piece can perform
                    self.pieceSelectedMoves = self.pieceSelected.possibleMoves()

                    #if the player is contested, check if the possibleMoves of the selected piece
                    #would result in the player no longer being selected.
                    self.playerContested()

                    #add line to skip highlighting and deselect piece if no valid moves
                    if (self.pieceSelectedMoves == []):
                        self.pieceSelected = None
                        #update info pannel to reflect this
                        self.information.config(text = "You can't move that piece\nTry moving a different one.")
                        
                    #only highlight if there are any possible moves
                    else:
                        #highlight the button holding the selected piece and possible moves
                        self.highlight(self.tiles[self.pieceSelected.position])
                        #update info pannel to reflect this
                        self.information.config(text = "Select where you\nwill move this piece.")

                #piece selected cannnot be overtaken
                else:
                    self.information.config(text = "You can't move\nyour piece there.")


    #below are functions for the Game class utilized by the process function
                        
    #change the current turn to the opposite player, update the information text to the default
    #saying whose turn it is
    def changeTurn(self):
        if (self.currentTurn == "white"):
            self.currentTurn = "black"
            self.information.config(text = "Player Two's turn.\nSelect a black piece to move.")
        else:
            self.currentTurn = "white"
            self.information.config(text = "Player One's turn.\nSelect a white piece to move.")
    
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

        #blank tile, so simply move the initial selection to the secondary location, updating the pictures for both
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
    def overtake(self, secondarySelection):
        secondarySelection.updatePiecePosition(00)
        self.updateDiscard(secondarySelection)

    # function that increments discarded piece count based on a given image and value
    def updateDiscard(self, secondarySelection):
        # find the piece type index to update the parallel list
        for i in range(0, len(self.discardType)):
            if (self.discardType[i] == secondarySelection.pieceType):
                index = i
        
        # determine color and update parallel list
        if (secondarySelection.color == "white"):
            self.whitePieces.remove(secondarySelection)
            self.whiteDiscard[index] += 1
            self.whiteDiscardLabels[self.discardType[index]].config(text = "x{}".format(self.whiteDiscard[index]))
        else:
            self.blackPieces.remove(secondarySelection)
            self.blackDiscard[index] += 1
            self.blackDiscardLabels[self.discardType[index]].config(text = "x{}".format(self.blackDiscard[index]))

        if (GPIO):
            self.setupGPIO()

    #function to display whose turn it is currently
    def displayTurn(self):
        if (self.currentTurn == "white"):
            self.p1Turn.config(bg = "red", text = "Your Turn")
            self.p2Turn.config(bg = "grey85", text = "")
            self.information.config(bg = "red")
            
        else:
            self.p1Turn.config(bg = "grey85", text = "")
            self.p2Turn.config(bg = "light blue", text = "Your Turn")
            self.information.config(bg = "light blue")

        # loops the function every millisecond
        self.after(1, self.displayTurn)


    #function used for pawnswap to add a new instance of the desired piece
    def addPiece(self, row, pawnPosition):
        #overtake the pawn to remove it from the board first
        self.overtake(self.pieceSelected)

        #determine the type of piece selected
        pieceType = self.discardType[row]

        #if currentTurn is white, make a new instance of a pieceType class with correct color
        if (self.currentTurn == "white"):
            #build the call function in a string to be evaluated
            newPieceString = pieceType+"(white"+pieceType+", 'white', pawnPosition)"
            newPiece = eval(newPieceString)
            #add new piece to pieces in play by color
            self.whitePieces.append(newPiece)
        #if currentTurn is black, make a new instance of a pieceType class with correct color
        else:
            #build the call function in a string to be evaluated
            newPieceString = pieceType+"(black"+pieceType+", 'black', pawnPosition)"
            newPiece = eval(newPieceString)
            #add new piece to pieces in play by color
            self.blackPieces.append(newPiece)

        #place the piece appropriately on the board (image on the tile and
        #give the piece the appropriate position)
        self.tiles[pawnPosition].configure(image = newPiece.image)
        newPiece.updatePiecePosition(pawnPosition)

        self.setupGPIO()
        
        #set pawn swap to false to indicate the swap was successfully completed
        self.pawnSwap = False

    ######functions for timer processing
        
    #function to setup which timer will be used based on the main menu input
    def timerSetup(self):

        if (timerCheck == 1):
            if (timerType == 1):
                #normal timer
                self.p1Time = 900
                self.p2Time = 900
                if DEBUG:
                    print "returning countdown for normal timer"
                    
            else:
                #blitz timer
                self.p1Time = 300
                self.p2Time = 300

            return "countdown"
        
        else:
            #no timer
            self.p1Time = 0
            self.p2Time = 0
            return "countup"


        
        '''#normal timer uses default 900 seconds
        if (timerCheck == "normal"):
            self.p1Time = 900
            self.p2Time = 900
            if DEBUG:
                print "returning countdown for normal timer"
            
            return "countdown"

        #blitz timer uses 300 seconds
        elif (timer == "blitz"):
            self.p1Time = 300
            self.p2Time = 300
            return "countdown"

        #no timer, so the clocks will count up instead
        else:
            self.p1Time = 0
            self.p2Time = 0
            return "countup"'''

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

    #function that counts up and updates the player timers on a loop
    def countup(self):
        # counts down selected player's timer
        if (self.currentTurn == "white"):
            self.p1Time += 1
            self.timer1.config(text = "Time:   {}:{}".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)))
             
        else:
            self.p2Time += 1
            self.timer2.config(text = "Time:   {}:{}".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)))
            
        # loops the function every second
        self.after(1000, self.countup)

    ########end of timer functions

    ########highlight buttons as needed with these functions
        
    #highlight initially selected piece green, and all possible moves
    #yellow (blank) or red (occupied)
    def highlight(self, button):
        #highligh initial selection
        button.config(bg = "green")

        #only highlight all tiles if checkbox active
        if (self.highlightActive):
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
            

    #################################################################################king logic

    #function to return the piece instance of the black king
    def getBlackKing(self):
        for piece in self.blackPieces:
                if (piece.image == blackKing):
                    return piece

    #function to return the piece instance of the white king
    def getWhiteKing(self):
        for piece in self.whitePieces:
                if (piece.image == whiteKing):
                    return piece

    #function similar to the getKing function but to get the knights because they are
    #the only piece which can hop other pieces to move and need to be checked
    #to see if they would put the king in check
    def getKnights(self, king):
        #list to hold all knights found (0-2 depending on how many were overtaken)
        knights = []
        
        #if white just moved, find the black Knight instances in the blackPieces list
        if (king.color == "white"):
            for piece in self.blackPieces:
                if (piece.image == blackKnight):
                    knights.append(piece)
        #black just moved, so find white Knights in whitePieces list
        else:
            for piece in self.whitePieces:
                if (piece.image == whiteKnight):
                    knights.append(piece)

        #if the knight is still in play but has a position of None, this means the logic in the
        #invalidUncheckMove function is processing a potential move where the knight would be
        #overtaken. In this case, do not use that knight in determining if the king is in check
        for piece in knights:
            if (piece.position == None):
                knights.remove(piece)
                
        return knights

    #function to check if the position of a king is in the possibleMoves of another
    #specified piece
    def pieceInKingRange(self, king, other):
        otherMoves = other.possibleMoves()
        if (king.position in otherMoves):
            return True
        else:
            return False

    #function to hold the general logic used when searching for if the king is in check,
    #which can be applied to any direction based on inputted values of r and c (r and c
    #values are used to modify the row and column depending on the direction desired)
    def kingCheckLogic(self, king, r, c):
        #stay in loop until invalid tile reached (or manual break)
        while (king.isValidTile(king.row + r, king.column + c, king.color)):
            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(king.row+r)*10+(king.column+c)]) != None):
                
                #check if the king could be hit by the piece in question
                if (self.pieceInKingRange(king, Game.getPiece(game, Game.tiles[(king.row+r)*10+(king.column+c)]))):
                    #king can be hit, so set contested factors to True and return True
                    return True

            #modify r and c values appropriately
            r = self.modifyRowColValues(r)
            c = self.modifyRowColValues(c)

        #king is not in check from this direction
        return False

    #function used by the kingCheckLogic function to modify the row and column values appropriately,
    #where one is passed in at a time
    def modifyRowColValues(self, i):
        #increment a positive value, decrement a negative, or leave a 0 value unchanged
        if(i > 0):
            return i + 1
        elif(i < 0):
            return i - 1
        else:
            return i
    
    #function used after a player has moved to look at the king of the other player
    #and see if that other player is in check (ex: player A's piece is moved, check
    #player B's king)
    def kingCheck(self, king):
        #ignoring knights until below this logic, a piece must be in one of eight directions
        #around the king to even have the potential of hitting him. Therefore, implement
        #logic similar to how the queen's possibleMoves function works, where all directions
        #are checked until a piece is reached. One a piece is reached, check if the piece is
        #of the opposite color. If so, call the possibleMoves for that piece and check if the
        #position of the king is in the list of that piece's possible moves. If not, continue
        #to check the remaining directions. If so, then immediately return True (and set king
        #contested variable to True if it is needed and kept)

        #check all directions using kingCheckLogic function to see if any piece could put the
        #king in check in those directions
        #SW
        if (self.kingCheckLogic(king, 1, -1)):
            return True
        #SE
        if (self.kingCheckLogic(king, 1, 1)):
            return True
        #NE
        if (self.kingCheckLogic(king, -1, 1)):
            return True
        #NW
        if (self.kingCheckLogic(king, -1, -1)):
            return True
        #up(up screen is negative y direction)
        if (self.kingCheckLogic(king, -1, 0)):
            return True
        #down screen, positive y
        if (self.kingCheckLogic(king, 1, 0)):
            return True
        #left
        if (self.kingCheckLogic(king, 0, -1)):
            return True
        #right
        if (self.kingCheckLogic(king, 0, 1)):
            return True

        #also need to check if either of the knights on the other player's team can hit the king
        #first, get the list of all opposing knights on the board
        knights = self.getKnights(king)
        for piece in knights:
            #check if the king could be hit by the knight in question
                if (self.pieceInKingRange(king, piece)):
                    #king can be hit, so set contested factors to True and return True
                    return True

        #the king is not contested, so return False
        return False

    #function used to see if a king is in checkmate. Only called if a player is confirmed to be in
    #check by the kingCheck function to see if the game should be ended
    def checkMate(self):
        #to check pieces, set the piece needed to be checked to selectedPiece and store its moves in
        #selectedPieceMoves so each move can be checked to see if any moves are valid
        #first, change the turn so the player whose king is being checked is considered the "currentTurn"
        self.changeTurn()

        #assume in checkmate until proven otherwise
        checkmate = True

        #go through the list of pieces for the player in question and find possible moves. Once a move is
        #found and put into the moves list, the for loop can be broken from because the player is not in
        #checkmate
        if(self.currentTurn == "white"):
            pieceList = self.whitePieces

        else:
            pieceList = self.blackPieces

        #go through every piece and see if any piece has at least one possible move. If a move is found,
        #the player is not in checkmate
        for piece in pieceList:
            self.pieceSelected = piece
            self.pieceSelectedMoves = self.pieceSelected.possibleMoves()
            self.playerContested()

            #at least one piece has a possible move to take the player out of check, so break from the loop
            if (len(self.pieceSelectedMoves) > 0):
                checkmate = False
                break
                
        #change the currentTurn back to the original player who just moved to avoid skipping a player's turn
        self.changeTurn()

        #if there are no possible moves found for any pieces, the player is in checkmate
        if (checkmate):
            if DEBUG:
                print "Checkmate, game over"
            return True
        else:
            if DEBUG:
                print "only check, game continues"
            return False

    #function to process the moves for a player who is currently contested
    def playerContested(self):
        #hold all moves to be removed in this list to avoid issues which checking
        #every index, removing all values from the actual pieceSelectedMoves list
        #at the end all at once
        remove = []
        for move in self.pieceSelectedMoves:
            if DEBUG:
                print "move to look at: {}".format(move)
            if (self.invalidUncheckMove(move)):
                #the move is not valid for removing the player from check, so it is invalid
                remove.append(move)

        #iterate through the remove list to remove the specified values from the list of
        #pieceSelectedMoves
        for index in remove:
            self.pieceSelectedMoves.remove(index)

        if DEBUG:
            print "since player is contested, this is the new list of "\
                    + "possible moves: {}".format(self.pieceSelectedMoves)

    #function to determine if a specified move is valid to make the king no longer be in check
    #or to make sure a move would not make the player put themselves into check
    def invalidUncheckMove(self, move):
        if DEBUG:
            print "Move in question: {}".format(move)
            
        #if there is a piece at the position in question that the selected piece is being moved to, then
        #it must be an overtake, so find that piece and remove its position (to be added back at end)
        overtakenPiece = None
        if (self.getPiece(self.tiles[move]) != None):
            #don't change the actual tiles or images, but set the position of that piece to be 00 (invalid)
            #and store the piece itself in a variable so it can be given its position back
            overtakenPiece = self.getPiece(self.tiles[move])
            overtakenPiece.updatePiecePosition(00)
            if DEBUG:
                print "overtaken piece position set to {}".format(overtakenPiece.position)

        elif (DEBUG):
            print "no piece to overtake"

        #store the piece in question's current position so it can be reset
        originalPos = self.pieceSelected.position
        #don't use change position function because only want to temporary change it, therefore the image
        #does not need to be changed
        self.pieceSelected.updatePiecePosition(move)
        if DEBUG:
            print "selected piece position updated to move: {}".format(self.pieceSelected.position)

        
                        
        #check the king for the player currently trying to move to see if, with the piece moved to its new
        #potential location, the king would no longer be in check
        if (self.currentTurn == "white"):
            invalid = self.kingCheck(self.getWhiteKing())
        else:
            invalid = self.kingCheck(self.getBlackKing())

        if DEBUG:
            print "invalid = {}".format(invalid)

        #change the position of the selected piece back to where it originally was
        self.pieceSelected.updatePiecePosition(originalPos)
        if DEBUG:
            print "selected piece position reset to: {}".format(self.pieceSelected.position)

        #if the overtaken piece had its position removed, then add it back
        if (overtakenPiece != None):
            overtakenPiece.updatePiecePosition(move)
            if DEBUG:
                print "overtaken piece position reset to: {}".format(overtakenPiece.position)

        if DEBUG:    
            print "end of looking at move {}, proceeding...........................".format(move)
        #returns whether the possible move is valid to take the player out of check
        return invalid
            
            

    #################################################################################end of king functions


#Piece class: biggest class in center of program, (need to implement "hasa" relationship under Tile and Player classes
#possibly byincluding an instance of the piece class in the Tile and Player classes?)
class Piece(Game):
    #instance variables for piece class
    def __init__(self, image, color, position):
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

    #function to hold the movement logic for both the bishop and rook to reduce copied code
    def bishopAndRookLogic(self, moves, r, c):
        #stay in loop until invalid tile reached (or manual break)
        while (self.isValidTile(self.row + r, self.column + c, self.color)):
            #append the next move to the moves list
            moves.append((self.row+r)*10 + self.column+c)

            #use the getPiece function in Game to determine if there is a piece on the tile
            #(if there is, then the tile by default would hold a piece of the opposite color,
            #which is valid and was already added to the list, though no further moves will work)
            if (Game.getPiece(game, Game.tiles[(self.row+r)*10+(self.column+c)]) != None):
                break

            #modify r and c values appropriately (use function from the Game class also used by the king)
            r = self.modifyRowColValues(r)
            c = self.modifyRowColValues(c)

        #send the moves list back to the general movement function
        return moves


    #possible moves for the bishop (located here because Queen and Bishop classes both utilize this function)
    def bishopPossibleMoves(self):
        moves = []

        #call function using values to modify row and column in each direction and append possible
        #moves to the possible moves list
        #move SE
        moves = self.bishopAndRookLogic(moves, 1, 1)
        #move SW
        moves = self.bishopAndRookLogic(moves, 1, -1)
        #move NE
        moves = self.bishopAndRookLogic(moves, -1, 1)
        #move NW
        moves = self.bishopAndRookLogic(moves, -1, -1)
        
        return moves
	
    #possible moves for the rook (located here because Queen and Rook classes both utilize this function)
    def rookPossibleMoves(self):
        moves = []

        #call function using values to modify row and column in each direction and append possible
        #moves to the possible moves list
        #move up(up screen is negative y direction)
        moves = self.bishopAndRookLogic(moves, -1, 0)
        #move down screen, positive y
        moves = self.bishopAndRookLogic(moves, 1, 0)
        #move left
        moves = self.bishopAndRookLogic(moves, 0, -1)
        #move right
        moves = self.bishopAndRookLogic(moves, 0, 1)

        return moves
    
#All the individual types of pieces have classes defined below (concrete functions)
#King class
class King(Piece):
    #utilize the Piece class constructor, in addition to the contested variable (False by default)
    pieceType = "King"
    pieceValue = 0
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)

    
    #function to determine the possible moves a piece can make (takes contested state into account as well, but can be accessed
    #using self.contested when needed)
    def possibleMoves(self):
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
    pieceType = "Queen"
    pieceValue = 3
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #queen moves = rook moves + bishop moves
        return self.rookPossibleMoves() + self.bishopPossibleMoves()
    
#Rook class
class Rook(Piece):
    pieceType = "Rook"
    pieceValue = 2
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #call the function for rookPossibleMoves in the Pieces class and return the result
        return self.rookPossibleMoves()
    
#Bishop class
class Bishop(Piece):
    pieceType = "Bishop"
    pieceValue = 2
    #utilize the Piece class constructor
    def __init__(self, image, color, position):
        Piece.__init__(self, image, color, position)
    
    #function to determine the possible moves a piece can make
    def possibleMoves(self):
        #call the function for bishopPossibleMoves in the Pieces class and return the result
        return self.bishopPossibleMoves()
        
#Knight class
class Knight(Piece):
    pieceType = "Knight"
    pieceValue = 2
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
    pieceType = "Pawn"
    pieceValue = 1
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
    
#initialize pygame and the mixer for the music to work
if MUSIC:
    pygame.init()
    pygame.mixer.init()

#setup initial window for the main menu of the game (including playing music) 
window2 = Tk()
window2.title("Chess Reloaded")
menu = Menu(window2)
menu.setupGUI()
if MUSIC:
    pygame.mixer.music.load("music/menu.mp3")
    #-1 in play makes an infinite loop of the music until it is told otherwise
    pygame.mixer.music.play(-1)
window2.mainloop()

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
discardQueen = PhotoImage(file = "images/discardQueen.gif")
discardBishop = PhotoImage(file = "images/discardBishop.gif")
discardKnight = PhotoImage(file = "images/discardKnight.gif")
discardRook = PhotoImage(file = "images/discardRook.gif")
discardPawn = PhotoImage(file = "images/discardPawn.gif")

window.title("Chess Reloaded")
game = Game(window)

#figure out which timer function (countdown or up) is needed and set the timers
timerFunction = game.timerSetup()

#setup the components for teh gui and game to be ready to use, including tiles and pieces
game.setupGUI()
game.setupGame()

#start the loop for the appropriate timer to run
eval("game."+timerFunction+"()")

#set the current turn to display to allow the game to start properly
game.displayTurn()

#play the music if desired
if MUSIC:
    pygame.mixer.music.load("music/gameplay.ogg")
    #-1 in play makes an infinite loop of the music until it is told otherwise
    pygame.mixer.music.play(-1)
    
window.mainloop()

####note: once exit buttons are installed, they will need to take into account
####turning the music off

#credits for music:
#       freesound.org:
#               littlerobotsoundfactory jingle_win_00.wav (victory.mp3)
#               fmceretta Racing game menu music - while buying
#                    fancy cars we will never have!.mp3 (menu.mp3)
#       E's Jammy Jam (gameplay.mp3)
