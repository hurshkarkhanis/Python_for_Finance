#Simple Python program written while self teaching myself the language 
#Used YouTube tutorials to pull financial statement data from Yahoo Finance, 
#Used personal knowledge to calculate financial ratios

import numpy as np
import requests
import math

import lxml
from lxml import html

class StrongBalanceSheetClass():

	def __init__(self):
		self.ticker = ''
		self.plugIn = ''
		self.url = ''
		self.page = ''
		self.tree = ''
		self.companyName = ''
		self.fullBalanceSheet = []
		self.fullCashFlow = []


	def getTickerInput(self):

		self.ticker = input("PLEASE ENTER COMPANY TICKER (AMERICAN COMPANIES ONLY) : ")

		self.plugIn = 'balance-sheet'
		self.url = 'https://finance.yahoo.com/quote/' + self.ticker + '/'+ self.plugIn +'?p=' + self.ticker

	def getCompanyName(self):
		self.page = requests.get(self.url)

		self.tree = html.fromstring(self.page.content)

		
		self.companyName = self.tree.xpath("//h1/text()")


	def printCompanyName(self):
		print(self.companyName)
		print()
	 
	def makeBalanceSheet(self):

		table_rows = self.tree.xpath("//div[contains(@class, 'D(tbr)')]")

		lineItems = []

		numLines = 0
		for table_row in table_rows:
		    dataPoint = []
		    el = table_row.xpath("./div")
		    
		    none_count = 0
		    
		    for rs in el:
		        try:
		            (text,) = rs.xpath('.//span/text()[1]')
		            dataPoint.append(text)
		        except ValueError:
		            dataPoint.append(np.NaN)
		            none_count += 1

		    
		    if (none_count == 0):
		        lineItems.append(dataPoint)
		        numLines+=1


		##fullBalanceSheet = []
		for x in lineItems:
			self.fullBalanceSheet.append(x)
		

		for x in self.plugIn:
			if(x != '-'):
				print(x.upper(),end = '')
			else:
				print(' '),
		print()
		print()
		

		for x in self.fullBalanceSheet:
			print(x)
			print()
		#print financial statement


	def plugInAndURLCashFlow(self):
		self.plugIn = 'cash-flow'
		self.url = 'https://finance.yahoo.com/quote/' + self.ticker + '/'+ self.plugIn +'?p=' + self.ticker


	def makeCashFlow(self):
		self.page = requests.get(self.url)

		self.tree = html.fromstring(self.page.content)


		table_rows = self.tree.xpath("//div[contains(@class, 'D(tbr)')]")

		lineItemsCF = []

		numLines = 0
		for table_row in table_rows:
		    dataPoint = []
		    el = table_row.xpath("./div")
		    
		    none_count = 0
		    
		    for rs in el:
		        try:
		            (text,) = rs.xpath('.//span/text()[1]')
		            dataPoint.append(text)
		        except ValueError:
		            dataPoint.append(np.NaN)
		            none_count += 1
		            #print dataPoint, "type: ", type(dataPoint[0])
		    
		    if (none_count < 4):
		        lineItemsCF.append(dataPoint)
		        numLines+=1


		for x in lineItemsCF:
			self.fullCashFlow.append(x)

		for x in self.plugIn:
			if(x != '-'):
				print(x.upper(),end = '')
			else:
				print(' '),
		print()

		for x in self.fullCashFlow:
			print(x)
			print()


	def setUpMetrics(self):
		print (self.companyName, "Metrics")
		print
	
	def buildCurrentRatio(self):
		totalCurrentAssets = 0.0
		totalCurrentLiabilities = 0.0
		#current ratio
		for x in self.fullBalanceSheet:
			if x[0] == "Total Current Assets":
				totalCurrentAssets = x[1]
			if x[0] == "Total Current Liabilities":
				totalCurrentLiabilities = x[1]

		if totalCurrentAssets == 0 or totalCurrentLiabilities == 0:
			print ('CURRENT RATIO: cannot caluclate, no current assets or liabilities listed')
		else:
			print ('CURRENT RATIO: ' , float(str(totalCurrentAssets).replace(',', '')) / int(str(totalCurrentLiabilities).replace(',', '')))
		#current ratio

	def buildQuickRatio(self):
		#quick ratio
		totalCurrentAssets = 0.0
		inventory = 0.0
		totalCurrentLiabilities = 0.0
		for x in self.fullBalanceSheet:
			if x[0] == "Total Current Assets":
				totalCurrentAssets = x[1]
		for x in self.fullBalanceSheet:
			if x[0] == "Inventory":
				inventory = x[1]
			if x[0] == "Total Current Liabilities":
				totalCurrentLiabilities = x[1]
		if totalCurrentAssets == 0 or inventory == 0 or totalCurrentLiabilities == 0:
			print ('QUICK RATIO: cannot caluclate, no inventory listed')
		else:
			print ('QUICK RATIO: ' , (float(str(totalCurrentAssets).replace(',', '')) - float(str(inventory).replace(',', ''))) / int(str(totalCurrentLiabilities).replace(',', '')))
		print()
		#quick ratio

	def buildDebtToEquity(self):
		#debt to equity ratio
		totalLiabilities = 0.0
		totalSE = 0.0
		for x in self.fullBalanceSheet:
			if x[0] == "Total Liabilities":
				totalLiabilities = x[1]
			if x[0] == "Total stockholders' equity":
				totalSE = x[1]

		if totalLiabilities == 0 or totalSE == 0:
			print ('DEBT TO EQUITY RATIO: cannot caluclate, no liabilities or stockholders equity listed')
		else:
			print ('DEBT TO EQUITY RATIO: ' , (float(str(totalLiabilities).replace(',', ''))) / int(str(totalSE).replace(',', '')))
		#debt to equity ratio

	def buildTotalAssetToLiab(self):
		#total assets vs total liab
		totalAssets = 0.0
		totalLiabilities = 0.0
		for x in self.fullBalanceSheet:
			if x[0] == "Total Assets":
				totalAssets = x[1]
			if x[0] == "Total Liabilities":
				totalLiabilities = x[1]
		if totalAssets == 0 or totalLiabilities == 0:
			print ('TOTAL ASSETS / TOTAL LIAB.: cannot caluclate, no total assets or total liabilities listed')
		else:
			print ('TOTAL ASSETS / TOTAL LIAB.: ' , (float(str(totalAssets).replace(',', ''))) / (int(str(totalLiabilities).replace(',', ''))))
		print
		# total assets vs total liab

	def buildTotalSShortTermToLiab(self):
		#total short term assets vs liab
		totalSTassets = 0.0
		totalSTliab = 0.0
		for x in self.fullBalanceSheet:
			if x[0] == "Total non-current assets":
				totalSTassets = x[1]
			if x[0] == "Total non-current liabilities":
				totalSTliab = x[1]
		if totalSTassets == 0 or totalSTliab == 0:
			print ('TOTAL SHORT TERM ASSETS / TOTAL SHORT-TERM LIAB.: cannot caluclate, no short term assets or short term liabilities listed')
		else:
			print ('TOTAL SHORT TERM ASSETS / TOTAL SHORT-TERM LIAB: ' , float(str(totalSTassets).replace(',', '')) / int(str(totalSTliab).replace(',', '')))
		print
		#total short term assets vs liab

	def buildCashFlowToDebt(self):
		#cash flow vs debt
		freeCashFlow = 0.0
		totalLiabilities = 0.0
		for x in self.fullCashFlow:
			if x[0] == "Free Cash Flow":
				freeCashFlow = x[1]
		for x in self.fullBalanceSheet:
			if x[0] == "Total Liabilities":
				totalLiabilities = x[1]
		if freeCashFlow == 0 or totalLiabilities == 0:
			print ('CASH FLOW / DEBT : cannot caluclate, no cash flow or total liabilities listed')
		else:
			print ('CASH FLOW / DEBT: ' , float(str(freeCashFlow).replace(',', '')) / int(str(totalLiabilities).replace(',', '')))
		#cash flow vs debt

	def line(self):
		print ("==============================================")





