"""Class for handling a single security position."""

from dataclasses import dataclass

@dataclass
class Position:
    """Class for managing a single position: ticker, quantity, average cost"""
    ticker: str
    quantity: float = 0.0
    avg_cost: float = 0.0

    def __post_init__(self) -> None:
        if not self.ticker:
            raise ValueError(f"ticker symbol required, got {self.ticker!r}")
        self.ticker = self.ticker.upper()

    def buy(self, quantity: float, price: float, fees: float = 0.0) -> None:
        """Mutates Position's quantity and average cost following a Buy action"""
        if quantity <= 0:
            raise ValueError(f"quantity must be > 0, got {quantity!r}")
        if price < 0:
            raise ValueError(f"price must be >= 0, got {price!r}")

        old_total_cost = self.quantity * self.avg_cost
        add_cost = quantity * price + fees
        new_quantity = self.quantity + quantity
        self.quantity = new_quantity
        self.avg_cost = (old_total_cost + add_cost) / new_quantity

    def sell(self, quantity: float, price: float, fees: float = 0.0) -> float:
        """Mutates Position's quantity and average cost following a Sell action"""
        if quantity <= 0:
            raise ValueError(f"quantity must be > 0, got {quantity!r}")
        if quantity > self.quantity:
            raise ValueError("quantity sold cannot be greater than quantity "
                             f"held, got {quantity!r}")
        if price < 0:
            raise ValueError(f"price must be >= 0, got {price!r}")

        proceeds = quantity * price - fees
        cost_of_shares_sold = quantity * self.avg_cost
        realized_gain = proceeds - cost_of_shares_sold

        if self.quantity - quantity == 0:
            self.avg_cost = 0.0

        self.quantity = self.quantity - quantity

        return realized_gain

    @property
    def cost_basis(self) -> float:
        """Computes total dollars in the position at average cost"""
        return self.quantity * self.avg_cost

    def market_value(self, current_price: float) -> float:
        """Computes market value based on current security price"""
        if current_price < 0:
            raise ValueError(f"price must be >= 0, got {current_price!r}")

        return self.quantity * current_price