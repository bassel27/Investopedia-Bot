from typing import Counter
from yahoo_fin import stock_info as si
from tkinter import *
from tkinter import messagebox
import tkinterFunctions 
import functions
from Scraping import *
from Scrollbar import * 
import threading
import time
import tkinterFunctions


def organizeOutput(root, n, stock): 
    counter = 0
    row = 3
    column = 0
    while counter != n:
        stock[counter].frameOutput(root, row, column, counter, stock)
        counter += 1
        if column == 0:
            column = 1
        elif column == 1:
            column =0
            row += 1


counter = 0
scraping = Scraping()
threads = []

class Stock:


    def takeScreenshot (self):
        scraping.openWebDriver()
        scraping.getFinviz(self.ticker)
        scraping.takeScreenshot()
        scraping.cropImage()
        scraping.resizeImage()
        scraping.quitDriver()
        self.graph = PhotoImage(file='currentStock.png')    
        

    def frameInputStock(self, root, winChance, stock, risk, account):
        frameInput = LabelFrame(root)
        frameInput.pack()
        global counter
        Label(frameInput, text = functions.returnOrdinal(counter+1) + " stock").grid(row =0, column = 1)

        Label(frameInput, text = "Enter the ticker").grid(row =1, column =0, sticky = 'w')
        entryTicker = Entry(frameInput, borderwidth = 5)
        entryTicker.grid(row =1, column =1)

        Label(frameInput, text = "Enter your target price").grid(row = 2, column =0, sticky = 'w')
        entryTargetPrice = Entry(frameInput, borderwidth=5)
        entryTargetPrice.grid(row =2, column = 1)

        Label(frameInput, text = "Enter your stop loss price").grid(row = 3, column =0, sticky = 'w')
        entrystopLoss = Entry(frameInput, borderwidth=5)
        entrystopLoss.grid(row =3, column = 1)
        
        wasWinChanceNull = False
        if(winChance is None):
            Label(frameInput, text = "Enter win chance").grid(row = 4, column = 0, sticky = 'w')
            entryWinChance = Entry(frameInput, borderwidth = 5)
            entryWinChance.grid(row = 4, column = 1)
            wasWinChanceNull = True
    
        def clickNextStock(isFinished = False):
            try:
                #assign to attributes
                self.ticker = (entryTicker.get()).upper()
                self.stopLoss = float(entrystopLoss.get())
                self.targetPrice = float(entryTargetPrice.get())
                self.currentPrice = round(si.get_live_price(self.ticker), 2)
                self.currentPrice = self.currentPrice.item()
                self.currentPrice = self.currentPrice
                
                global counter

                if isFinished == False:
                    thread = threading.Thread(target = stock[counter].takeScreenshot)
                    thread.start()
                    global threads
                    threads.append(thread)
                else:
                    stock[counter].takeScreenshot()
                    
                nonlocal winChance
                if winChance is None:
                    winChance = float(entryWinChance.get())

                self.winChance = winChance
                self.lossChance = 1 - self.winChance
                self.expectancy =100 * abs(((self.targetPrice - self.currentPrice) / self.currentPrice)) * self.winChance - abs(((self.currentPrice - self.stopLoss) / self.currentPrice)) * self.lossChance
                self.quantity = int((account * (risk / 100)) / abs((self.currentPrice - self.stopLoss)))
                
                
                self.cost = round(self.currentPrice * self.quantity, 2)
                self.expectedProfit = round(abs(self.currentPrice - self.targetPrice) * self.quantity, 2)
                if self.currentPrice > self.targetPrice:
                    self.isLong = False
                else:
                    self.isLong = True

                if self.isLong == True:
                    self.transaction = "Buy"
                else:
                    self.transaction = "Sell Short"
                frameInput.destroy()
                
                if(wasWinChanceNull == True):
                    winChance = None

                counter += 1
                n = counter

                if isFinished == True:
                    stock.sort(key=lambda x: x.expectancy, reverse=True)
                    Label(root, text = "Results       ").pack()
                    
                    global mainFrame
                    mainFrame = VerticalScrolledFrame(root, width=1700, borderwidth=2, relief=SUNKEN, background="light gray")
                    mainFrame.pack(fill="both", expand=True)
                    organizeOutput(root, n, stock)
                else:
                    stock.append(Stock())
                    stock[counter].frameInputStock(root, winChance, stock, risk, account)
            
            except:
                if wasWinChanceNull == True:
                    winChance = None
                messagebox.showerror("Error", "Wrong entry. Please try again!")
                frameInput.destroy()
                stock[counter].frameInputStock(root, winChance, stock, risk, account)
            
            

        
        def checkEntry(event):
            nonlocal wasWinChanceNull
            if wasWinChanceNull == True:
                if entrystopLoss.get() and entryTargetPrice.get() and entryWinChance.get():
                    buttonNextStock.config(state=NORMAL)
                    buttonFinish.config(state=NORMAL)
                else:
                    buttonNextStock.config(state=DISABLED)
                    buttonFinish.config(state=DISABLED)
            else:
                if entrystopLoss.get() and entryTargetPrice.get():
                    buttonNextStock.config(state=NORMAL)
                    buttonFinish.config(state=NORMAL)
                else:
                    buttonNextStock.config(state=DISABLED)
                    buttonFinish.config(state=DISABLED)
            

        entryTargetPrice.bind('<KeyRelease>',checkEntry)         
        entrystopLoss.bind('<KeyRelease>', checkEntry)
        if wasWinChanceNull == True:
            entryWinChance.bind('<KeyRelease>', checkEntry)  

        
        buttonNextStock = Button(frameInput, text = "Onto the next stock", fg='green', command = clickNextStock, state = DISABLED)
        buttonNextStock.grid(row = 5, column =1)
        buttonFinish = Button(frameInput, text = "Finish", fg = 'green', command = lambda: clickNextStock(isFinished = True), state=DISABLED)
        buttonFinish.grid(row = 6, column =1)
        
            



    def frameOutput(self, root, rowNo, columnNo, counter, stock):
        def setEntryLimitPrice (entryLimitPrice):
            entryLimitPrice.grid(row = 2, column =0)
            if self.isLong == True:
                entryLimitPrice.insert(0, self.currentPrice + 0.02)
            else:
                entryLimitPrice.insert(0, self.currentPrice - 0.02)

        frameOutput = LabelFrame(mainFrame) 
        frameOutput.grid(row = rowNo, column = columnNo)
        Label(frameOutput, text = str(counter + 1) + ". " + self.ticker).grid(row = 0, column = 0, sticky = 'w')
        Label(frameOutput, text = f"Expectancy: {self.expectancy:.2f}%").grid(row = 1, column = 0, sticky = 'w')
        
        Label(frameOutput, text = "                          order: ").grid(row = 2, column = 0, sticky = 'w' )
        entryLimitPrice = Entry(frameOutput)
        setEntryLimitPrice(entryLimitPrice)
        var = StringVar()
        var.set("Limit")
        orderTypeDropDown = OptionMenu(frameOutput, var, "Limit", "Market")
        orderTypeDropDown.grid(row = 2, column = 0, sticky = 'w')        
        def dropDownFunction(*args):
            if var.get() == "Limit":
                setEntryLimitPrice(entryLimitPrice)        
            else:
                entryLimitPrice.delete(0, 'end')
                entryLimitPrice.grid_forget()
        var.trace('w', dropDownFunction)


        Label(frameOutput, text = "Stop loss: " + str(self.stopLoss) + " $").grid(row = 3, column = 0, sticky = 'w')
        Label(frameOutput, text = "Expected profit: " + str(self.expectedProfit)+ " $").grid(row = 4, column =0, sticky = 'w')
        if self.isLong == True:
            labelSharesLonged = Label(frameOutput, text = "Shares longed: " + str(self.quantity))
            labelSharesLonged.grid(row = 5, column = 0, sticky = 'w')
            labelCost= Label(frameOutput, text = "Total cost: " + str(self.cost) + " $")
            labelCost.grid(row = 6, column = 0, sticky = 'w')
        else:
            labelSharesShorted = Label(frameOutput, text = "Shares shorted: " + str(self.quantity))
            labelSharesShorted.grid(row = 5, column = 0, sticky = 'w')
        
        screenshotLabel = Label(frameOutput, image = self.graph)
        screenshotLabel.img = self.graph
        screenshotLabel.grid(row = 7, column = 0)

        def isCheckButtonChecked():
            if checkButtonExecuteVar.get():
                orderType = var.get()
                try:
                    limitPrice = entryLimitPrice.get()
                except:
                    limitPrice = 0

                scraping.openWebDriver()
                scraping.login()
                maxQuantity = scraping.executeOrder(self.ticker, self.transaction, self.quantity, orderType, limitPrice)
                scraping.quitDriver()

                if self.quantity > maxQuantity:
                    self.quantity = maxQuantity
                    self.cost = round(self.currentPrice * self.quantity, 2)

                    if self.isLong == True:
                        labelCost.destroy()
                        labelSharesLonged.destroy()
                        Label(frameOutput, text = "Shares longed: " + str(self.quantity) + "  (The number of shares was exceeding Investopedia's maximum for this stock)").grid(row = 5, column = 0, sticky = 'w')
                        Label(frameOutput, text = "Total cost: " + str(self.cost) + " $").grid(row = 6, column = 0, sticky = 'w')
                    else:
                        labelSharesShorted.destroy()
                        Label(frameOutput, text = "Shares shorted: " + str(self.quantity)).grid(row = 5, column = 0, sticky = 'w')
                    
                stock[counter-1].addNotionRow()

                
        
        Label(frameOutput, text = "Execute trade?").grid(row = 8, column = 0, sticky = 'w')
        checkButtonExecuteVar = IntVar()
        checkButtonExecute = Checkbutton(frameOutput, variable = checkButtonExecuteVar, command = isCheckButtonChecked, activeforeground='green')
        checkButtonExecute.grid(row = 8, column = 1)
        counter +=1


    def addNotionRow(self):
        from notion.client import NotionClient
        from datetime import date

        token = '67b7199ace904372cbae57a459653444771919d681a4e3aac217ef01dacfba380a7c5c378bfb713cd31472ec4de18484a9a6c3a7fe2d86f292459b1d1d6d27cea36cf5de4a7aa62318ee87084e55'
        client = NotionClient(token_v2=token)
        listUrl = 'https://www.notion.so/19338d10174b463cb6ce4fba6e82c18a?v=5237d4d9360d4deaaf9b79e59ae05edb'
        collectionView = client.get_collection_view(listUrl)
        if tkinterFunctions.cash>= self.cost: #error
            newRow = collectionView.collection.add_row()
            newRow.Ticker = self.ticker # to capitalize the string
            newRow.Quantity = self.quantity
            newRow.Filled_in_by_python = True
            newRow.Stop_loss = str(self.stopLoss)
            if self.isLong == True:
                newRow.Strategy = "Long"
                newRow.Date_Bought = date.today()
                newRow.Buy_Price = self.currentPrice
            else:
                newRow.Strategy = "Short"
                newRow.Date_Sold = date.today()
                newRow.Selling_Price = self.targetPrice