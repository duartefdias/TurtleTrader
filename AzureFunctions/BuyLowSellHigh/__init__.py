# From Azure template
import datetime
import logging
import azure.functions as func

# Custom imports
import alpaca_trade_api as tradeapi
import os

api = tradeapi.REST(os.getenv("API_KEY_ID"), os.getenv("SECRET_ACCESS_KEY"), base_url="https://paper-api.alpaca.markets")

# Large cap stocks
large_caps = ['AAPL', 'AMZN', 'MSFT', 'GOOG', 'GOOGL', 'FB', 'TSLA', 'NVDA', 'PYPL', 'ADBE', 'NFLX', 'AVGO', 'CSCO', 'INTC', 'AMGN', 'QCOM', 'TXN', 'COST', 'MDLZ', 'SBUX', 'BIIB', 'TMUS', 'ISRG', 'CHTR', 'BKNG']

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

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # Loop through the top stocks and check if the price has dipped
    for stock in large_caps:
        if check_price_dip(stock.symbol):
            # Buy the stock if the price has dipped
            api.submit_order(
                symbol=stock.symbol,
                qty=1,
                side='buy',
                type='limit',
                time_in_force='gtc',
                limit_price=stock_price,
                extended_hours=False
            )
            # Wait for a few seconds to avoid hitting the rate limit
            time.sleep(3)

    print("Dip buying complete")
