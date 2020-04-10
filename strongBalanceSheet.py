#Python program written while self teaching myself the language 
#Used online web scraper turotials to pull balance sheet data from Yahoo Finance, 
#Used personal knowledge to calculate financial ratios

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import pandas_datareader.data as web 
import requests
import math

import lxml
from lxml import html

ticker = raw_input("PLEASE ENTER COMPANY TICKER (AMERICAN COMPANIES ONLY) : ")

print ticker




plugIn = 'balance-sheet'
url = 'https://finance.yahoo.com/quote/' + ticker + '/'+ plugIn +'?p=' + ticker

 

page = requests.get(url)

tree = html.fromstring(page.content)

print
print
companyName = tree.xpath("//h1/text()")
print companyName
print



table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

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


fullBalanceSheet = []
for x in lineItems:
	fullBalanceSheet.append(x)

#print financial statement

for x in plugIn:
	if(x != '-'):
		print x.upper(),
	else:
		print ' ',
print
print

for x in fullBalanceSheet:
	print x
	print
#print financial statement



plugIn = 'cash-flow'
url = 'https://finance.yahoo.com/quote/' + ticker + '/'+ plugIn +'?p=' + ticker


page = requests.get(url)

tree = html.fromstring(page.content)

print

table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

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


fullCashFlow = []
for x in lineItemsCF:
	fullCashFlow.append(x)

for x in plugIn:
	if(x != '-'):
		print x.upper(),
	else:
		print ' ',
print

for x in fullCashFlow:
	print x
	print


print "========================================="
print


print companyName, " METRICS"

totalCurrentAssets = 0.0
totalCurrentLiabilities = 0.0
#current ratio
for x in fullBalanceSheet:
	if x[0] == "Total Current Assets":
		totalCurrentAssets = x[1]
	if x[0] == "Total Current Liabilities":
		totalCurrentLiabilities = x[1]

if totalCurrentAssets == 0 or totalCurrentLiabilities == 0:
	print 'CURRENT RATIO: cannot caluclate, no current assets or liabilities listed'
else:
	print 'CURRENT RATIO: ' , float(str(totalCurrentAssets).replace(',', '')) / int(str(totalCurrentLiabilities).replace(',', ''))
print
#current ratio


#quick ratio
inventory = 0.0
for x in fullBalanceSheet:
	if x[0] == "Inventory":
		inventory = x[1]
if inventory == 0 :
	print 'QUICK RATIO: cannot caluclate, no inventory listed'
else:
	print 'QUICK RATIO: ' , (float(str(totalCurrentAssets).replace(',', '')) - float(str(inventory).replace(',', ''))) / int(str(totalCurrentLiabilities).replace(',', ''))
print
#quick ratio

#debt to equity ratio
totalLiabilities = 0.0
totalSE = 0.0
for x in fullBalanceSheet:
	if x[0] == "Total Liabilities":
		totalLiabilities = x[1]
	if x[0] == "Total stockholders' equity":
		totalSE = x[1]

if totalLiabilities == 0 or totalSE == 0:
	print 'DEBT TO EQUITY RATIO: cannot caluclate, no liabilities or stockholders equity listed'
else:
	print 'DEBT TO EQUITY RATIO: ' , (float(str(totalLiabilities).replace(',', ''))) / int(str(totalSE).replace(',', ''))
#debt to equity ratio

#total assets vs total liab
totalAssets = 0.0
totalLiabilities = 0.0
for x in fullBalanceSheet:
	if x[0] == "Total Assets":
		totalAssets = x[1]
	if x[0] == "Total Liabilities":
		totalLiabilities = x[1]
if totalAssets == 0 or totalLiabilities == 0:
	print 'TOTAL ASSETS / TOTAL LIAB.: cannot caluclate, no total assets or total liabilities listed'
else:
	print 'TOTAL ASSETS / TOTAL LIAB.: ' , (float(str(totalAssets).replace(',', ''))) / (int(str(totalLiabilities).replace(',', '')))
print
# total assets vs total liab

#total short term assets vs liab
totalSTassets = 0.0
totalSTliab = 0.0
for x in fullBalanceSheet:
	if x[0] == "Total non-current assets":
		totalSTassets = x[1]
	if x[0] == "Total non-current liabilities":
		totalSTliab = x[1]
if totalSTassets == 0 or totalSTliab == 0:
	print 'TOTAL SHORT-TERM ASSETS / TOTAL SHORT-TERM LIAB.: cannot caluclate, no short term assets or short term liabilities listed'
else:
	print 'TOTAL SHORT-TERM ASSETS / TOTAL SHORT-TERM LIAB: ' , float(str(totalSTassets).replace(',', '')) / int(str(totalSTliab).replace(',', ''))
print
#total short term assets vs liab

#cash flow vs debt
freeCashFlow = 0.0
totalLiabilities = 0.0
for x in fullCashFlow:
	if x[0] == "Free Cash Flow":
		freeCashFlow = x[1]
for x in fullBalanceSheet:
	if x[0] == "Total Liabilities":
		totalLiabilities = x[1]
if freeCashFlow == 0 or totalLiabilities == 0:
	print 'CASH FLOW / DEBT : cannot caluclate, no cash flow or total liabilities listed'
else:
	print 'CASH FLOW / DEBT ' , float(str(freeCashFlow).replace(',', '')) / int(str(totalLiabilities).replace(',', ''))
print
#cash flow vs debt


