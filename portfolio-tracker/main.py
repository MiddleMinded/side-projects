import bext
import time
from pathlib import Path
from handlers import (handle_buy, handle_sell, handle_deposit, 
                      handle_withdraw, handle_record_dividend,
                      refresh_current_prices)
from db.database import Database
from models.portfolio import Portfolio
from reports.display import (portfolio_summary, positions_table, cash_summary,
                             roi_table, diversification_table)

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
                input("\nPress Enter to continue.\n")
            
            elif selection == 2:
                handle_sell(portfolio)
                input("\nPress Enter to continue.\n")

            elif selection == 3:
                handle_deposit(portfolio)
                input("\nPress Enter to continue.\n")

            elif selection == 4:
                handle_withdraw(portfolio)
                input("\nPress Enter to continue.\n")
            
            elif selection == 5:
                handle_record_dividend(portfolio)
                input("\nPress Enter to continue.\n")
            
            elif selection == 6:
                refresh_current_prices(portfolio, current_prices)
                portfolio_summary(portfolio, current_prices)
                input("\nPress Enter to continue.\n")

            elif selection == 7:
                refresh_current_prices(portfolio, current_prices)
                positions_table(portfolio, current_prices)
                input("\nPress Enter to continue.\n")
            
            elif selection == 8:
                refresh_current_prices(portfolio, current_prices)
                cash_summary(portfolio, current_prices)
                input("\nPress Enter to continue.\n")
            
            elif selection == 9:
                refresh_current_prices(portfolio, current_prices)
                roi_table(portfolio, current_prices)
                input("\nPress Enter to continue.\n")
            
            elif selection == 10:
                refresh_current_prices(portfolio, current_prices)
                diversification_table(portfolio, current_prices)
                input("\nPress Enter to continue.\n")
            
            elif selection == 11:
                break

if __name__ == "__main__":
    main()