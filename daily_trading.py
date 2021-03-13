# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:37:54 2021

@author: sin
"""
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

file_name = 'screener_results.xls'
def fidelity_top_stock(file_name):
    df = pd.read_excel(file_name)
    last_symbol_index = (pd.isnull(df['Symbol']).to_numpy().nonzero()[0][0])-1
    stock_symbol = df.loc[:last_symbol_index , 'Symbol']
    return stock_symbol

def download_raw_data(symbol_name):
    raw_data = yf.download(tickers = symbol_name, period = '180d', interval = '1d' )
    return raw_data

def add_signal_to(raw_data):
    
    def SMA(close_price, period = 9):
        sma = close_price.rolling(window=period).mean().iloc[period-1: ]
        return sma.to_frame()
    
    sma = SMA(raw_data['Adj Close'], 9)
    raw_data['SMA'] =  sma
    raw_data['sma_position'] = ((raw_data['Adj Close'] - raw_data['SMA']) / raw_data['Adj Close']) * 100
    return raw_data

today = datetime.date.today()
stock_list = fidelity_top_stock(file_name)

# for i in stock_list:
#     df = download_raw_data(i)
#     df = add_signal_to(df)
#     print(i,end = " ")
#     print ( df['sma_position'].tail(1))
        
   
# plot 
symbol = 'DHR'
df = download_raw_data(symbol)
df = add_signal_to(df)
plt.figure(figsize = (24,12))
plt.plot(df['2020':'2021']['Adj Close'], label='Adj Close', linewidth = 2)
plt.plot(df['2020':'2021']['SMA'], label='9 days rolling SMA', linewidth = 1.5)
plt.xlabel('Date')
plt.ylabel('Adjusted closing price ($)')
plt.title('Simple Moving Average')
plt.legend()
plt.show()









