from prefect import flow, task
import requests
from prefect.blocks.system import Secret

import os

@task
def fetch_data(ticker):
    base_url = "https://www.alphavantage.co"
    secret_block = Secret.load("alphavantage-secret")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={secret_block.get()}'
    r = requests.get(url)
    return r


@task
def get_avg(r):
    data = r.json()['Time Series (Daily)']['2022-10-04']
    open = float(data['1. open'])
    high =float(data['2. high'])
    low = float(data['3. low'])
    close = float(data['4. close'])
    avg= (open+high+low+close)/4
    return avg

@task
def write_to_file(ticker,avg):
    print(f'the daily avg for {ticker} is {avg}')

    return True


@flow(version=os.getenv("GIT_COMMIT_SHA"))
def get_daily_avg(ticker,test):
    data =fetch_data(ticker)
    avg = get_avg(data)
    wrote_file = write_to_file(ticker, avg)



if __name__ == "__main__":
    get_daily_avg("IBM","ABC")