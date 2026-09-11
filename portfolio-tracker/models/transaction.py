"""Class for tracking an individual transaction within the portfolio."""

import datetime
from dataclasses import dataclass

VALID_ACTIONS = ("BUY", "SELL")

@dataclass(frozen=True)
class Transaction:
    """
    An immutable record of the purchase or sale of a security: ticker, action, 
    quantity, price, fees, and date.
    """
    ticker: str
    action: str
    quantity: float
    price: float
    date: datetime.date
    fees: float = 0.0

    # __post_init__ guards below are mirrored by CHECK constraints in db/schema.sql
    # (transactions table) — change both together.
    def __post_init__(self) -> None:
        if not self.ticker:
            raise ValueError(f"ticker symbol required, got {self.ticker!r}")
        object.__setattr__(self, "ticker", self.ticker.upper())

        if not self.action:
            raise ValueError(
                f"a BUY or SELL action is required, got {self.action!r}")
        object.__setattr__(self, "action", self.action.upper())
        if self.action not in VALID_ACTIONS:
            raise ValueError(
                f"action must be BUY or SELL, got {self.action!r}")

        if self.quantity is None:
            raise ValueError(f"quantity is required, got {self.quantity!r}")
        if self.quantity <= 0:
            raise ValueError(f"quantity must be > 0, got {self.quantity!r}")

        if self.price is None:
            raise ValueError(f"price is required, got {self.price!r}")
        if self.price < 0:
            raise ValueError(f"price must be >= 0, got {self.price!r}")
        
        if not self.date:
            raise ValueError(f"date is required, got {self.date!r}")
        if not isinstance(self.date, datetime.date):
            raise TypeError(
                f"date must be a datetime.date, got {type(self.date).__name__!r}")

        if self.fees < 0:
            raise ValueError(
                f"fees must be greater than or equal to zero, got {self.fees!r}")

    @classmethod
    def from_row(cls, row) -> "Transaction":
        return cls(
            ticker=row["ticker"],
            action=row["action"],
            quantity=row["quantity"],
            price=row["price"],
            date=datetime.date.fromisoformat(row["date"]),
            fees=row["fees"]
        )
