"""Class for handling database operations."""

import logging
import sqlite3
from pathlib import Path
from models.transaction import Transaction

logger = logging.getLogger(__name__)

class Database:
    """Owns the SQLite connection and confines all SQL to this module."""
    def __init__(self, path):
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row

        # no FKs in the schema yet; here so enforcement is on when 
        # transactions.ticker gets its FK
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()
        logger.info("database ready: %s", self.path)

    def close(self):
        self._conn.close()

    def _init_schema(self):
        schema_path = Path(__file__).parent / "schema.sql"
        contents = schema_path.read_text()
        self._conn.executescript(contents)
        self._conn.commit()

    def save_transaction(self, txn: Transaction) -> None:
        self._conn.execute(
            """
            INSERT INTO transactions (ticker, action, quantity, price, fees, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (txn.ticker, txn.action, txn.quantity, txn.price, txn.fees, txn.date.isoformat()),
        )
        self._conn.commit()
        logger.debug(
            "saved transaction: %s %s %s", txn.action, txn.quantity, txn.ticker
        )

    def get_transactions_for_ticker(self, ticker: str) -> list[Transaction]:
        rows = self._conn.execute("SELECT * FROM transactions WHERE ticker = ? ORDER BY date, id",
            (ticker,))
        transactions = [Transaction.from_row(row) for row in rows]
        return transactions

    def get_all_transactions(self) -> list[Transaction]:
        rows = self._conn.execute("SELECT * FROM transactions ORDER BY date, id")
        transactions = [Transaction.from_row(row) for row in rows]
        return transactions