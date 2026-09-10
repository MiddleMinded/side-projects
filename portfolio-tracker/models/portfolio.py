"""
Portfolio: the top-level holding that derives positions from the transaction log.
"""

from db.database import Database
from models.position import Position
from datetime import date
from models.transaction import Transaction
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

    def _load_positions(self):
        """
        Rebuild self.positions from scratch by replaying every recorded transaction.
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

    def _get_or_create_position(self, ticker: str) -> Position:
        """
        Return the Position for `ticker`, creating an empty one the first time 
        it's seen.
        """
        if ticker not in self.positions:
            self.positions[ticker] = Position(ticker)

        return self.positions[ticker]


    def buy
if __name__ == "__main__":
    db = Database(":memory:")

    txns = [
        Transaction("AAPL", "BUY",  1, 5,  date(2024, 1, 1)),
        Transaction("AAPL", "BUY",  1, 10, date(2024, 1, 2)),
        Transaction("AAPL", "SELL", 1, 12, date(2024, 1, 3)),
        Transaction("MSFT", "BUY",  2, 300, date(2024, 1, 4)),
    ]
    for txn in txns:
        db.save_transaction(txn)

    portfolio = Portfolio(db)

    for position in portfolio.positions.values():
        print(position)

    db.close()
