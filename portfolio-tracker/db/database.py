"""Class for handling database operations."""

import logging
import sqlite3
from pathlib import Path
from models.cash_account import CashTransaction
from models.stock import Stock
from models.transaction import Transaction


logger = logging.getLogger(__name__)

class Database:
    """Owns the SQLite connection and confines all SQL to this module."""
    def __init__(self, path):
        """Open the SQLite connection, enable foreign keys, and init the schema."""
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()
        logger.info("database ready: %s", self.path)

    def close(self):
        """Close the database connection."""
        self._conn.close()

    def _init_schema(self):
        """Run schema.sql so every table exists."""
        schema_path = Path(__file__).parent / "schema.sql"
        contents = schema_path.read_text()
        self._conn.executescript(contents)
        self._conn.commit()

    def save_stock(self, stock: Stock) -> None:
        """Insert a new stock row."""
        self._conn.execute(
            """
            INSERT INTO stocks (ticker, name, sector, exchange) VALUES 
            (?, ?, ?, ?)
            """,
            (stock.ticker, stock.name, stock.sector, stock.exchange)
        )
        self._conn.commit()
        logger.debug(
            "Saved stock: %s (%s)", stock.name, stock.ticker
        )

    def save_transaction(self, txn: Transaction) -> None:
        """Insert a new transaction row."""
        self._conn.execute(
            """
            INSERT INTO transactions (ticker, action, quantity, price, fees, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (txn.ticker, txn.action, txn.quantity, txn.price, txn.fees, 
             txn.date.isoformat()),
        )
        self._conn.commit()
        logger.debug(
            "saved transaction: %s %s %s", txn.action, txn.quantity, txn.ticker
        )

    def save_cash_transaction(self, txn: CashTransaction) -> None:
        """Insert a new cash transaction row."""
        self._conn.execute(
            """
            INSERT INTO cash_transactions (flow_type, amount, date, description)
            VALUES (?, ?, ?, ?)
            """,
            (txn.flow_type, txn.amount, txn.date.isoformat(), txn.description)
        )
        self._conn.commit()
        logger.debug(
            "saved cash transaction: %s %s", txn.flow_type, txn.amount
        )

    def get_stock(self, ticker) -> Stock | None:
        """Return the Stock for `ticker`, or None if it hasn't been created yet."""
        rows = self._conn.execute("SELECT * FROM stocks WHERE ticker = ?",
                                  (ticker,))
        row = rows.fetchone()
        if row is None:
            return None

        stock = Stock.from_row(row)
        return stock

    def get_all_stocks(self) -> list[Stock]:
        """Return every stock, ordered by ticker."""
        rows = self._conn.execute("SELECT * FROM stocks ORDER BY ticker")
        stocks = [Stock.from_row(row) for row in rows]
        return stocks

    def get_transactions_for_ticker(self, ticker: str) -> list[Transaction]:
        """Return every transaction for `ticker`, ordered by date."""
        rows = self._conn.execute(
            "SELECT * FROM transactions WHERE ticker = ? ORDER BY date, id",
            (ticker,))
        transactions = [Transaction.from_row(row) for row in rows]
        return transactions

    def get_all_transactions(self) -> list[Transaction]:
        """Return every transaction, ordered by date."""
        rows = self._conn.execute("SELECT * FROM transactions ORDER BY date, id")
        transactions = [Transaction.from_row(row) for row in rows]
        return transactions

    def get_all_cash_transactions(self) -> list[CashTransaction]:
        """Return every cash transaction, ordered by date."""
        rows = self._conn.execute(
            "SELECT * FROM cash_transactions ORDER BY date, id")
        cash_transactions = [CashTransaction.from_row(row) for row in rows]
        return cash_transactions