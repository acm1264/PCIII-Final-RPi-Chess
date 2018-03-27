######################################################
# Names: Andrew Maurice, Cody Johnson, Lindsay Cason
# Date: 5/16/18
# Description: DOES SOME PRETTY COOL STUFF
#####################################################

from Tkinter import *
        
class newGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.p1Time = 300
        self.p2Time = 300
        self.whichTimer = 1


    # p1Time accessor
    @property
    def p1Time(self):
        return self._p1Time


    # p1Time mutator
    @p1Time.setter
    def p1Time(self, value):
        self._p1Time = value


    # p2Time accessor
    @property
    def p2Time(self):
        return self._p2Time


    # p2Time mutator
    @p2Time.setter
    def p2Time(self, value):
        self._p2Time = value


    # whichTimer accessor
    @property
    def whichTimer(self):
        return self._whichTimer


    # whichTimer mutator
    @whichTimer.setter
    def whichTimer(self, value):
        self._whichTimer = value


##### sets up the majority of the GUI
    def setupGUI(self):
        # creates buttons for each of the chess board tiles, initialized with the image of the piece located
        # on each tile by default (or the blank image for the other tiles)
        # tiles are numbered with two digit codes, where the first number represents the row
        # and the second digit represents the column
        
        # first row
        square01 = Button(self.master, image = blackRook, bd = 1, command = lambda: self.highlight(square01))
        square01.grid(row = 0, column = 1)
        square02 = Button(self.master, image = blackKnight, bd = 1, command = lambda: self.highlight(square02))
        square02.grid(row = 0, column = 2)
        square03 = Button(self.master, image = blackBishop, bd = 1, command = lambda: self.highlight(square03))
        square03.grid(row = 0, column = 3)
        square04 = Button(self.master, image = blackQueen, bd = 1, command = lambda: self.highlight(square04))
        square04.grid(row = 0, column = 4)
        square05 = Button(self.master, image = blackKing, bd = 1, command = lambda: self.highlight(square05))
        square05.grid(row = 0, column = 5)
        square06 = Button(self.master, image = blackBishop, bd = 1, command = lambda: self.highlight(square06))
        square06.grid(row = 0, column = 6)
        square07 = Button(self.master, image = blackKnight, bd = 1, command = lambda: self.highlight(square07))
        square07.grid(row = 0, column = 7)
        square08 = Button(self.master, image = blackRook, bd = 1, command = lambda: self.highlight(square08))
        square08.grid(row = 0, column = 8)


        # second row
        square11 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square11))
        square11.grid(row = 1, column = 1)
        square12 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square12))
        square12.grid(row = 1, column = 2)
        square13 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square13))
        square13.grid(row = 1, column = 3)
        square14 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square14))
        square14.grid(row = 1, column = 4)
        square15 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square15))
        square15.grid(row = 1, column = 5)
        square16 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square16))
        square16.grid(row = 1, column = 6)
        square17 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square17))
        square17.grid(row = 1, column = 7)
        square18 = Button(self.master, image = blackPawn, bd = 1, command = lambda: self.highlight(square18))
        square18.grid(row = 1, column = 8)


        # third row
        square21 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square21))
        square21.grid(row = 2, column = 1)
        square22 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square22))
        square22.grid(row = 2, column = 2)
        square23 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square23))
        square23.grid(row = 2, column = 3)
        square24 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square24))
        square24.grid(row = 2, column = 4)
        square25 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square25))
        square25.grid(row = 2, column = 5)
        square26 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square26))
        square26.grid(row = 2, column = 6)
        square27 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square27))
        square27.grid(row = 2, column = 7)
        square28 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square28))
        square28.grid(row = 2, column = 8)


        # fourth row
        square31 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square31))
        square31.grid(row = 3, column = 1)
        square32 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square32))
        square32.grid(row = 3, column = 2)
        square33 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square33))
        square33.grid(row = 3, column = 3)
        square34 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square34))
        square34.grid(row = 3, column = 4)
        square35 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square35))
        square35.grid(row = 3, column = 5)
        square36 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square36))
        square36.grid(row = 3, column = 6)
        square37 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square37))
        square37.grid(row = 3, column = 7)
        square38 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square38))
        square38.grid(row = 3, column = 8)


        # fifth row
        square41 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square41))
        square41.grid(row = 4, column = 1)
        square42 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square42))
        square42.grid(row = 4, column = 2)
        square43 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square43))
        square43.grid(row = 4, column = 3)
        square44 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square44))
        square44.grid(row = 4, column = 4)
        square45 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square45))
        square45.grid(row = 4, column = 5)
        square46 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square46))
        square46.grid(row = 4, column = 6)
        square47 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square47))
        square47.grid(row = 4, column = 7)
        square48 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square48))
        square48.grid(row = 4, column = 8)


        # sixth row
        square51 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square51))
        square51.grid(row = 5, column = 1)
        square52 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square52))
        square52.grid(row = 5, column = 2)
        square53 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square53))
        square53.grid(row = 5, column = 3)
        square54 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square54))
        square54.grid(row = 5, column = 4)
        square55 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square55))
        square55.grid(row = 5, column = 5)
        square56 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square56))
        square56.grid(row = 5, column = 6)
        square57 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square57))
        square57.grid(row = 5, column = 7)
        square58 = Button(self.master, image = blank, bd = 1, command = lambda: self.highlight(square58))
        square58.grid(row = 5, column = 8)


        # seventh row
        square61 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square61))
        square61.grid(row = 6, column = 1)
        square62 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square62))
        square62.grid(row = 6, column = 2)
        square63 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square63))
        square63.grid(row = 6, column = 3)
        square64 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square64))
        square64.grid(row = 6, column = 4)
        square65 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square65))
        square65.grid(row = 6, column = 5)
        square66 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square66))
        square66.grid(row = 6, column = 6)
        square67 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square67))
        square67.grid(row = 6, column = 7)
        square68 = Button(self.master, image = whitePawn, bd = 1, command = lambda: self.highlight(square68))
        square68.grid(row = 6, column = 8)


        # eighth row
        square71 = Button(self.master, image = whiteRook, bd = 1, command = lambda: self.highlight(square71))
        square71.grid(row = 7, column = 1)
        square72 = Button(self.master, image = whiteKnight, bd = 1, command = lambda: self.highlight(square72))
        square72.grid(row = 7, column = 2)
        square73 = Button(self.master, image = whiteBishop, bd = 1, command = lambda: self.highlight(square73))
        square73.grid(row = 7, column = 3)
        square74 = Button(self.master, image = whiteQueen, bd = 1, command = lambda: self.highlight(square74))
        square74.grid(row = 7, column = 4)
        square75 = Button(self.master, image = whiteKing, bd = 1, command = lambda: self.highlight(square75))
        square75.grid(row = 7, column = 5)
        square76 = Button(self.master, image = whiteBishop, bd = 1, command = lambda: self.highlight(square76))
        square76.grid(row = 7, column = 6)
        square77 = Button(self.master, image = whiteKnight, bd = 1, command = lambda: self.highlight(square77))
        square77.grid(row = 7, column = 7)
        square78 = Button(self.master, image = whiteRook, bd = 1, command = lambda: self.highlight(square78))
        square78.grid(row = 7, column = 8)


        # left-side player headers
        p1Title = Label(self.master, text = " P1 ", font = ("Courier", 25))
        p1Title.grid(row = 7, column = 0)
        p2Title = Label(self.master, text = " P2 ", font = ("Courier", 25))
        p2Title.grid(row = 0, column = 0)


