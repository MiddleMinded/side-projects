# Portfolio Tracker

A class-based Python stock portfolio tracker backed by SQLite, built as a
personal project for practicing object-oriented design and SQL. Tracks stock
transactions and cash flows (deposits, withdrawals, dividends), and derives
positions, cash balance, and portfolio metrics (unrealized/realized gains,
diversification, ROI) from those logs. `main.py` is a complete, numbered-menu
command-line REPL covering buying/selling stock, depositing/withdrawing cash,
recording dividends, and viewing portfolio reports.

## Usage

Install the project in editable mode, which also installs its dependencies
(`tabulate`, `bext`):

```bash
pip install -e .
```

Then run it from the project root:

```bash
python3 main.py
```

Activity is logged to `portfolio_tracker.log` at the project root.

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
- **A cancel/bail-out option for the input retry loops.** Every handler (buy,
  sell, deposit, withdraw, record dividend) currently has no way out of its
  `while True` retry loop except eventually giving valid input. Needs a
  convention designed once, consistently, across every handler — not patched
  into a single one.
- **A one-line pre-transaction preview.** Right after the ticker is entered in
  Buy/Sell, show the ticker, quantity currently held, and current price (from
  the session's price cache) before prompting for the rest of the transaction.
- **Live market-data API integration**, so prices don't have to be entered
  manually. This directly conflicts with the "no live market data" limitation
  above, so adopting it means deliberately revisiting that constraint, not
  quietly working around it.
- **A more informative oversell error message.** `Position.sell()`'s "quantity
  sold cannot be greater than quantity held" error currently only echoes back
  the quantity that was *requested*, not the quantity actually *held*.
- **List the tickers held in each sector** in the diversification report, not
  just the aggregate sector weight — needed to see what to actually target
  when rebalancing.
- **Dividend reinvestment (DRIP).** Automatically reinvest a recorded dividend
  back into the issuing company's stock. Requires linking a dividend to a
  ticker (`Portfolio.record_dividend()` is currently a pure cash event with no
  ticker at all) and a share price to reinvest at, so it also depends on the
  live market-data upgrade above.
- **Trading performance metrics**, to evaluate trades on an R-multiple basis:
  Gross R, Fee R, Realized R, capture ratio, cumulative R, average win/loss,
  win/loss rate, and expected value. Expected to add real complexity (each of
  these depends on defining a consistent "R"/risk unit per trade), but needed
  for assessing actual trading performance rather than just raw ROI.
