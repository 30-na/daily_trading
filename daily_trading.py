# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:37:54 2021

@author: sin
"""
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import random

file_name = 'screener_results.xls'
today = str(datetime.date.today())
interval = 250

#df["trend"] = df.iloc[:,6] - df.iloc[: ,7] 

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

def plot_cross(symbol, period):
    df = download_raw_data(symbol)
    df = add_SMA09_to(df)
    df = add_SMA21_to(df)
    plt.figure(figsize = (24,12))
    plt.plot(df.iloc[-period: , [4]], label='Adj Close', linewidth = 2)
    plt.plot(df.iloc[-period: , [6]], label='9 days rolling SMA', linewidth = 1.5)
    plt.plot(df.iloc[-period: , [7]], label='21 days rolling SMA', linewidth = 1.5)
    plt.xlabel('Date')
    plt.ylabel('Adjusted closing price ($)')
    plt.title('Simple Moving Average')
    plt.legend()
    plt.show()


def get_SPY_stock_list():
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = table[0]
    df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
    return df["Symbol"]

def profit(stock_list, interval):
    sum = 0
    def regular_profit(symbol_df, interval):
        # if interval > symbol_df.shape[0]:
        #     interval = symbol_df.shape[0]
        profit = (( symbol_df.iloc[-1 , 4] - symbol_df.iloc[-interval , 4] ) /  symbol_df.iloc[-interval , 4]) * 100
        return profit

    for i in stock_list:
        i = i.replace('.','-')
        df = download_raw_data(i)
        sum = regular_profit(df, interval) + sum
    return sum/len(stock_list)

def str1_cross_profit(stock_list, interval):
    
    def cross_sma(symbol_df, interval):
        position = "sell"
        profit = 0
        # count_buy_day = 0
        # count_sell_day = 0
        for i in range(interval):
        #     if position == "sell":
        #         count_sell_day += 1
                
        #     if position == "buy":
        #         count_buy_day += 1
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
   
    sum = 0
    for i in stock_list:
        i = i.replace('.','-')
        df = download_raw_data(i)       
        df = add_SMA09_to(df)       
        df = add_SMA21_to(df)
        df['trend'] = ((df.iloc[:,6] - df.iloc[:,7])/df.iloc[:,6])*100
        sum = cross_sma(df, interval) + sum
    
    return sum/len(stock_list)


budget = 1000
interval = 30
stock_list = fidelity_top_stock(file_name)
my_portfo = dict()
sell_list = []
for i in range(interval):
    #buy
    while budget >= 100:
      stock_symbol = random.choice(stock_list)
      while stock_symbol in my_portfo:
          stock_symbol = random.choice(stock_list)
      symbol_df = download_raw_data(stock_symbol)
      close_price = symbol_df.iloc[-interval + i , 4]
      # print(type(stock_symbol))
      # print(close_price)
      stock_share = 100/close_price
      budget = budget - 100
      # print(my_portfo)
      # print(stock_share)
      my_portfo[stock_symbol] = stock_share
  
    #sell 
    for j in my_portfo:   
        symbol_df = download_raw_data(j)
        close_price = symbol_df.iloc[-interval + i , 4]
        stock_share = my_portfo[j]
        stock_value = close_price * stock_share
        
        if  stock_value > 105 or stock_value < 95:
            budget = stock_value + budget
            sell_list.append(j)
            
    for j in sell_list:
        my_portfo.pop(j)
    
    sell_list.clear()
    
investment_value = budget
for j in my_portfo:
    symbol_df = download_raw_data(j)
    close_price = symbol_df.iloc[-interval + i , 4]
    stock_share = my_portfo[j]
    stock_value = close_price * stock_share
    investment_value = investment_value + stock_value

print(investment_value)



SPY_list = list(get_SPY_stock_list())
SPY_list.remove('VNT')










    
