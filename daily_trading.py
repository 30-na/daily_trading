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
    raw_data = yf.download(tickers = symbol_name, period = '300d', interval = '1d' )
    return raw_data

def add_SMA_to(raw_data):
    
    def SMA(close_price, period = 9):
        sma = close_price.rolling(window=period).mean().iloc[period-1: ]
        return sma.to_frame()
    
    sma = SMA(raw_data['Adj Close'], 9)
    raw_data['SMA'] =  sma
    raw_data['sma_position'] = ((raw_data['Adj Close'] - raw_data['SMA']) / raw_data['Adj Close']) * 100
    return raw_data

def add_SMA09_to(raw_data):
    
    def SMA(close_price, period = 9):
        sma = close_price.rolling(window=period).mean().iloc[period-1: ]
        return sma.to_frame()
    
    sma = SMA(raw_data['Adj Close'])
    raw_data['SMA09'] =  sma
    return raw_data

def add_SMA21_to(raw_data):
    
    def SMA(close_price, period = 21):
        sma = close_price.rolling(window=period).mean().iloc[period-1: ]
        return sma.to_frame()
    
    sma = SMA(raw_data['Adj Close'])
    raw_data['SMA21'] =  sma
    return raw_data

today = str(datetime.date.today())
stock_list = fidelity_top_stock(file_name)
upward_trend_stock_list = []


# def str1_cross_SMA (symbol):


df = download_raw_data("LOGI")
df = add_SMA09_to(df)
df = add_SMA21_to(df)
df["trend"] = df.iloc[:,6] - df.iloc[: ,7] 

print(df.iloc[-10: , [4,6,7,8]]) 

symbol = "U"
interval = 250
def regular_profit(symbol_df, interval):
    profit = (( symbol_df.iloc[-1 , 4] - symbol_df.iloc[-interval , 4] ) /  symbol_df.iloc[-interval , 4]) * 100
    return profit


def str01_cross_sma(symbol_df, interval):
    position = "sell"
    profit = 0
    count_buy_day = 0
    count_sell_day = 0
    for i in range(interval):
        if position == "sell":
            count_sell_day += 1
            
        if position == "buy":
            count_buy_day += 1
        # print(i, end= " ")
        # print(position, end=' ')
        # print(symbol_df.iloc[-interval + i , 8], end=" ")
        # print(count_sell_day, end=" ")
        # print(count_buy_day)
         
        if symbol_df.iloc[-interval + i , 8] > 1 and position == "sell":
            buy_price = symbol_df.iloc[-interval + i , 4]
            position = "buy"
            
        elif symbol_df.iloc[-interval + i , 8] < -1 and position == "buy":
            position = 'sell'
            profit = (symbol_df.iloc[-interval + i , 4] - buy_price) + profit
    profit = (profit / symbol_df.iloc[-interval , 4]) * 100
    # print(count_buy_day)
    # print(count_sell_day)     
    return profit

print(regular_profit(df, interval))
print(str01_cross_sma(df, interval))    




# plot 
# symbol = 'ENVA'
# df = download_raw_data(symbol)
# df = add_signal_to(df)
# plt.figure(figsize = (24,12))
# plt.plot(df['2020':'2021']['Adj Close'], label='Adj Close', linewidth = 2)
# plt.plot(df['2020':'2021']['SMA'], label='9 days rolling SMA', linewidth = 1.5)
# plt.xlabel('Date')
# plt.ylabel('Adjusted closing price ($)')
# plt.title('Simple Moving Average')
# plt.legend()
# plt.show()


#plot
symbol = 'LOGI'
period = 500
plt.figure(figsize = (24,12))
plt.plot(df.iloc[-period: , [4]], label='Adj Close', linewidth = 2)
plt.plot(df.iloc[-period: , [6]], label='9 days rolling SMA', linewidth = 1.5)
plt.plot(df.iloc[-period: , [7]], label='21 days rolling SMA', linewidth = 1.5)
plt.xlabel('Date')
plt.ylabel('Adjusted closing price ($)')
plt.title('Simple Moving Average')
plt.legend()
plt.show()







