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
- **Money is stored as `float`.** Binary floating point can't represent most
  decimal amounts exactly, so displayed values can look inconsistent by a
  cent. For example, a market value of `15.165` may display as `15.16` while
  the gain computed from it displays as `0.02`, because each figure is
  rounded independently from its own binary error. Totals are correct to
  within floating-point error, but not exact.

## Future upgrades

- **Store money as integer cents.** Replace `float` amounts with integer cents
  throughout the models, database schema, and metrics, and convert to dollars
  only at display time. This makes arithmetic exact and rounds each value once,
  fixing the display inconsistency described under Known limitations.
