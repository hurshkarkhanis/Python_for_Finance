#Simple Python program written while self teaching myself the language 
#Used YouTube tutorials to pull data from Yahoo Finance, print daily statistics and display chart 
#Used personal knowledge to integrate Stochastic RSI formula into program and plot on chart

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import pandas_datareader.data as web 


#establishing start and end dates
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2020, 5, 20)

 
#reading yahoo finance data on AMZN
df = web.DataReader('WORK', 'yahoo', start, end)


#creating columns for moving averages and changes
df['CHANGE'] = ( df['Close'] - df['Open'] )

df['15ma'] = df['Adj Close'].rolling(window = 15, min_periods = 0).mean()
df['20ma'] = df['Adj Close'].rolling(window = 20, min_periods = 0).mean()
df['30ma'] = df['Adj Close'].rolling(window = 30, min_periods = 0).mean()
df['50ma'] = df['Adj Close'].rolling(window = 50, min_periods = 0).mean()


df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()

df['gain'] = np.where(df['CHANGE']>=0, df['CHANGE'], 0)
df['loss'] = np.where(df['CHANGE']<=0, df['CHANGE'], 0)


df['14Pgain'] = df['gain'].rolling(window = 14, min_periods = 0).mean()
df['14Ploss'] = df['loss'].rolling(window = 14, min_periods = 0).mean()

#the to steps to calculating RSI
df['step one'] = 100-(100/(1+((df['14Pgain'])/(df['14Ploss']))))

df['step two'] = 100-(100/(1+((df['14Pgain']*13+df['gain'])/(df['14Ploss']*13+df['loss']))))

df['Stochastic RSI'] =  (df['step two'] - df['step two'].rolling(window = 14, min_periods = 0).min() ) / (df['step two'].rolling(window = 14, min_periods = 0).max() - df['step two'].rolling(window = 14, min_periods = 0).min())


ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)


#plotting closing price, moving averages on top plot
#plotting RSI on botton plot
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['15ma'])
ax1.plot(df.index, df['20ma'])
ax1.plot(df.index, df['30ma'])
ax1.plot(df.index, df['50ma'])
ax1.plot(df.index, df['100ma'])
ax2.plot(df.index, df['Stochastic RSI']) 





plt.show()
