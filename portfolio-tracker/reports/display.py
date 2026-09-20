import datetime
from analytics import metrics
from db.database import Database
from models.portfolio import Portfolio
from tabulate import tabulate

def positions_table(portfolio: Portfolio, current_prices: dict) -> None:
    """
    Prints a table of current positions with current price, market value, 
    and unrealized gain.
    """
    table_data = []
    for ticker, position in portfolio.positions.items():
        current_price = current_prices[ticker]
        market_value = position.market_value(current_price)
        unrealized_gain = metrics.unrealized_gain(position, current_price)

        position_data = {
            "TICKER": ticker,
            "SHARES": position.quantity,
            "AVERAGE COST": position.avg_cost,
            "MARKET VALUE": market_value,
            "UNREALIZED GAIN": unrealized_gain
        }
        table_data.append(position_data)

    tmv = metrics.total_market_value(portfolio, current_prices)
    ug = metrics.total_unrealized_gain(portfolio, current_prices)
    totals_row = {
            "TICKER": "-TOTAL-",
            "SHARES": "",
            "AVERAGE COST": "",
            "MARKET VALUE": tmv,
            "UNREALIZED GAIN": ug
    }
    table_data.append(totals_row)

    print(tabulate(table_data, 
            headers="keys",
            tablefmt="grid",
            floatfmt=("", ".5f", ".4f", ".2f", ".2f")))

def cash_summary(portfolio: Portfolio, current_prices: dict) -> None:
    """
    Prints a table with the current cash account balance and total portfolio 
    value.
    """
    table_data = [{
        "CATEGORY": "Cash Account Balance",
        "AMOUNT": portfolio.cash_account.balance
        },
        {
        "CATEGORY": "Total Portfolio Value",
        "AMOUNT": metrics.total_portfolio_value(portfolio, current_prices)
        }]

    print(tabulate(table_data,
            headers="keys",
            tablefmt="grid",
            floatfmt=("", ".2f")))

if __name__ == "__main__":
    db = Database(":memory:")
    portfolio = Portfolio(db)
    portfolio.deposit(1000, datetime.date(2026, 9, 15), "Cash in")
    portfolio.get_or_create_stock("AAPL", "Apple, Inc.", "Tech", "NASDAQ")
    portfolio.get_or_create_stock("MSFT", "Microsoft, Inc.", "Tech", "NASDAQ")
    portfolio.get_or_create_stock("CRZY", "Crazy Co.", "Durable Goods", "NYSE")
    portfolio.buy("AAPL", 5.0, 10.00, datetime.date(2026, 9, 20), 0)
    portfolio.buy("MSFT", 2.0, 20.00, datetime.date(2026, 9, 20), 0)
    portfolio.buy("CRZY", 1.5, 10.10, datetime.date(2026, 9, 20), 0)
    portfolio.buy("AAPL", 3.0, 20.00, datetime.date(2026, 9, 20), 0)
    current_prices = {"AAPL": 30.00, "MSFT": 5.00, "CRZY": 10.11}
    positions_table(portfolio, current_prices)
    cash_summary(portfolio, current_prices)