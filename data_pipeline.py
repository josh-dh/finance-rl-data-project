from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import csv
yf.pdr_override()
data_file = open("financial-tweets/stockerbot-export.csv")
reader = csv.reader(data_file)

#use to get hourly stock data for all tickers on the given date
#returns a hash table where each entry is an ndarray of prices
#the 7 entries are the open prices for that hour
#as more finite data is not available, consider the price of a stock at any time as the price for that hour
def get_stock_data(tickers, start_date, end_date):
    stock_tickers = {}
    for ticker in tickers:
        stock_tickers[ticker] = pdr.get_data_yahoo(ticker, start=start_date, end=end_date, interval="1h")["Open"].to_numpy()

    return stock_tickers

data = get_stock_data(["MSFT", "AAPL"], "2018-07-02", "2018-07-03")
print(data["MSFT"][0])

#process a tweet timestamp to get the start date, end date, and the index of the hour to find the price
#returns tuple (start_date, end_date, hour_index)
def get_date_for_tweet_timestamp(timestamp):
    start_date = ""
    end_date = ""
    hour = 0

    return (start_date, end_date, hour)

#process a tweet object to get the stock prices for the mentioned tickers at the given time
def get_prices_for_tweet(tickers, timestamp):
    date = get_date_for_tweet_timestamp(timestamp)
    prices = {}

    return prices

#returns processed and cleaned tweet, and price data for mentioned tickers
def get_next_tweet():
    line = next(reader)
    tweet = line[0]
    timestamp = line[1]
    tickers = line[2].split('-')
    prices = get_prices_for_tweet(tickers, timestamp)
    return 0

get_next_tweet()