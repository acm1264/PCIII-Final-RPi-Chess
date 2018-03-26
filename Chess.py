from Tkinter import *

class newGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

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
        
        square00 = Label(self.master, image = blackRook)
        square00.image = blackRook
        square00.grid(row = 0, column = 0)

        square01 = Label(self.master, image = blackKnight)
        square01.image = blackKnight
        square01.grid(row = 0, column = 1)

        square02 = Label(self.master, image = blackBishop)
        square02.image = blackBishop
        square02.grid(row = 0, column = 2)

        square03 = Label(self.master, image = blackQueen)
        square03.image = blackQueen
        square03.grid(row = 0, column = 3)

        square04 = Label(self.master, image = blackKing)
        square04.image = blackKing
        square04.grid(row = 0, column = 4)

        square05 = Label(self.master, image = blackBishop)
        square05.image = blackBishop
        square05.grid(row = 0, column = 5)

        square06 = Label(self.master, image = blackKnight)
        square06.image = blackKnight
        square06.grid(row = 0, column = 6)

        square07 = Label(self.master, image = blackRook)
        square07.image = blackRook
        square07.grid(row = 0, column = 7)

        square10 = Label(self.master, image = blackPawn)
        square10.image = blackPawn
        square10.grid(row = 1, column = 0)

        square11 = Label(self.master, image = blackPawn)
        square11.image = blackPawn
        square11.grid(row = 1, column = 1)

        square12 = Label(self.master, image = blackPawn)
        square12.image = blackPawn
        square12.grid(row = 1, column = 2)

        square13 = Label(self.master, image = blackPawn)
        square13.image = blackPawn
        square13.grid(row = 1, column = 3)

        square14 = Label(self.master, image = blackPawn)
        square14.image = blackPawn
        square14.grid(row = 1, column = 4)

        square15 = Label(self.master, image = blackPawn)
        square15.image = blackPawn
        square15.grid(row = 1, column = 5)

        square16 = Label(self.master, image = blackPawn)
        square16.image = blackPawn
        square16.grid(row = 1, column = 6)

        square17 = Label(self.master, image = blackPawn)
        square17.image = blackPawn
        square17.grid(row = 1, column = 7)

        square20 = Label(self.master, image = blank)
        square20.image = blank
        square20.grid(row = 2, column = 0)

        square21 = Label(self.master, image = blank)
        square21.image = blank
        square21.grid(row = 2, column = 1)

        square22 = Label(self.master, image = blank)
        square22.image = blank
        square22.grid(row = 2, column = 2)

        square23 = Label(self.master, image = blank)
        square23.image = blank
        square23.grid(row = 2, column = 3)

        square24 = Label(self.master, image = blank)
        square24.image = blank
        square24.grid(row = 2, column = 4)

        square25 = Label(self.master, image = blank)
        square25.image = blank
        square25.grid(row = 2, column = 5)

        square26 = Label(self.master, image = blank)
        square26.image = blank
        square26.grid(row = 2, column = 6)

        square27 = Label(self.master, image = blank)
        square27.image = blank
        square27.grid(row = 2, column = 7)

        square30 = Label(self.master, image = blank)
        square30.image = blank
        square30.grid(row = 3, column = 0)

        square31 = Label(self.master, image = blank)
        square31.image = blank
        square31.grid(row = 3, column = 1)

        square32 = Label(self.master, image = blank)
        square32.image = blank
        square32.grid(row = 3, column = 2)

        square33 = Label(self.master, image = blank)
        square33.image = blank
        square33.grid(row = 3, column = 3)

        square34 = Label(self.master, image = blank)
        square34.image = blank
        square34.grid(row = 3, column = 4)

        square35 = Label(self.master, image = blank)
        square35.image = blank
        square35.grid(row = 3, column = 5)

        square36 = Label(self.master, image = blank)
        square36.image = blank
        square36.grid(row = 3, column = 6)

        square37 = Label(self.master, image = blank)
        square37.image = blank
        square37.grid(row = 3, column = 7)

        square40 = Label(self.master, image = blank)
        square40.image = blank
        square40.grid(row = 4, column = 0)

        square41 = Label(self.master, image = blank)
        square41.image = blank
        square41.grid(row = 4, column = 1)

        square42 = Label(self.master, image = blank)
        square42.image = blank
        square42.grid(row = 4, column = 2)

        square43 = Label(self.master, image = blank)
        square43.image = blank
        square43.grid(row = 4, column = 3)

        square44 = Label(self.master, image = blank)
        square44.image = blank
        square44.grid(row = 4, column = 4)

        square45 = Label(self.master, image = blank)
        square45.image = blank
        square45.grid(row = 4, column = 5)

        square46 = Label(self.master, image = blank)
        square46.image = blank
        square46.grid(row = 4, column = 6)

        square47 = Label(self.master, image = blank)
        square47.image = blank
        square47.grid(row = 4, column = 7)

        square50 = Label(self.master, image = blank)
        square50.image = blank
        square50.grid(row = 5, column = 0)

        square51 = Label(self.master, image = blank)
        square51.image = blank
        square51.grid(row = 5, column = 1)

        square52 = Label(self.master, image = blank)
        square52.image = blank
        square52.grid(row = 5, column = 2)

        square53 = Label(self.master, image = blank)
        square53.image = blank
        square53.grid(row = 5, column = 3)

        square54 = Label(self.master, image = blank)
        square54.image = blank
        square54.grid(row = 5, column = 4)

        square55 = Label(self.master, image = blank)
        square55.image = blank
        square55.grid(row = 5, column = 5)

        square56 = Label(self.master, image = blank)
        square56.image = blank
        square56.grid(row = 5, column = 6)

        square57 = Label(self.master, image = blank)
        square57.image = blank
        square57.grid(row = 5, column = 7)

        square60 = Label(self.master, image = whitePawn)
        square60.image = whitePawn
        square60.grid(row = 6, column = 0)

        square61 = Label(self.master, image = whitePawn)
        square61.image = whitePawn
        square61.grid(row = 6, column = 1)

        square62 = Label(self.master, image = whitePawn)
        square62.image = whitePawn
        square62.grid(row = 6, column = 2)

        square63 = Label(self.master, image = whitePawn)
        square63.image = whitePawn
        square63.grid(row = 6, column = 3)

        square64 = Label(self.master, image = whitePawn)
        square64.image = whitePawn
        square64.grid(row = 6, column = 4)

        square65 = Label(self.master, image = whitePawn)
        square65.image = whitePawn
        square65.grid(row = 6, column = 5)

        square66 = Label(self.master, image = whitePawn)
        square66.image = whitePawn
        square66.grid(row = 6, column = 6)

        square67 = Label(self.master, image = whitePawn)
        square67.image = whitePawn
        square67.grid(row = 6, column = 7)

        square70 = Label(self.master, image = whiteRook)
        square70.image = whiteRook
        square70.grid(row = 7, column = 0)

        square71 = Label(self.master, image = whiteKnight)
        square71.image = whiteKnight
        square71.grid(row = 7, column = 1)

        square72 = Label(self.master, image = whiteBishop)
        square72.image = whiteBishop
        square72.grid(row = 7, column = 2)

        square73 = Label(self.master, image = whiteQueen)
        square73.image = whiteQueen
        square73.grid(row = 7, column = 3)

        square74 = Label(self.master, image = whiteKing)
        square74.image = whiteKing
        square74.grid(row = 7, column = 4)

        square75 = Label(self.master, image = whiteBishop)
        square75.image = whiteBishop
        square75.grid(row = 7, column = 5)

        square76 = Label(self.master, image = whiteKnight)
        square76.image = whiteKnight
        square76.grid(row = 7, column = 6)

        square77 = Label(self.master, image = whiteRook)
        square77.image = whiteRook
        square77.grid(row = 7, column = 7)

window = Tk()
window.title("Chess Reloaded")
game = newGame(window)
game.setupGUI()
window.mainloop()
