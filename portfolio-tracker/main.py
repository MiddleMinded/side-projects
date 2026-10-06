import bext
import time
from pathlib import Path
from handlers import (handle_buy, handle_sell, handle_deposit, 
                      handle_withdraw, handle_record_dividend,
                      get_price)
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
                handle_withdraw(portfolio) 
            
            elif selection == 5:
                handle_record_dividend(portfolio)
            
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

if __name__ == "__main__":
    main()