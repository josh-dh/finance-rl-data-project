from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import csv
from datetime import date
from datetime import timedelta

import torch
import transformers
from pytorch_pretrained_bert import BertTokenizer, BertConfig
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

yf.pdr_override()
data_file = open("financial-tweets/stockerbot-export.csv")
reader = csv.reader(data_file)

#use to get hourly stock data for all tickers on the given date
#returns a hash table where each entry is the price for the requested hour
#for the first 7 hours in the trading day, take the open price
#for the last hour, take the closing price for the day
#as more finite data is not available, consider the price of a stock at any time as the price for that hour
def get_stock_data(tickers, start_date, end_date, hour):
    stock_tickers = {}
    for ticker in tickers:
        if (hour < 7):
            stock_tickers[ticker] = pdr.get_data_yahoo(ticker, start=start_date, end=end_date, interval="1h")["Open"].to_numpy()[hour]
        else:
            stock_tickers[ticker] = pdr.get_data_yahoo(ticker, start=start_date, end=end_date, interval="1h")["Close"].to_numpy()[6]

    return stock_tickers

def get_month(month):
    if (month == 'Jan'):
        month = 1
    elif (month == 'Feb'):
        month = 2
    elif (month == 'Mar'):
        month = 3
    elif (month == 'Apr'):
        month = 4
    elif (month == 'May'):
        month = 5
    elif (month == 'Jun'):
        month = 6
    elif (month == 'Jul'):
        month = 7
    elif (month == 'Aug'):
        month = 8
    elif (month == 'Sep'):
        month = 9
    elif (month == 'Oct'):
        month = 10
    elif (month == 'Nov'):
        month = 11
    else:
        month = 12
    
    return month


#process a tweet timestamp to get the start date, end date, and the index of the hour to find the price
#returns tuple (start_date, end_date, hour_index)
def get_date_for_tweet_timestamp(timestamp):
    timestamp = timestamp.split()
    day_of_week = timestamp[0]
    month = get_month(timestamp[1])
    day = int(timestamp[2])
    hour = int(timestamp[3][0:1])
    year = int(timestamp[5])
    timestamp_date = date(year, month, day)
    #case: use last friday's closing data (time between 1700 friday and 0900 monday)
    if ((day_of_week == 'Mon' and hour < 9) or (day_of_week == 'Fri' and hour > 17) or day_of_week == 'Sat' or day_of_week == 'Sun'):
        hour = 7
        #find date of last friday
        if (day == 'Mon'):
            start_date = timestamp_date - timedelta(days = 3)
        elif (day == 'Sun'):
            start_date = timestamp_date - timedelta(days = 2)
        elif (day == 'Sat'):
            start_date = timestamp_date - timedelta(days = 1)
        else:
            start_date = timestamp_date
    #case: use prev weekday's closing data (time between 1900 and 0900 on weekday nights)
    elif (hour > 17 or hour < 9):
        hour = 7
        start_date = timestamp_date - timedelta(days = 1)
    #case: use opening data for the hour
    else:
        hour -= 9
        start_date = timestamp_date

    end_date = start_date + timedelta(days = 1)

    return (start_date.isoformat(), end_date.isoformat(), hour)

#process a tweet object to get the stock prices for the mentioned tickers at the given time
def get_prices_for_tweet(tickers, timestamp):
    date = get_date_for_tweet_timestamp(timestamp)
    return get_stock_data(tickers, date[0], date[1], date[2])

#apply nlp tokenizer to tweet text
#use BERT pre-trained tokenizer to generate dense contextual tokens which work with the pretrained BERT Model
def process_tweet(tweet_text):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(tweet_text))

#returns processed and cleaned tweet, and price data for mentioned tickers
def get_next_tweet():
    line = next(reader)
    tweet = process_tweet(line[0])
    timestamp = line[1]
    tickers = line[2].split('-')
    try:
        prices = get_prices_for_tweet(tickers, timestamp)
    except (ValueError, IndexError):
        print("invalid ticker used")
        return 0
    return (tweet, prices)

print(get_next_tweet())