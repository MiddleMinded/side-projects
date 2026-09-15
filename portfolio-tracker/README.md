# Portfolio Tracker

A class-based Python stock portfolio tracker backed by SQLite. Tracks stock
transactions and cash flows, and derives positions, cash balance, and
portfolio metrics (unrealized/realized gains, diversification, ROI) from
those logs.

## Known limitations

- **No live market data.** There is no integration with a pricing API.
  Anywhere a "current price" is needed (e.g. `analytics.metrics.
  total_market_value`), it must be supplied by the caller.
- **No historical price tracking, so `time_weighted_return` can't be fed
  real data yet.** A true time-weighted return needs the portfolio's market
  value at each cash-flow boundary date, which requires historical prices
  that this project doesn't store anywhere. `analytics.metrics.
  time_weighted_return` itself is complete — it correctly compounds a list
  of period returns — but nothing in the project can currently produce that
  list from real data. For now it can only be exercised with hand-supplied
  example returns.
