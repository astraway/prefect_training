from prefect import task, flow
import yfinance as yf
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn= task_input_hash, cache_expiration=timedelta(minutes=1),retries=4,retry_delay_seconds=20)
def get_data(ticker):
    df = yf.download(tickers=ticker)
    print(df)

@task()
def get_quarterly_financials(ticker):
    ticker_data = yf.Ticker(ticker)
    return ticker_data.quarterly_financials


@task
def print_to_screen(qtr_fin):
    print(qtr_fin)
    return qtr_fin



@flow
def quarterly_financials_flow(ticker):
    qtr_fin = get_quarterly_financials(ticker)
    wrote_to_parqet = print_to_screen(qtr_fin)
    return qtr_fin


@flow
def stock_flow(ticker):
    ticker_data = get_data(ticker)
    qtr_fin = quarterly_financials_flow(ticker)
    return True




if __name__ == "__main__":
    stock_flow("AAPL")