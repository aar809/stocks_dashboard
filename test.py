from flask import Flask, render_template,request #this has changed
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

sample_df = pd.read_csv("data/df.csv")

N = 200
x = np.linspace(0, 1, N)
#x will have to be time.. or date?
y = np.random.randn(N)
#y will be the stock price.
df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

print(df)
print(type(df))
print(sample_df)
print(type(sample_df))

random_x = np.random.randn(10)
random_y = np.random.randn(10)

print(random_x)
print(type(random_x))
print(sample_df.iloc[:,0])

import yfinance as yf

msft = yf.Ticker("msft")
df = msft.history(period="24mo")
# df.to_csv (r'data/dji_2.csv', index = True, header=True)
# print(df.iloc[:,0])
# print(df.index)
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
# print(data)
# data.to_csv (r'data/yfinancedata.csv', index = True, header=True)
# msft.balance_sheet
# print(msft.actions(period="24mo"))
print(msft.dividends)
data = yf.Ticker("nflx").institutional_holders
data = yf.Ticker("nflx").info

# print(data)

# pd.DataFrame.from_dict(data=data, orient='index').to_csv('dict_file.csv', header=False)
print(data["sector"])

# data.to_csv (r'data/info.csv', index = False, header=True)
