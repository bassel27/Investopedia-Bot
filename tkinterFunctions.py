from tkinter import *
from tkinter import messagebox
from functions import *
from Stock import *
from Scraping import *

def atExit(root):
    def exitMessage():
        response = messagebox.askyesno("Confirmation", "Are you sure you want to exit?")
        if response == True:
            try:
                os.remove('currentStock.png')
            except:
                pass
            root.destroy()

        else:
            pass

    root.protocol('WM_DELETE_WINDOW', exitMessage)

def intro(root):
    root.title("Trading Core")
    global title
    title = Label (root, text = "Trading Core")    #to create anything in tkinter, you have to do it in 2 steps: define the thing and put it on the screen
    title.pack()    #putting the label on the screen
    global frameInput 
    frameInput = LabelFrame(root)
    frameInput.pack()
    root.iconbitmap(r'C:\Users\Bassel Attia\Documents\Trading Core\money_icon.ico')      #because it's in the same directory as your program, you don't need to type the whole address



def enableButtonNext(root):

    def clickNext():
        try:
            if checkButtonRiskVar:
                risk = 2

            else:
                risk = entryRisk.get()

            frameInput.destroy()
            frameAccAndCash.destroy()
        except:
            messagebox.showerror("Error", "Wrong entry. Please try again!")
            frameInput.destroy()
            frameInputAll(root)

        isChanceDefault = bool(checkButtonChanceVar.get())

        if isChanceDefault:
            winChance =0.9
        else:
            winChance = None

        stock = []
        stock.append(Stock())
        stock[0].frameInputStock(root, winChance, stock, risk, account)
            


    buttonNext = Button(frameInput, text = "Next!", width = 20, height = 2, fg = 'green', bg = 'white', command= clickNext)   #note that the function name is mentioned without
    buttonNext.grid(row = 2, column = 1)
    
    

def checkButtonStuff():
    def isCheckButtonChecked():
            if checkButtonRiskVar.get():
                labelRisk.grid_forget()
                entryRisk.grid_forget()
            else:
                labelRisk.grid( row = 0, column = 2)
                entryRisk.grid(row = 0, column = 3)
                

    global checkButtonRiskVar
    checkButtonRiskVar = IntVar(value = 1)
    checkButtonIsRiskDefault = Checkbutton(frameInput, variable = checkButtonRiskVar, command=isCheckButtonChecked, activeforeground='green')
    Label(frameInput, text="Make risk = 2%?").grid(row= 0, column = 0, sticky = 'w')
    checkButtonIsRiskDefault.grid(row = 0, column = 1)

    labelRisk = Label(frameInput, text = "Enter risk percentage")
    global entryRisk
    entryRisk = Entry(frameInput, borderwidth = 3)
    
    global checkButtonChanceVar
    checkButtonChanceVar = IntVar(value = 1)
    checkButtonIsChanceDefault = Checkbutton(frameInput, variable = checkButtonChanceVar, command=isCheckButtonChecked, activeforeground='green')
    Label(frameInput, text="Make chance = 0.9?").grid(row=1, column = 0, sticky = 'w')
    checkButtonIsChanceDefault.grid(row = 1, column = 1)




def  frameAccAndCash(root):
    global account, cash
    scraping = Scraping()
    scraping.openWebDriver()
    scraping.login()
    account, cash = scraping.scrapeAccCash()
    scraping.quitDriver()
    global frameAccAndCash
    frameAccAndCash = LabelFrame(root)
    frameAccAndCash.pack()
    Label(frameAccAndCash, fg = 'green', text = ("Account value = " + str(account)+ " $"+ "   -   " + "cash = "+ str(cash) + " $")).grid(column =1 , row =0)



def frameInputAll(root):
    intro(root)
    checkButtonStuff()
    enableButtonNext(root)
