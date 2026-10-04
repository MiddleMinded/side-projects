import bext
import datetime
import time
from pathlib import Path
from db.database import Database
from models.portfolio import Portfolio
from reports.display import portfolio_summary

def main():
    db_dir = Path(__file__).parent
    db_path = db_dir / "user_data.db"
    user_db = Database(db_path)
    user_portfolio = Portfolio(user_db)
    run(user_portfolio)
    user_db.close()

def run(portfolio: Portfolio):
    print("#" * 49)
    print("#" + " " * 47 + "#")
    print("#" + " " * 10 + "PORTFOLIO TRACKER MAIN MENU" + " " * 10 + "#")
    print("#" + " " * 47 + "#")
    print("#" * 49)

    current_prices = {}

    while True:
        print("\nSelect one of the options below:\n")
        print("(1) Buy Stock")
        print("(2) Sell Stock")
        print("(3) Deposit Funds")
        print("(4) Withdraw Funds")
        print("(5) Record Dividend")
        print("(6) View Portfolio Summary")
        print("(7) View Positions")
        print("(8) View Cash Summary")
        print("(9) View Portfolio ROI")
        print("(10) View Diversification")
        print("(11) Exit")
        selection = input("\nSelection: ")

        if selection == "":
            print("You must make a selection.")
            time.sleep(1)
            bext.clear()
            continue
        elif not selection.isdigit():
            print("You must enter a number from the list of options.")
            time.sleep(1)
            bext.clear()
            continue
        else:
            selection = int(selection)
            if selection == 1:
                handle_buy(portfolio)
            
            elif selection == 2:
                handle_sell(portfolio)
            
            elif selection == 3:
                handle_deposit(portfolio)
            
            elif selection == 4:
                pass 
            
            elif selection == 5:
                pass
            
            elif selection == 6:
                for ticker, position in portfolio.positions.items():
                    if position.quantity == 0:
                        current_prices[ticker] = 0.0
                    else:
                        current_prices[ticker] = get_price(
                            ticker, current_prices)
                portfolio_summary(portfolio, current_prices)

            elif selection == 7:
                pass 
            
            elif selection == 8:
                pass 
            
            elif selection == 9:
                pass 
            
            elif selection == 10:
                pass 
            
            elif selection == 11:
                break

def handle_buy(portfolio: Portfolio):
    """
    Creates a stock, if none exists, and then creates a buy transaction for that 
    stock.
    """
    ticker = input("\nEnter the ticker symbol: ")
    ticker = ticker.strip().upper()
    if ticker in portfolio.sectors:
        print(f"Found {ticker} in database.")
    else:
        print(
            f"{ticker} not found in database. Provide the following details.\n")
        while True:
            try:
                name = input("Full company name: ")
                sector = input("Stock sector: ")
                exchange = input("Stock exchange: ")
                portfolio.get_or_create_stock(
                    ticker, name, sector, exchange)
                break
            except ValueError:
                print("\nWARNING: All fields must be completed.\n")
                continue

    while True:
        try:
            date = prompt_date(
                "Enter the transaction date (YYYY-MM-DD) or leave blank for " \
                "today: ")
            quantity = prompt_float("Enter the buy quantity: ")
            price = prompt_float("Enter the buy price: $")
            fees = prompt_float(
                "Enter the fees paid or leave blank for no fees: $", default=0.0)
            portfolio.buy(ticker, quantity, price, date, fees)
            break
        except ValueError as e:
            print(f"\n{e}\n")
            continue

def handle_sell(portfolio: Portfolio):
    """
    Creates a sell transaction for a stock currently held in the portfolio.
    """
    ticker = input("\nEnter the ticker symbol: ")
    ticker = ticker.strip().upper()
    while True:
        try:
            date = prompt_date(
                "Enter the transaction date (YYYY-MM-DD) or leave blank for " \
                "today: ")
            quantity = prompt_float("Enter the sell quantity: ")
            price = prompt_float("Enter the sell price: $")
            fees = prompt_float(
                "Enter the fees paid or leave blank for no fees: $", default=0.0)
            portfolio.sell(ticker, quantity, price, date, fees)
            break
        except ValueError as e:
            print(f"\n{e}\n")
            continue

def handle_deposit(portfolio: Portfolio):
    """Creates a deposit transaction."""
    while True:
        try:
            date = prompt_date(
                "Enter the transaction date (YYYY-MM-DD) or leave blank for " \
                "today: ")
            amount = prompt_float("Enter the amount: $")
            description = input("Enter a description for the transaction: ")
            if description == "":
                portfolio.deposit(amount, date)
            else:
                portfolio.deposit(amount, date, description)
            break
        except ValueError:
            continue
    

def get_price(ticker: str, current_prices: dict) -> float:
    """Returns the current price for a given ticker."""

    if ticker in current_prices:
        return current_prices[ticker]
    else:
        print(f"{ticker} does not exist.")
        temp_price = prompt_float(f"Enter the current price of {ticker}: $")
        current_prices[ticker] = temp_price
        print(f"\n{ticker} @ ${temp_price:.2f} stored.")
        return current_prices[ticker]

def prompt_float(prompt: str, default=None) -> float:
    """Validates and converts user input to a float."""
    while True:
        value = input(prompt)
        if value == "":
            return default
        try:
            float_value = float(value.strip())
        except ValueError:
            print("\nYour input was not a valid number.")
            continue

        return float_value

def prompt_date(prompt: str) -> datetime:
    """Validates and converts user input to a datetime object."""
    while True:
        value = input(prompt)
        if value == "":
            return datetime.date.today()
        else:
            try:
                return datetime.date.fromisoformat(value)
            except ValueError:
                continue

        
        
         

if __name__ == "__main__":
    main()


    
