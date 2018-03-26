from Tkinter import *

class newGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.p1Time = 300
        self.p2Time = 300

    @property
    def p1Time(self):
        return self._p1Time

    @p1Time.setter
    def p1Time(self, value):
        self._p1Time = value

    @property
    def p2Time(self):
        return self._p2Time

    @p2Time.setter
    def p2Time(self, value):
        self._p2Time = value

    def setupGUI(self):
        blank = PhotoImage(file = "blank.gif")
        whiteKing = PhotoImage(file = "whiteKing.gif")
        whiteQueen = PhotoImage(file = "whiteQueen.gif")
        whiteBishop = PhotoImage(file = "whiteBishop.gif")
        whiteKnight = PhotoImage(file = "whiteKnight.gif")
        whiteRook = PhotoImage(file = "whiteRook.gif")
        whitePawn = PhotoImage(file = "whitePawn.gif")
        blackKing = PhotoImage(file = "blackKing.gif")
        blackQueen = PhotoImage(file = "blackQueen.gif")
        blackBishop = PhotoImage(file = "blackBishop.gif")
        blackKnight = PhotoImage(file = "blackKnight.gif")
        blackRook = PhotoImage(file = "blackRook.gif")
        blackPawn = PhotoImage(file = "blackPawn.gif")
        
        square00 = Button(self.master, image = blackRook)
        square00.image = blackRook
        square00.grid(row = 0, column = 0)

        square01 = Button(self.master, image = blackKnight)
        square01.image = blackKnight
        square01.grid(row = 0, column = 1)

        square02 = Button(self.master, image = blackBishop)
        square02.image = blackBishop
        square02.grid(row = 0, column = 2)

        square03 = Button(self.master, image = blackQueen)
        square03.image = blackQueen
        square03.grid(row = 0, column = 3)

        square04 = Button(self.master, image = blackKing)
        square04.image = blackKing
        square04.grid(row = 0, column = 4)

        square05 = Button(self.master, image = blackBishop)
        square05.image = blackBishop
        square05.grid(row = 0, column = 5)

        square06 = Button(self.master, image = blackKnight)
        square06.image = blackKnight
        square06.grid(row = 0, column = 6)

        square07 = Button(self.master, image = blackRook)
        square07.image = blackRook
        square07.grid(row = 0, column = 7)

        square10 = Button(self.master, image = blackPawn)
        square10.image = blackPawn
        square10.grid(row = 1, column = 0)

        square11 = Button(self.master, image = blackPawn)
        square11.image = blackPawn
        square11.grid(row = 1, column = 1)

        square12 = Button(self.master, image = blackPawn)
        square12.image = blackPawn
        square12.grid(row = 1, column = 2)

        square13 = Button(self.master, image = blackPawn)
        square13.image = blackPawn
        square13.grid(row = 1, column = 3)

        square14 = Button(self.master, image = blackPawn)
        square14.image = blackPawn
        square14.grid(row = 1, column = 4)

        square15 = Button(self.master, image = blackPawn)
        square15.image = blackPawn
        square15.grid(row = 1, column = 5)

        square16 = Button(self.master, image = blackPawn)
        square16.image = blackPawn
        square16.grid(row = 1, column = 6)

        square17 = Button(self.master, image = blackPawn)
        square17.image = blackPawn
        square17.grid(row = 1, column = 7)

        square20 = Button(self.master, image = blank)
        square20.image = blank
        square20.grid(row = 2, column = 0)

        square21 = Button(self.master, image = blank)
        square21.image = blank
        square21.grid(row = 2, column = 1)

        square22 = Button(self.master, image = blank)
        square22.image = blank
        square22.grid(row = 2, column = 2)

        square23 = Button(self.master, image = blank)
        square23.image = blank
        square23.grid(row = 2, column = 3)

        square24 = Button(self.master, image = blank)
        square24.image = blank
        square24.grid(row = 2, column = 4)

        square25 = Button(self.master, image = blank)
        square25.image = blank
        square25.grid(row = 2, column = 5)

        square26 = Button(self.master, image = blank)
        square26.image = blank
        square26.grid(row = 2, column = 6)

        square27 = Button(self.master, image = blank)
        square27.image = blank
        square27.grid(row = 2, column = 7)

        square30 = Button(self.master, image = blank)
        square30.image = blank
        square30.grid(row = 3, column = 0)

        square31 = Button(self.master, image = blank)
        square31.image = blank
        square31.grid(row = 3, column = 1)

        square32 = Button(self.master, image = blank)
        square32.image = blank
        square32.grid(row = 3, column = 2)

        square33 = Button(self.master, image = blank)
        square33.image = blank
        square33.grid(row = 3, column = 3)

        square34 = Button(self.master, image = blank)
        square34.image = blank
        square34.grid(row = 3, column = 4)

        square35 = Button(self.master, image = blank)
        square35.image = blank
        square35.grid(row = 3, column = 5)

        square36 = Button(self.master, image = blank)
        square36.image = blank
        square36.grid(row = 3, column = 6)

        square37 = Button(self.master, image = blank)
        square37.image = blank
        square37.grid(row = 3, column = 7)

        square40 = Button(self.master, image = blank)
        square40.image = blank
        square40.grid(row = 4, column = 0)

        square41 = Button(self.master, image = blank)
        square41.image = blank
        square41.grid(row = 4, column = 1)

        square42 = Button(self.master, image = blank)
        square42.image = blank
        square42.grid(row = 4, column = 2)

        square43 = Button(self.master, image = blank)
        square43.image = blank
        square43.grid(row = 4, column = 3)

        square44 = Button(self.master, image = blank)
        square44.image = blank
        square44.grid(row = 4, column = 4)

        square45 = Button(self.master, image = blank)
        square45.image = blank
        square45.grid(row = 4, column = 5)

        square46 = Button(self.master, image = blank)
        square46.image = blank
        square46.grid(row = 4, column = 6)

        square47 = Button(self.master, image = blank)
        square47.image = blank
        square47.grid(row = 4, column = 7)

        square50 = Button(self.master, image = blank)
        square50.image = blank
        square50.grid(row = 5, column = 0)

        square51 = Button(self.master, image = blank)
        square51.image = blank
        square51.grid(row = 5, column = 1)

        square52 = Button(self.master, image = blank)
        square52.image = blank
        square52.grid(row = 5, column = 2)

        square53 = Button(self.master, image = blank)
        square53.image = blank
        square53.grid(row = 5, column = 3)

        square54 = Button(self.master, image = blank)
        square54.image = blank
        square54.grid(row = 5, column = 4)

        square55 = Button(self.master, image = blank)
        square55.image = blank
        square55.grid(row = 5, column = 5)

        square56 = Button(self.master, image = blank)
        square56.image = blank
        square56.grid(row = 5, column = 6)

        square57 = Button(self.master, image = blank)
        square57.image = blank
        square57.grid(row = 5, column = 7)

        square60 = Button(self.master, image = whitePawn)
        square60.image = whitePawn
        square60.grid(row = 6, column = 0)

        square61 = Button(self.master, image = whitePawn)
        square61.image = whitePawn
        square61.grid(row = 6, column = 1)

        square62 = Button(self.master, image = whitePawn)
        square62.image = whitePawn
        square62.grid(row = 6, column = 2)

        square63 = Button(self.master, image = whitePawn)
        square63.image = whitePawn
        square63.grid(row = 6, column = 3)

        square64 = Button(self.master, image = whitePawn)
        square64.image = whitePawn
        square64.grid(row = 6, column = 4)

        square65 = Button(self.master, image = whitePawn)
        square65.image = whitePawn
        square65.grid(row = 6, column = 5)

        square66 = Button(self.master, image = whitePawn)
        square66.image = whitePawn
        square66.grid(row = 6, column = 6)

        square67 = Button(self.master, image = whitePawn)
        square67.image = whitePawn
        square67.grid(row = 6, column = 7)

        square70 = Button(self.master, image = whiteRook)
        square70.image = whiteRook
        square70.grid(row = 7, column = 0)

        square71 = Button(self.master, image = whiteKnight)
        square71.image = whiteKnight
        square71.grid(row = 7, column = 1)

        square72 = Button(self.master, image = whiteBishop)
        square72.image = whiteBishop
        square72.grid(row = 7, column = 2)

        square73 = Button(self.master, image = whiteQueen)
        square73.image = whiteQueen
        square73.grid(row = 7, column = 3)

        square74 = Button(self.master, image = whiteKing)
        square74.image = whiteKing
        square74.grid(row = 7, column = 4)

        square75 = Button(self.master, image = whiteBishop)
        square75.image = whiteBishop
        square75.grid(row = 7, column = 5)

        square76 = Button(self.master, image = whiteKnight)
        square76.image = whiteKnight
        square76.grid(row = 7, column = 6)

        square77 = Button(self.master, image = whiteRook)
        square77.image = whiteRook
        square77.grid(row = 7, column = 7)

        timer1 = Label(self.master, text = "     P1 Time Remaining:   {}:{}     ".format(self.p1Time / 60, str(self.p1Time % 60).zfill(2)))
        timer1.grid(row = 6, column = 8, rowspan = 2)

        timer2 = Label(self.master, text = "     P2 Time Remaining:   {}:{}     ".format(self.p2Time / 60, str(self.p2Time % 60).zfill(2)))
        timer2.grid(row = 0, column = 8, rowspan = 2)

window = Tk()
window.title("Chess Reloaded")
game = newGame(window)
game.setupGUI()
window.mainloop()
