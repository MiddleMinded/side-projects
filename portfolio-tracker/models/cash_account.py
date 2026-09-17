"""Class for handling cash flow between transactions and the database."""

import datetime
import enum
from dataclasses import dataclass

class CashFlowType(str, enum.Enum):
    """Class for initializing cash flow members."""
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRADE_SETTLEMENT = "TRADE_SETTLEMENT"
    DIVIDEND = "DIVIDEND"

@dataclass(frozen=True)
class CashTransaction:
    """
    Class for managing a single cash transaction: type, amount, date, description
    """
    flow_type: CashFlowType
    amount: float
    date: datetime.date
    description: str = "No description provided"

    def __post_init__(self) -> None:
        if not isinstance(self.flow_type, CashFlowType):
            raise TypeError("expected DEPOSIT, WITHDRAWAL, TRADE_SETTLEMENT or "
                            f"DIVIDEND, got {self.flow_type!r}")
        if self.flow_type in (
            CashFlowType.DEPOSIT, CashFlowType.DIVIDEND) and self.amount <= 0:
            raise ValueError(f"amount must be > 0, got {self.amount!r}")
        if self.flow_type == CashFlowType.WITHDRAWAL and self.amount >= 0:
            raise ValueError(f"amount must be < 0, got {self.amount!r}")

    @classmethod
    def from_row(cls, row) -> "CashTransaction":
        return cls(
            flow_type=CashFlowType(row["flow_type"]),
            amount=row["amount"],
            date=datetime.date.fromisoformat(row["date"]),
            description=row["description"]
        )

@dataclass
class CashAccount:
    """Class for managing the current balance of the portfolio"""
    balance: float = 0.0

    def apply(self, delta: float) -> None:
        "Mutates the portfolio's cash account balance"
        new_balance = self.balance + delta
        if new_balance < 0:
            raise ValueError(
                f"balance cannot be less than zero, got {new_balance!r}")

        self.balance = new_balance

if __name__ == "__main__":
    cash = CashAccount()
    cash.apply(100)
    cash.apply(-30)
    print(cash.balance)
    cash.apply(-100)