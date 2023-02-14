# From Azure template
import datetime
import logging
import azure.functions as func

# Custom imports
from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
import os

# Large cap stocks
large_caps = ['AAPL', 'AMZN', 'MSFT', 'GOOG', 'GOOGL', 'FB', 'TSLA', 'NVDA', 'PYPL', 'ADBE', 'NFLX', 'AVGO', 'CSCO', 'INTC', 'AMGN', 'QCOM', 'TXN', 'COST', 'MDLZ', 'SBUX', 'BIIB', 'TMUS', 'ISRG', 'CHTR', 'BKNG']
target_stock = 'TSLA'

def check_price_dip(ticker):
    # Get the latest price data for the stock
    stock_price = api.get_last_trade(ticker).price
    
    # Get the historical data for the stock
    historical_data = api.get_aggs(ticker, 1, 'day')
    
    # Calculate the average price of the stock over the past 25 days
    avg_price = sum(data.close for data in historical_data) / 25
    
    # Check if the current price is less than the average price
    if stock_price < avg_price:
        return True
    else:
        return False

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    api_key_id = os.getenv("API_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")
    historical_data_client = StockHistoricalDataClient(api_key_id, secret_access_key)
    trading_client = TradingClient(api_key_id, secret_access_key, paper=True)

    request_params = StockBarsRequest(
        symbol_or_symbols=[target_stock],
        timeframe=TimeFrame.Day,
        start="2022-02-01 00:00:00"
    )

    bars = historical_data_client.get_stock_bars(request_params)
    bars_df = bars.df
    print(bars_df)

    print("Dip buying complete")