##### function that determines which piece was selected and displays possible moves
    def highlight(self, piece):
        # highlight and unhighlight tiles
        if (piece.cget("bg") == "black"):
            piece.config(bg = "white")
        else:
            piece.config(bg = "black")


        # switches timers when any tile is clicked, currently for testing purposes
        if (self.whichTimer == 1):
            self.whichTimer = 2
        else:
            self.whichTimer = 1

        
        # blank
        if (piece.cget("image") == "pyimage1"):
            pass
        # king
        elif ((piece.cget("image") == "pyimage2") or (piece.cget("image") == "pyimage8")):
            pass
        # queen
        elif ((piece.cget("image") == "pyimage3") or (piece.cget("image") == "pyimage9")):
            pass
        # bishop
        elif ((piece.cget("image") == "pyimage4") or (piece.cget("image") == "pyimage10")):
            pass
        # knight
        elif ((piece.cget("image") == "pyimage5") or (piece.cget("image") == "pyimage11")):
            pass
        # rook
        elif ((piece.cget("image") == "pyimage6") or (piece.cget("image") == "pyimage12")):
            pass
        # pawn
        elif ((piece.cget("image") == "pyimage7") or (piece.cget("image") == "pyimage13")):
            pass


##### function that counts down and updates player timers on a loop
    def countdown(self):
        # counts down selected player's timer
        if (self.whichTimer == 1):
            self.p1Time -= 1
        else:
            self.p2Time -= 1


        # updates the timer
        timer1 = Label(self.master, text = "     P1 Time Remaining:   {}:{}     ".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)))
        timer1.grid(row = 7, column = 9)

        timer2 = Label(self.master, text = "     P2 Time Remaining:   {}:{}     ".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)))
        timer2.grid(row = 0, column = 9)


        # loops the function every second
        self.after(1000, self.countdown)


window = Tk()

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

window.title("Chess Reloaded")
game = newGame(window)
game.setupGUI()
game.countdown()
window.mainloop()
