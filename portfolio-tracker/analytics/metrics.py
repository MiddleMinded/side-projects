from models.portfolio import Portfolio
from models.position import Position
from models.transaction import Transaction

def unrealized_gain(position: Position, current_price: float) -> float:
    """Calculate the difference between a position's current value and cost-basis."""
    return position.market_value(current_price) - position.cost_basis

def unrealized_gain_pct(position: Position, current_price: float) -> float:
    """Calculate the percent difference between a position's current value and cost-basis."""
    if position.cost_basis == 0.0:
        raise ValueError(f"expected cost-basis > 0.0, got {position.cost_basis}")

    gain = unrealized_gain(position, current_price)

    return (gain / position.cost_basis) * 100

def total_market_value(portfolio: Portfolio, current_prices: dict) -> float:
    """Calculate the total market value of the portfolio."""
    tmv = 0.0
    for ticker, position in portfolio.positions.items():
        current_price = current_prices[ticker]
        market_value = position.market_value(current_price)
        tmv = tmv + market_value

    return tmv

def total_cost_basis(portfolio: Portfolio) -> float:
    """Calculate the total cost basis of the portfolio."""
    tcb = 0.0
    for position in portfolio.positions.values():
        cost_basis = position.cost_basis
        tcb = tcb + cost_basis

    return tcb

def total_unrealized_gain(portfolio: Portfolio, current_prices: dict) -> float:
    """Calculate the total unrealized gain of the portfolio."""
    tmv = total_market_value(portfolio, current_prices)
    tcb = total_cost_basis(portfolio)

    return tmv - tcb

def position_weight(ticker: str, portfolio: Portfolio, current_prices: dict) -> float:
    """Calculates the weight of a single position relative to the total portfolio."""
    tmv = total_market_value(portfolio, current_prices)
    if tmv == 0.0:
        raise ValueError(f"portfolio value must be > 0.0, got {tmv!r}")
    
    current_price = current_prices[ticker]
    pv = portfolio.positions[ticker].market_value(current_price)
    pw = (pv / tmv) * 100

    return pw

def realized_gain_by_ticker(transactions: list[Transaction]):
    """
    """
    positions = {}
    for txn in transactions():
        ticker = txn.ticker
        position = self._get_or_create_position(ticker)

        if txn.action == "BUY":
            position.buy(txn.quantity, txn.price, txn.fees)
        elif txn.action == "SELL":
            position.sell(txn.quantity, txn.price, txn.fees)
        else:
            raise ValueError(f"BUY or SELL is required, got {txn.action!r}")