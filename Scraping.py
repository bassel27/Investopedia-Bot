from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os, time
import threading
from selenium.webdriver.common.by import By
import config
from selenium.webdriver.support import expected_conditions as EC

class Scraping:
    def openWebDriver(self):
        chromeOptions = Options()
        chromeOptions.add_argument("--log-level=3")
        # chromeOptions.add_argument('--headless')
        # chromeOptions.add_argument('--log-level=1')
        chromeOptions.add_extension('ublock_origin.crx')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)     #to create the instance of chrome WebDriver
        # self.driver.set_window_position(-10000,0)
        
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


    def login(self):
        self.driver.get(r'https://www.investopedia.com/simulator/home.aspx')
        self.driver.implicitly_wait(10)
        #implement threading here .....................................................
        username = self.driver.find_element(By.ID, 'username')
        username.send_keys(config.INVESTOPEDIA_EMAIL)
        time.sleep(0.5)
        
        self.driver.find_element(By.ID, 'password').send_keys(config.INVESTOPEDIA_PASSW)
        time.sleep(0.5)
        
        self.driver.find_element(By.ID, 'login').click()
        try:
            self.getTradePage()
        except:
            self.login()
    
    def getTradePage(self):
        self.driver.find_element(By.XPATH, '//a[@class="text-h6 white--text pl-8 pr-8 v-tab"]').click()

    def scrapeAccCash(self):   
        time.sleep(2)     
        account = self.driver.find_element(By.XPATH, '//div[@data-cy="account-value"]').text
        cash = self.driver.find_element(By.XPATH, '//div[@data-cy="cash"]').text
        account = account.replace('$', '').replace(',', '')
        cash =  cash.replace('$', '').replace(',', '')
        return float(account), float(cash)
        
    
    def setStock(self, ticker):
        self.driver.find_element(By.XPATH,'//input[@placeholder="Look up Symbol/Company Name"]').send_keys(ticker)
        self.driver.find_element(By.XPATH, '//span[@data-cy="symbol-description"]').click()

    def setTransaction(self, transaction):
        self.driver.find_element(By.CLASS_NAME, 'v-select__selections').click()
        self.driver.find_element(By.XPATH, "//*[text()='" + transaction + "']").click()

    def removePopup(self):
        self.driver.find_element(By.XPATH, '//span[@style="color: rgb(255, 255, 255);"]').click()

    def getMaxQuantity(self):
        self.driver.find_element(By.XPATH, '(//span[@class="v-btn__content"])[7]').click()
        quantityEntry = self.driver.find_element(By.XPATH, '//input[@data-cy="quantity-input"]')
        time.sleep(2)
        maxQuantity = quantityEntry.get_attribute("value")
        return float(maxQuantity)


    def setQuantity(self, quantity):
        self.driver.find_element(By.XPATH, '//input[@data-cy="quantity-input"]').send_keys(quantity)

    def setOrderType(self, orderType, limitPrice = 0):
        self.driver.find_element(By.XPATH, '(//div[@class="v-select__selections"])[2]').click()
    

        self.driver.find_element(By.XPATH, "//*[text()='" + orderType + "']").click()
        self.driver.find_element(By.XPATH, '//input[@data-cy="limit-input"]').send_keys(limitPrice)
    
    def preview(self):
        self.driver.find_element(By.XPATH, '(//span[@class="v-btn__content"])[9]').click()

    def submit(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH, '(//span[@class="v-btn__content"])[11]').click()

    def executeOrder(self, ticker , transaction, quantity, orderType, limitPrice, sendEmail = True):
        self.openWebDriver()
        self.login()
        self.setStock(ticker)
        try:
            self.removePopup()
        except:
            pass
        if transaction != 'Buy':
            self.setTransaction(transaction)
        
        maxQuantity = self.getMaxQuantity()
        if maxQuantity < quantity:
            quantity = maxQuantity
        self.setQuantity(quantity)
        
        if orderType != "Market":    
            self.setOrderType(orderType, limitPrice)
            
        self.preview()
        self.submit()
        
