from types import BuiltinMethodType
from matplotlib import style
from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import pickle
import sys
import datetime as dt 

# portfolio = {'AAPL':20, "TSLA":5, "GS":10}

# with open("portfolio.pkl", "wb") as f:
#     pickle.dump(portfolio,f)

with open("portfolio.pkl", "rb") as f:
    portfolio= pickle.load(f)


def save_portfolio():
    with open("portfolio.pkl", "wb") as f:
        pickle.dump(portfolio,f)


def add_portfolio():
    ticker = input("Whick stock you want to add: ")
    amount = input("How many share you want to buy")

    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)
    
    save_portfolio()

def remove_portfolio():
    ticker = input("Whick stock you want to sell: ")
    amount = input("How many share you want to sell")

    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker]-= int(amount)
            save_portfolio()
        else:
            print("You don't have enough share")
    else:
        print(f"You don't have that comany share {ticker}")

def show_portfolio():
    print("Your portfolio")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")


def porfolio_worth():
    sum =0
    for ticker in portfolio.keys():
        data = web.DataReader(ticker,'yahoo')
        price = data['Close'].iloc[-1]
        sum += price
    print(f"Your porfolio worth {sum} USD")

def portfolio_gain():
    starting_date = input("Enter date for comparison (YYYY-MM-DD)")
    sum_now = 0
    sum_then =0

    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker,'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then
        print(f"Relative gain: {((sum_now-sum_then)/sum_then)*100}%")
        print(f"Absolute gain: {(sum_now-sum_then)} $USD")
    except IndexError:
        print("There is no trading that day")




def plot_chart():
    ticker = input("choose a ticker symbol: ")
    starting_string = input("Choose a starting date (DD/MM/YYYY) ")
    plt.style.use('dark_background')
    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    data = web.DataReader(ticker,'yahoo',start, end)
    colors = mpf.make_marketcolors(up='#00ff00',down='#ff0000', wick= 'inherit', edge='inherit',volume='in')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=colors)
    mpf.plot(data, type='candle', style= mpf_style, volume=True)


def bye():
    print("Good Bye")
    sys.exit(0)

mappings = {
    'plot_chart':plot_chart,
    'add_portfolio':add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio':show_portfolio,
    'portfolio_gain': portfolio_gain,
    'porfolio_worth': porfolio_worth,
    'bye':bye
}


assistance = GenericAssistant('intents.json', mappings, "Stock Market Bot")
# assistance.train_model()
# assistance.save_model()
assistance.load_model()

while True:
    message= input("")
    assistance.request(message)



    
