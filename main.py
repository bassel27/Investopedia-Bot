from tkinter import *
from tkinterFunctions import *
from Stock import *

root = Tk() #creating the root widget which the empty window

atExit(root)
frameInputAll(root)

frameAccAndCash(root)

root.mainloop() #program loop