import tkinter
from App import MainWindow

# main program

root = tkinter.Tk()     # creating root. controls the whole tkinter structure
app = MainWindow(root)  # main window object
app.mainloop()          # running mainloop. Updates tkinter