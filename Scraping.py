from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os
import creds
import time

class Scraping:
    def openWebDriver(self):
        ublockPath = r'C:\Users\Bassel Attia\Documents\Trading Core\1.37.2_0'
        chromeOptions = Options()
        chromeOptions.add_argument("--log-level=3")
        # chromeOptions.add_argument('--headless')
        # chromeOptions.add_argument('--log-level=1')
        chromeOptions.add_argument('load-extension=' + ublockPath)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)     #to create the instance of chrome WebDriver
        #self.driver.set_window_position(-10000,0)
        
    def getFinviz(self, ticker):
        self.driver.get('https://finviz.com/quote.ashx?t=' + ticker)

    def takeScreenshot(self):
        self.driver.get_screenshot_as_file('currentStock.png')
        self.image = Image.open('currentStock.png')
        
    def cropImage(self):
        area = (20, 290, 1250, 800)
        croppedImage=self.image.crop(area)
        os.remove('currentStock.png')
        croppedImage.save('currentStock.png')
        self.image = Image.open('currentStock.png')

    def resizeImage(self):
        newHeight = 300
        newWidth = int(newHeight / self.image.height * self.image.width)
        resizedImage = self.image.resize((newWidth, newHeight))
        os.remove('currentStock.png')
        resizedImage.save('currentStock.png')
        self.image = Image.open('currentStock.png')
        self.image.close()
        
    
    def quitDriver(self):
        self.driver.quit()   


    def login (self):
        self.driver.get(r'https://www.investopedia.com/auth/realms/investopedia/protocol/openid-connect/auth?scope=email&state=efce4bc80385e2710878f031749d464a&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fwww.investopedia.com%2Fsimulator%2Fhome.aspx&client_id=inv-simulator-conf')

        username = self.driver.find_element_by_id('username')
        password = self.driver.find_element_by_id('password')

        username.send_keys(creds.username)
        password.send_keys(creds.password)

        buttonLogin = self.driver.find_element_by_id('login')
        buttonLogin.click()

        self.driver.implicitly_wait(10)

    def scrapeAccCash(self):
        tradeUrl = 'https://www.investopedia.com/simulator/trade/tradestock.aspx'
        self.driver.get(tradeUrl)
        accBuyingCash = self.driver.find_elements_by_class_name('num')  #or 'value'. They are  different calsses
        account = (accBuyingCash[0].text).replace('$', '').replace(',', '')
        cash =  (accBuyingCash[2].text).replace('$', '').replace(',', '')
        return float(account), float(cash)

    def getTradePage(self):
        tradeUrl = 'https://www.investopedia.com/simulator/trade/tradestock.aspx'
        self.driver.get(tradeUrl)

    def acceptCookies (self):
        self.driver.implicitly_wait(0.5)
        try:
            acceptCookie = self.driver.find_element_by_id('gdpr-notification-banner__btn-close_1-0')
            acceptCookie.click()
        except:
            pass
        self.driver.implicitly_wait(10)
    

    def setStock (self, ticker):
        stockSymbolTxtBox = self.driver.find_element_by_id('symbolTextbox')
        stockSymbolTxtBox.send_keys(ticker)
        selectSymbol= self.driver.find_element_by_id('symbolTextbox_mi_1')
        selectSymbol.click()

    def setTransaction (self, transaction):
        orderDict = {
            'Buy': 0,
            'Sell' : 1,
            'Sell Short' : 2,
            'Buy to Cover' : 3        
        }
        orderNumber = orderDict.get(transaction)
        transactionList = self.driver.find_element_by_id('transactionTypeDropDown')
        selectItem = Select(transactionList)
        selectItem.select_by_index(orderNumber)

    
    def getMaxQuantity (self):
        showMax = self.driver.find_element_by_id('showMaxLink')  
        showMax.click()
        
        time.sleep(0.5)
        maxQuantityText = self.driver.find_element_by_id('limitationLabel')
        maxQuantity = 0
        for word in (maxQuantityText.text).split():
            if word.isdigit():
                maxQuantity = int(word)

        return maxQuantity

    def setQuantity (self, quantity):
        qunatityTxtBox = self.driver.find_element_by_id('quantityTextbox')
        qunatityTxtBox.send_keys(quantity)

    def setOrderType (self, orderType, limitPrice):
        if(orderType == "Limit"):
            limitOrderSelection = self.driver.find_element_by_id('limitRadioButton')
            limitOrderSelection.click()
            limitPriceTxtBox = self.driver.find_element_by_id('limitPriceTextBox')
            limitPriceTxtBox.send_keys(str(limitPrice))
    
    def setSendEmail (self, sendEmail):
        if sendEmail == False:
            sendConfirmationEmail = self.driver.find_element_by_id('sendConfirmationEmailCheckBox')
            sendConfirmationEmail.click()

    def previewAndSubmit (self):
        previewOrder = self.driver.find_element_by_id('previewButton')
        previewOrder.click()
        
        submitOrder = self.driver.find_element_by_id('submitOrder')
        submitOrder.click()

    def executeOrder (self, ticker , transaction, quantity, orderType, limitPrice, sendEmail = True):
        self.getTradePage()
        self.acceptCookies()
        self.setStock(ticker)
        self.setTransaction(transaction)
        self.setQuantity(quantity)
        maxQuantity = self.getMaxQuantity()
        self.setOrderType(orderType, limitPrice)
        self.setSendEmail(sendEmail)
        self.previewAndSubmit()
        return maxQuantity


