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
            "AVERAGE COST ($)": position.avg_cost,
            "MARKET VALUE ($)": market_value,
            "UNREALIZED GAIN ($)": unrealized_gain
        }
        table_data.append(position_data)

    tmv = metrics.total_market_value(portfolio, current_prices)
    ug = metrics.total_unrealized_gain(portfolio, current_prices)
    totals_row = {
            "TICKER": "-TOTAL-",
            "SHARES": "",
            "AVERAGE COST ($)": "",
            "MARKET VALUE ($)": tmv,
            "UNREALIZED GAIN ($)": ug
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
        "AMOUNT ($)": portfolio.cash_account.balance
        },
        {
        "CATEGORY": "Total Portfolio Value",
        "AMOUNT ($)": metrics.total_portfolio_value(portfolio, current_prices)
        }]

    print(tabulate(table_data,
            headers="keys",
            tablefmt="grid",
            floatfmt=("", ".2f")))

def roi_table(portfolio: Portfolio, current_prices: dict) -> None:
    """Prints a table with the portfolio's simple ROI."""
    transactions = portfolio.get_transactions()
    realized_gains = metrics.realized_gain_by_ticker(transactions)
    total_rg = 0.0
    total_rg = sum(realized_gains.values())

    tmv = metrics.total_market_value(portfolio, current_prices)
    tcb = metrics.total_cost_basis(portfolio)
    roi = metrics.simple_roi(tcb, tmv, total_rg)

    table_data = [{
            "CATEGORY": "Cost Basis ($)",
            "AMOUNT": tcb
            },
            {
            "CATEGORY": "Market Value ($)",
            "AMOUNT": tmv
            },
            {
            "CATEGORY": "Return-On-Investment (%)",
            "AMOUNT": roi
            }]

    print(tabulate(table_data,
            headers="keys",
            tablefmt="grid",
            floatfmt=(".2f", ".2f")))

def diversification_table(portfolio: Portfolio, current_prices: dict) -> None:
    """Prints a table with the current portfolio diversification by sector."""
    sectors = []
    sector_dict = metrics.diversification_by_sector(portfolio, current_prices)
    for sector, weight in sector_dict.items():
        temp_dict = {
            "SECTOR": sector,
            "WEIGHT (%)": weight
        }
        sectors.append(temp_dict)

    sorted_sectors = sorted(
        sectors, key=lambda row: row["WEIGHT (%)"], reverse=True)

    print(tabulate(sorted_sectors, 
        headers="keys",
        tablefmt="grid",
        floatfmt=("", ".2f")))

def portfolio_summary(portfolio: Portfolio, current_prices: dict) -> None:
    """
    Prints tables containing the current portfolio positions and the cash 
    summary.
    """
    print("\n---CURRENT POSITIONS---")
    positions_table(portfolio, current_prices)
    print("\n---PORTFOLIO VALUE---")
    cash_summary(portfolio, current_prices)
    print("\n---PORTFOLIO PERFORMANCE---")
    roi_table(portfolio, current_prices)
    print("\n---SECTOR DIVERSIFICATION---")
    diversification_table(portfolio, current_prices)