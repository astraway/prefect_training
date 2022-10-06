from prefect import flow, task
import requests
from prefect.blocks.system import Secret
import subprocess
from prefect import get_run_logger
from prefect_dask import DaskTaskRunner
# import git



# Access the stored secret


# repo = git.Repo(search_parent_directories=True)
# sha = repo.head.commit.hexsha
# sha
import os

@task
def fetch_data(ticker):

    base_url = "https://www.alphavantage.co"
    secret_block = Secret.load("alphavantage-secret")
    print(secret_block.get())
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
    logger = get_run_logger()
    logger.debug("logger info test")
    print(f'the daily avg for {ticker} is {avg}')

    return True


@flow(version=subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip(),task_runner=DaskTaskRunner )
def get_daily_avg(ticker):
    logger = get_run_logger()
    logger.info("logger info test")
    print(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip())
    data =fetch_data.map(ticker)
    avg = get_avg.map(data)
    wrote_file = write_to_file.map(data, avg)



if __name__ == "__main__":
    get_daily_avg(["IBM","AAPL"])