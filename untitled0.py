# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:28:10 2021

@author: msin2
"""
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

# get fidelity top rated stock list
file_name = 'screener_results.xls'
def fidelity_top_stock(file_name):
    df = pd.read_excel(file_name)
    last_symbol_index = (pd.isnull(df['Symbol']).to_numpy().nonzero()[0][0])-1
    stock_symbol = df.loc[:last_symbol_index , 'Symbol']
    return stock_symbol

def download_raw_data(symbol_name):
    raw_data = yf.download(tickers = symbol_name, period = '20d', interval = '1d' )
    # df['birth_date'] = pd.to_datetime(df['birth_date'])
    return pd.DataFrame(raw_data)

def SMA(list, period):
    return list.rolling(window=period).mean().iloc[period-1: ]

    
def add_SMA_column(raw_data, period):
    raw_data = download_raw_data('LOGI')
    data_SMA = SMA(raw_data['Adj Close'], period)
    raw_data['SMA'] =  pd.to_numeric(data_SMA) 
    return raw_data

# strategy01 moving average cross the price
# def add_SMA_cross(raw_data): 
#     sma_position = []
#     for i in raw_data:
        
#         if raw_data['SMA']  > raw_data['Adj Close']:
#             sma_position.append['sell']
#         elif raw_data['SMA']  < raw_data['Adj Close']:
#             sma_position.append['buy']
#         else:
#             sma_position.append['watch']
#     raw_data['SMA_position'] = sma_position
#     return raw_data
         
df = download_raw_data('LOGI') 
df = add_SMA_column(df, 9)
sma_position = []
# for i in df:
#     if df['SMA'].isnull():
#         sma_position.append('null')
#     else: 
#         if df['SMA'] < pd.to_numeric(df['Adj Close']):
#             sma_position.append('buy')
#         elif df['SMA'] > pd.to_numeric(df['Adj Close']):
#             sma_position.append('sell')
#         else:
#             sma_position.append('watch') 

if (df[-10:]['SMA'] < df[-10:]['Adj Close']):
    sma_position.append("buy")




    # print(df['SMA'].isnull())  

# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days = 1)
# print( raw_data.loc[today:today]['Adj Close']  )

# print(SMA(raw_data['Adj Close'], 9))
# def plot(close_price):
#     plt.figure(figsize = (12,6))
#     plt.plot(close_price, label='Adj Close',lineWidth = 2 )
#     plt.plot(SMA(close_price, 30), label='SMA', lineWidth = 1.5 )
#     plt.xlabel('Date')
#     plt.ylabel('Adjusted closing price ($)')
#     plt.title('Price with SMA')
#     plt.legend()
#     plt.show()
# plot(raw_data['Adj Close'])

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    