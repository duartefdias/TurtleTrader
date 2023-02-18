# From Azure template
import datetime
import logging
import azure.functions as func

# Alpaca api imports
from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, MarketOrderRequest
from alpaca.trading.enums import AssetClass, OrderSide, TimeInForce

# Other imports
import os

# Set target stock
target_stock = "MSFT"

def main(mytimer: func.TimerRequest) -> None:
    # Get the current time
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # Get environment variables and initialize clients
    api_key_id = os.getenv("API_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")
    historical_data_client = StockHistoricalDataClient(api_key_id, secret_access_key)
    trading_client = TradingClient(api_key_id, secret_access_key, paper=True)

    # Get historical data for a stock
    # Preparing request query
    request_params = StockBarsRequest(
        symbol_or_symbols=[target_stock],
        timeframe=TimeFrame.Day,
        start="2022-02-01 00:00:00"
    )
    # Submit request
    bars = historical_data_client.get_stock_bars(request_params)

    # Convert to pandas dataframe
    bars_df = bars.df
    logging.info(bars_df)

    # TODO: Perform fancy analysis on the data

    # Get all current assets in our alpaca trading account
    assets = trading_client.get_all_positions()
    logging.info(assets)

    # Submit a market order to buy half a share of the target stock
    # Preparing order
    market_order_data = MarketOrderRequest(
                        symbol=target_stock,
                        qty=0.5,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                        )

    # Submit buy order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                )
    
