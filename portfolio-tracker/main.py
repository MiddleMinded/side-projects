from pathlib import Path
from db.database import Database
from models.portfolio import Portfolio

def main():
    db_dir = Path(__file__).parent
    db_path = db_dir / "user_data.db"
    user_db = Database(db_path)
    user_portfolio = Portfolio(user_db)

def get_price(ticker: str, current_prices: dict) -> float:
    """Returns the current price for a given ticker."""

    if ticker in current_prices:
        return current_prices[ticker]
    else:
        print(f"{ticker} does not exist.")
        temp_price = float(input(f"Enter the current price of {ticker}: $"))
        current_prices[ticker] = temp_price
        print(f"\n{ticker} @ ${temp_price:.2f} stored.")
        return current_prices[ticker]
         

if __name__ == "__main__":
    current_prices = {
        "AAPL": 10,
        "MSFT": 20,
        "SPCX": 120
    }
    ticker = "TSLA"
    print(get_price(ticker, current_prices))
    print(get_price(ticker, current_prices))

    
