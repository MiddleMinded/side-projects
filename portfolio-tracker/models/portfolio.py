"""
Portfolio: the top-level holding that derives positions from the transaction log.
"""

import datetime
import logging
from db.database import Database
from models.position import Position
from models.transaction import Transaction
from models.cash_account import CashFlowType, CashTransaction, CashAccount

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

    def _load_positions(self):
        """
        Rebuild self.positions from scratch by replaying every recorded 
        transaction.
        """
        self.positions = {}
        for txn in self._db.get_all_transactions():
            ticker = txn.ticker
            position = self._get_or_create_position(ticker)

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

    def _get_or_create_position(self, ticker: str) -> Position:
        """
        Return the Position for `ticker`, creating an empty one the first time 
        it's seen.
        """
        if ticker not in self.positions:
            self.positions[ticker] = Position(ticker)

        return self.positions[ticker]

    def buy(self, ticker: str, quantity: float, price: float, 
            date: datetime.date, fees: float =0.0) -> Position:
        """
        Record a buy: persist the transaction, then update the matching Position.
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
        Record a sell: mutate the matching Position, then persist the transaction.
        """
        txn = Transaction(ticker, "SELL", quantity, price, date, fees)
        position = self._get_or_create_position(txn.ticker)

        realized_gain = position.sell(quantity, price, fees)
        self._settle_trade(txn)
        logger.info("sell %s %s @ %s, realized_gain=%s", quantity, txn.ticker, 
                    price, realized_gain)
      
        self._db.save_transaction(txn)
        
        return realized_gain

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
