# UML Class Diagram

Covers the actual object model (`models/`, `db/`). `analytics/metrics.py`,
`reports/display.py`, `main.py`, and `handlers.py` are all plain functions,
not classes, so they're shown only as notes on the classes they call into,
not as class boxes of their own.

```mermaid
classDiagram
    class Stock {
        +str ticker
        +str name
        +str sector
        +str exchange
        +from_row(row) Stock
    }

    class Transaction {
        <<immutable>>
        +str ticker
        +str action
        +float quantity
        +float price
        +date date
        +float fees
        +from_row(row) Transaction
    }

    class Position {
        +str ticker
        +float quantity
        +float avg_cost
        +buy(quantity, price, fees)
        +sell(quantity, price, fees) float
        +cost_basis() float
        +market_value(current_price) float
    }

    class CashFlowType {
        <<enumeration>>
        DEPOSIT
        WITHDRAWAL
        TRADE_SETTLEMENT
        DIVIDEND
    }

    class CashTransaction {
        <<immutable>>
        +CashFlowType flow_type
        +float amount
        +date date
        +str description
        +from_row(row) CashTransaction
    }

    class CashAccount {
        +float balance
        +apply(delta)
    }

    class Portfolio {
        -Database _db
        +dict positions
        +CashAccount cash_account
        +dict sectors
        -_load_positions()
        -_load_cash_account()
        -_load_sectors()
        -_get_or_create_position(ticker) Position
        -_settle_trade(txn)
        +get_or_create_stock(ticker, name, sector, exchange) Stock
        +get_transactions() list
        +buy(ticker, quantity, price, date, fees) Position
        +sell(ticker, quantity, price, date, fees) float
        +deposit(amount, date, description)
        +withdraw(amount, date, description)
        +record_dividend(amount, date, description)
    }

    class Database {
        +Path path
        -_init_schema()
        +close()
        +save_stock(stock)
        +save_transaction(txn)
        +save_cash_transaction(txn)
        +get_stock(ticker) Stock
        +get_all_stocks() list
        +get_transactions_for_ticker(ticker) list
        +get_all_transactions() list
        +get_all_cash_transactions() list
    }

    Portfolio "1" *-- "many" Position : positions
    Portfolio "1" *-- "1" CashAccount : cash_account
    Portfolio ..> Database : uses (constructor-injected)
    Portfolio ..> Stock : creates/reads
    Portfolio ..> Transaction : creates
    Portfolio ..> CashTransaction : creates
    CashTransaction --> CashFlowType : flow_type
    Database ..> Stock : builds via from_row
    Database ..> Transaction : builds via from_row
    Database ..> CashTransaction : builds via from_row

    note for Portfolio "Called only by main.py / handlers.py (the CLI layer)\n— never Database directly ('the wall')."
    note for Position "analytics.metrics and reports.display take Position/\nPortfolio objects as plain function arguments — no\nclasses of their own."
```

## Notes

- **Composition** (`*--`): `Portfolio` owns its `Position`s and its single
  `CashAccount` — they have no existence or lifecycle outside a `Portfolio`.
- **Dependency** (`..>`): `Portfolio` *uses* `Database` but doesn't own its
  lifecycle — `Database` is constructed in `main()` and injected into
  `Portfolio`'s constructor, and `main()` is also what closes it. This is the
  constructor-injection / resource-ownership split documented in the handoff
  notes, not composition.
- `positions`/`sectors` are `dict`s (`ticker -> Position` / `ticker -> sector`
  respectively); the "many" multiplicity on the `Position` relationship
  captures that rather than the field's raw type.
- Dunder methods (`__post_init__`, `__init__`) are omitted — they're either
  implicit in the attribute list or, for `Portfolio`/`Database`, pure
  construction/assembly with no return value worth modeling separately.
