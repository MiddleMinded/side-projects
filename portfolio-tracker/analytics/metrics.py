from models.portfolio import Portfolio
from models.position import Position
from models.transaction import Transaction

def unrealized_gain(position: Position, current_price: float) -> float:
    """
    Calculate the difference between a position's current value and cost-basis.
    """
    return position.market_value(current_price) - position.cost_basis

def unrealized_gain_pct(position: Position, current_price: float) -> float:
    """
    Calculate the percent difference between a position's current value and 
    cost-basis.
    """
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

def position_weight(
        ticker: str, portfolio: Portfolio, current_prices: dict) -> float:
    """
    Calculates the weight of a single position relative to the total portfolio.
    """
    tmv = total_market_value(portfolio, current_prices)
    if tmv == 0.0:
        raise ValueError(f"portfolio value must be > 0.0, got {tmv!r}")
    
    current_price = current_prices[ticker]
    pv = portfolio.positions[ticker].market_value(current_price)
    pw = (pv / tmv) * 100

    return pw

def realized_gain_by_ticker(transactions: list[Transaction]):
    """Calculates the realized gain for each Position in the portfolio."""
    positions = {}
    gains = {}

    for txn in transactions:
        position = _get_or_create_position(txn.ticker, positions)

        if txn.action == "BUY":
            position.buy(txn.quantity, txn.price, txn.fees)
        elif txn.action == "SELL":
            if txn.ticker not in gains:
                gains[txn.ticker] = 0.0
            realized_gain = position.sell(txn.quantity, txn.price, txn.fees)
            gains[txn.ticker] += realized_gain
        else:
            raise ValueError(f"BUY or SELL is required, got {txn.action!r}")

    return gains

def _get_or_create_position(ticker: str, positions: dict) -> Position:
    """
    Return the Position for `ticker`, creating an empty one the first time 
    it's seen.
    """
    if ticker not in positions:
        positions[ticker] = Position(ticker)

    return positions[ticker]

def diversification_by_sector(
        portfolio: Portfolio, current_prices: dict) -> dict[str, float]:
    """Calculates the weight for each sector in the portfolio."""
    sectors = {}
    for ticker in portfolio.positions:
        sector = portfolio.sectors[ticker]
        if sector not in sectors:
            sectors[sector] = 0.0
        weight = position_weight(ticker, portfolio, current_prices)
        sectors[sector] += weight

    return sectors

def simple_roi(
        cost_basis: float, current_value: float, realized_gain: float) -> float:
    """
    Calculates the portfolio's ROI by combining realized and unrealized gains.
    """
    if cost_basis == 0.0:
        raise ValueError(f"cost basis must be > 0.0, got {cost_basis!r}")

    roi = (((current_value - cost_basis) + realized_gain) / cost_basis) * 100

    return roi

def time_weighted_return(period_returns: list[float]) -> float:
    """
    Compounds a series of per-period returns into one overall time-weighted 
    return.
    """
    twr = 1.0
    for r in period_returns:
        twr *= (1 + r)

    return (twr - 1) * 100

def total_portfolio_value(portfolio: Portfolio, current_prices: dict) -> float:
    """
    Sums and returns total market value and the portfolio cash account balance.
    """
    tmv = total_market_value(portfolio, current_prices)
    cash = portfolio.cash_account.balance

    return tmv + cash

