from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os, time

import config

class Scraping:
	def openWebDriver(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument("log-level=3")
		options.add_argument('load-extension=' + os.getenv('APPDATA') + r'\..\Local\Google\Chrome\User Data\Default\Extensions\cjpalhdlnbpafiamejdnhcphjbkeiagm\1.38.6_0')
		self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
		
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

		self.driver.find_element_by_id('username').send_keys(config.INVESTOPEDIA_EMAIL)
		self.driver.find_element_by_id('password').send_keys(config.INVESTOPEDIA_PASSW)

		self.driver.find_element_by_id('login').click()

	def scrapeAccCash(self):
		self.driver.get('https://www.investopedia.com/simulator/trade/tradestock.aspx')
  
		accBuyingCash = self.driver.find_elements_by_class_name('num')
		return accBuyingCash[0].text, accBuyingCash[2].text

	def getTradePage(self):
		self.driver.get('https://www.investopedia.com/simulator/trade/tradestock.aspx')
	
	def setStock(self, ticker):
		self.driver.find_element_by_id('symbolTextbox').send_keys(ticker)
		self.driver.find_element_by_id('symbolTextbox_mi_1').click()

	def setTransaction(self, transaction):
		orderDict = {
			'Buy': 0,
			'Sell' : 1,
			'Sell Short' : 2,
			'Buy to Cover' : 3
		}
		Select(self.driver.find_element_by_id('transactionTypeDropDown')).select_by_index(orderDict.get(transaction))

	def getMaxQuantity(self):
		self.driver.find_element_by_id('showMaxLink').click()
		
		time.sleep(0.5)
		maxQuantityText = self.driver.find_element_by_id('limitationLabel')
		maxQuantity = 0
		for word in (maxQuantityText.text).split():
			if word.isdigit():
				maxQuantity = int(word)
		return maxQuantity

	def setQuantity(self, quantity):
		self.driver.find_element_by_id('quantityTextbox').send_keys(quantity)

	def setOrderType(self, orderType, limitPrice):
		if(orderType == "Limit"):
			self.driver.find_element_by_id('limitRadioButton').click()
			self.driver.find_element_by_id('limitPriceTextBox').send_keys(str(limitPrice))
	
	def setSendEmail(self, sendEmail):
		if sendEmail == False:
			sendConfirmationEmail = self.driver.find_element_by_id('sendConfirmationEmailCheckBox').click()

	def previewAndSubmit(self):
		self.driver.find_element_by_id('previewButton').click()
		self.driver.find_element_by_id('submitOrder').click()

	def executeOrder(self, ticker, transaction, quantity, orderType, limitPrice, sendEmail = True):
		self.getTradePage()
		self.setStock(ticker)
		self.setTransaction(transaction)
		
		maxQuantity = self.getMaxQuantity()
		if quantity > maxQuantity:
			quantity = maxQuantity
			
		self.setQuantity(quantity)
		self.setOrderType(orderType, limitPrice)
		self.setSendEmail(sendEmail)
		self.previewAndSubmit()
		
		return maxQuantity