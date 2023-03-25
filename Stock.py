from typing import Counter
from yahoo_fin import stock_info as si
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading, functions

import tkinterFunctions 
from Scraping import *
from Scrollbar import * 

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
        entryTicker = ttk.Entry(frameInput)
        entryTicker.grid(row =1, column =1)

        Label(frameInput, text = "Enter your target price").grid(row = 2, column =0, sticky = 'w')
        entryTargetPrice = ttk.Entry(frameInput)
        entryTargetPrice.grid(row =2, column = 1)

        Label(frameInput, text = "Enter your stop loss price").grid(row = 3, column =0, sticky = 'w')
        entrystopLoss = ttk.Entry(frameInput)
        entrystopLoss.grid(row =3, column = 1)
        
        wasWinChanceNull = False
        if(winChance is None):
            Label(frameInput, text = "Enter win chance").grid(row = 4, column = 0, sticky = 'w')
            entryWinChance = ttk.Entry(frameInput)
            entryWinChance.grid(row = 4, column = 1)
            wasWinChanceNull = True
    
        def clickNextStock(isFinished = False):
            try:
                #assign to attributes
                self.ticker = (entryTicker.get()).upper()
                self.stopLoss = float(entrystopLoss.get())
                self.targetPrice = float(entryTargetPrice.get())
                self.currentPrice = float(si.get_live_price(self.ticker))
                print(type(self.currentPrice))
                
                global counter
                    
                nonlocal winChance
                if winChance is None:
                    winChance = float(entryWinChance.get())

                self.winChance = winChance
                self.lossChance = 1 - self.winChance
                self.expectancy =100 * abs(((self.targetPrice - self.currentPrice) / self.currentPrice)) * self.winChance - abs(((self.currentPrice - self.stopLoss) / self.currentPrice)) * self.lossChance
                self.quantity = int((account * (risk / 100)) / abs((self.currentPrice - self.stopLoss)))
                
                
                self.cost = self.currentPrice * self.quantity
                self.expectedProfit = abs(self.currentPrice - self.targetPrice) * self.quantity
                if self.currentPrice > self.targetPrice:
                    self.isLong = False
                else:
                    self.isLong = True

                if self.isLong == True:
                    self.transaction = "Buy"
                else:
                    self.transaction = "Short"
                frameInput.destroy()
                
                if(wasWinChanceNull == True):
                    winChance = None

                counter += 1
                n = counter

                if isFinished == True:
                    global threads
                    stock[counter-1].takeScreenshot()
                    stock.sort(key=lambda x: x.expectancy, reverse=True)
                    Label(root, text = "Results       ").pack()
                    
                    global mainFrame
                    mainFrame = VerticalScrolledFrame(root, width=1700, borderwidth=2, relief=SUNKEN, background="light gray")
                    mainFrame.pack(fill="both", expand=True)
                    organizeOutput(root, n, stock)
                else:
                    thread = threading.Thread(target = stock[counter-1].takeScreenshot)
                    thread.start()
                    threads.append(thread)

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

        buttonNextStock = ttk.Button(frameInput, text = "Onto the next stock", command = clickNextStock, state = DISABLED)
        buttonNextStock.grid(row = 5, column =1)
        buttonFinish = ttk.Button(frameInput, text = "Finish", command = lambda: clickNextStock(isFinished = True), state=DISABLED)
        buttonFinish.grid(row = 6, column =1)
        
    def frameOutput(self, root, rowNo, columnNo, counter, stock):
        def setEntryLimitPrice (entryLimitPrice):
            entryLimitPrice.delete(0, 'end')
            entryLimitPrice.grid(row = 2, column =0)
            if self.isLong == True:
                entryLimitPrice.insert(0, round(self.currentPrice + 0.02, 2))
            else:
                entryLimitPrice.insert(0, round(self.currentPrice - 0.02, 2))

        frameOutput = LabelFrame(mainFrame) 
        frameOutput.grid(row = rowNo, column = columnNo)
        Label(frameOutput, text = str(counter + 1) + ". " + self.ticker).grid(row = 0, column = 0, sticky = 'w')
        Label(frameOutput, text = f"Expectancy: {self.expectancy:.2f}%").grid(row = 1, column = 0, sticky = 'w')
        
        Label(frameOutput, text = "                         order: ").grid(row = 2, column = 0, sticky = 'w' )
        entryLimitPrice = ttk.Entry(frameOutput)
        setEntryLimitPrice(entryLimitPrice)
        var = StringVar()
        var.set("Limit")
        options = ["Limit", "Market"]
        orderTypeDropDown = ttk.OptionMenu(frameOutput, var, options[0], *options )
        orderTypeDropDown.grid(row = 2, column = 0, sticky = 'w')  
              
        def dropDownFunction(*args):
            if var.get() == options[0]:
                setEntryLimitPrice(entryLimitPrice)        
            else:
                entryLimitPrice.delete(0, 'end')
                entryLimitPrice.grid_forget()
        var.trace('w', dropDownFunction)

        Label(frameOutput, text = "Stop loss: " + str(self.stopLoss) + " $").grid(row = 3, column = 0, sticky = 'w')
        Label(frameOutput, text = "Expected profit: " + str(round(self.expectedProfit, 2))+ " $").grid(row = 4, column =0, sticky = 'w')
        
        if self.isLong == True:
            labelSharesLonged = Label(frameOutput, text = "Shares longed: " + str(self.quantity))
            labelSharesLonged.grid(row = 5, column = 0, sticky = 'w')
            labelCost= Label(frameOutput, text = "Total cost: " + str(round(self.cost, 2)) + " $")
            labelCost.grid(row = 6, column = 0, sticky = 'w')
        else:
            labelSharesShorted = Label(frameOutput, text = "Shares shorted: " + str(self.quantity))
            labelSharesShorted.grid(row = 5, column = 0, sticky = 'w')
            Label(frameOutput, text = ' ').grid(row = 6, column = 0)
        
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

                
                
                maxQuantity = scraping.executeOrder(self.ticker, self.transaction, self.quantity, orderType, limitPrice)
                scraping.quitDriver()

                if self.quantity > maxQuantity:
                    self.quantity = maxQuantity
                    self.cost = self.currentPrice * self.quantity

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
        checkButtonExecute = ttk.Checkbutton(frameOutput, variable = checkButtonExecuteVar, command = isCheckButtonChecked)
        checkButtonExecute.grid(row = 8, column = 1)

    # def addNotionRow(self):
    #     from notion.client import NotionClient
    #     from datetime import date

    #     token = config.token
    #     client = NotionClient(token_v2=token)
    #     listUrl = 'https://www.notion.so/19338d10174b463cb6ce4fba6e82c18a?v=5237d4d9360d4deaaf9b79e59ae05edb'
    #     collectionView = client.get_collection_view(listUrl)
    #     if tkinterFunctions.cash>= self.cost: #error
    #         newRow = collectionView.collection.add_row()
    #         newRow.Ticker = self.ticker # to capitalize the string
    #         newRow.Quantity = self.quantity
    #         newRow.Filled_in_by_python = True
    #         newRow.Stop_loss = str(self.stopLoss)
    #         newRow.Expected_profit = str(round(self.expectedProfit, 2))
    #         if self.isLong == True:
    #             newRow.Strategy = "Long"
    #             newRow.Date_Bought = date.today()
    #             newRow.Buy_Price = self.currentPrice
    #         else:
    #             newRow.Strategy = "Short"
    #             newRow.Date_Sold = date.today()
    #             newRow.Selling_Price = self.targetPrice