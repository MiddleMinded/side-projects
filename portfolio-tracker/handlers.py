import datetime
from models.portfolio import Portfolio

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
                print(f"Stock record for {ticker} created.\n")
                break
            except ValueError as e:
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
            print(f"Purchase of {quantity:.5f} shares of {ticker} recorded.")
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
            print(f"Sale of {quantity:.5f} shares of {ticker} recorded.")
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
            print(f"Deposit of ${amount:.2f} recorded.")
            break
        except ValueError as e:
            print(f"\n{e}\n")
            continue

def handle_withdraw(portfolio: Portfolio):
    """Creates a withdraw transaction."""
    while True:
        try:
            date = prompt_date(
                "Enter the transaction date (YYYY-MM-DD) or leave blank for " \
                "today: ")
            amount = prompt_float("Enter the amount: $")
            description = input("Enter a description for the transaction: ")
            if description == "":
                portfolio.withdraw(amount, date)
            else:
                portfolio.withdraw(amount, date, description)
            print(f"Withdrawal of ${amount:.2f} recorded.")
            break
        except ValueError as e:
            print(f"\n{e}\n")
            continue

def handle_record_dividend(portfolio: Portfolio):
    """Creates a dividend transaction."""
    while True:
        try:
            date = prompt_date(
                "Enter the transaction date (YYYY-MM-DD) or leave blank for " \
                "today: ")
            amount = prompt_float("Enter the amount: $")
            description = input("Enter a description for the transaction: ")
            if description == "":
                portfolio.record_dividend(amount, date)
            else:
                portfolio.record_dividend(amount, date, description)
            print(f"Dividend of ${amount:.2f} recorded.")
            break
        except ValueError as e:
            print(f"\n{e}\n")
            continue

def refresh_current_prices(portfolio: Portfolio, current_prices: dict) -> None:
    """Prompts user for the price of every active position in the portfolio."""
    for ticker, position in portfolio.positions.items():
        if position.quantity == 0:
            current_prices[ticker] = 0.0
        else:
            current_prices[ticker] = get_price(
            ticker, current_prices)

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