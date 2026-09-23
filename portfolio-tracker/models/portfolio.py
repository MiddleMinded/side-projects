"""
Portfolio: the top-level holding that derives positions from the transaction log.
"""

import datetime
import logging
from db.database import Database
from models.cash_account import CashFlowType, CashTransaction, CashAccount
from models.position import Position
from models.stock import Stock
from models.transaction import Transaction


logger = logging.getLogger(__name__)
class Portfolio:
    """
    Owns the open positions and the database they're rebuilt from.

    Positions are derived, never persisted directly. On construction the full
    transaction history is replayed to reconstruct each Position. Live trades go
    through buy() / sell(), which append to the log and update the matching
    Position in place, keeping memory and log consistent without a full reload.
    """

    def __init__(self, db: Database):
        self._db = db

        self._load_positions()
        self._load_cash_account()
        self._load_sectors()

    def _load_positions(self):
        """
        Rebuild self.positions from scratch by replaying every recorded 
        transaction.
        """
        self.positions = {}
        for txn in self._db.get_all_transactions():
            position = self._get_or_create_position(txn.ticker)

            if txn.action == "BUY":
                position.buy(txn.quantity, txn.price, txn.fees)
            elif txn.action == "SELL":
                position.sell(txn.quantity, txn.price, txn.fees)
            else:
                raise ValueError(f"BUY or SELL is required, got {txn.action!r}")

    def _load_cash_account(self):
        """
        Rebuild self.cash_account from scratch by replaying every recorded 
        transaction.
        """
        self.cash_account = CashAccount()
        for cash_txn in self._db.get_all_cash_transactions():
            self.cash_account.apply(cash_txn.amount)

    def _load_sectors(self):
        """Compiles a dictionary of all stocks with their associated sectors."""
        self.sectors = {}
        for stock in self._db.get_all_stocks():
            self.sectors[stock.ticker] = stock.sector

    def _get_or_create_position(self, ticker: str) -> Position:
        """
        Return the Position for `ticker`, creating an empty one the first time 
        it's seen.
        """
        if ticker not in self.positions:
            self.positions[ticker] = Position(ticker)

        return self.positions[ticker]

    def _settle_trade(self, txn: Transaction) -> None:
        """Calculates the delta of buy and sell transactions."""
        if txn.action == "BUY":
            delta = -(txn.quantity * txn.price + txn.fees)
            description = (f"Bought {txn.quantity} shares of {txn.ticker} at "
                           f"${txn.price}/share.")
        elif txn.action == "SELL":
            delta = txn.quantity * txn.price - txn.fees
            description = (f"Sold {txn.quantity} shares of {txn.ticker} at "
                                       f"${txn.price}/share.")
        else:
            raise ValueError(f"BUY or SELL was expected, got {txn.action!r}")

        cash_txn = CashTransaction(CashFlowType.TRADE_SETTLEMENT, delta, 
                                   txn.date, description)
        self.cash_account.apply(delta)
        logger.info("settled trade: %s %s %s", txn.action, txn.ticker, delta)

        self._db.save_cash_transaction(cash_txn)

    def get_or_create_stock(self, ticker, name, sector, exchange) -> Stock:
        """
        Return the Stock for `ticker`, creating a new one the first time 
        it's seen.
        """
        stock = self._db.get_stock(ticker)
        if stock is None:
            stock = Stock(ticker, name, sector, exchange)
            self._db.save_stock(stock)
            self.sectors[stock.ticker] = stock.sector

        return stock

    def get_transactions(self) -> list[Transaction]:
        """A public function for retrieving all stock transactions."""
        return self._db.get_all_transactions()

    def buy(self, ticker: str, quantity: float, price: float, 
        date: datetime.date, fees: float =0.0) -> Position:
        """
        Record a buy: persist the transaction, then update the matching 
        Position.
        """
        txn = Transaction(ticker, "BUY", quantity, price, date, fees)
        self._settle_trade(txn)

        self._db.save_transaction(txn)

        position = self._get_or_create_position(txn.ticker)
        position.buy(quantity, price, fees)
        logger.info("buy %s %s @ %s", quantity, txn.ticker, price)

        return position

    def sell(self, ticker: str, quantity: float, price: float, 
            date: datetime.date, fees: float =0.0) -> float:
        """
        Record a sell: mutate the matching Position, then persist the 
        transaction.
        """
        txn = Transaction(ticker, "SELL", quantity, price, date, fees)
        position = self._get_or_create_position(txn.ticker)

        realized_gain = position.sell(quantity, price, fees)
        self._settle_trade(txn)
        logger.info("sell %s %s @ %s, realized_gain=%s", quantity, txn.ticker, 
                    price, realized_gain)
      
        self._db.save_transaction(txn)
        
        return realized_gain

    def deposit(self, amount: float, date: datetime.date, 
                description: str = "No description provided") -> None:
        """
        Create a cash deposit transaction in the database and adjust 
        cash_account.
        """
        cash_txn = CashTransaction(
            CashFlowType.DEPOSIT, amount, date, description)
        self.cash_account.apply(amount)
        logger.info("deposit created: %s %s", date, amount)

        self._db.save_cash_transaction(cash_txn)

    def withdraw(self, amount: float, date: datetime.date, 
                    description: str = "No description provided") -> None:
        """
        Create a cash withdrawal transaction in the database and adjust 
        cash_account.
        """
        amount = -amount
        cash_txn = CashTransaction(
            CashFlowType.WITHDRAWAL, amount, date, description)
        self.cash_account.apply(amount)
        logger.info("withdrawal created: %s %s", date, amount)

        self._db.save_cash_transaction(cash_txn)

    def record_dividend(self, amount: float, date: datetime.date, 
                description: str = "No description provided") -> None:
        """
        Create a cash dividend transaction in the database and adjust 
        cash_account.
        """
        cash_txn = CashTransaction(
            CashFlowType.DIVIDEND, amount, date, description)
        self.cash_account.apply(amount)
        logger.info("dividend created: %s %s", date, amount)

        self._db.save_cash_transaction(cash_txn)



if __name__ == "__main__":
    db = Database(":memory:")
    portfolio = Portfolio(db)
    portfolio.deposit(100, datetime.date(2026, 9, 15), "Cash in")
    portfolio.withdraw(50, datetime.date(2026, 9, 16), "Cash out")
    portfolio.record_dividend(5, datetime.date(2026, 9, 17), "Dividend in")
    print(portfolio.cash_account.balance)
    print(db.get_all_cash_transactions())
    portfolio.withdraw(1000, datetime.date(2026, 9, 18), "Overdraw test")