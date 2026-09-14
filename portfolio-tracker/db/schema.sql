CREATE TABLE IF NOT EXISTS stocks (
    ticker      TEXT PRIMARY KEY NOT NULL,
    name        TEXT NOT NULL,
    sector      TEXT NOT NULL,
    exchange    TEXT NOT NULL
);

-- CHECK constraints below mirror Transaction.__post_init__ — change both together.
CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    action          TEXT NOT NULL CHECK (action IN ('BUY', 'SELL')),
    quantity        REAL NOT NULL CHECK (quantity > 0),
    price           REAL NOT NULL CHECK (price >= 0),
    fees            REAL NOT NULL DEFAULT 0.0 CHECK (fees >= 0),
    date            TEXT NOT NULL
);

-- CHECK constraints below mirror CashTransaction.__post_init__ — change both together.
CREATE TABLE IF NOT EXISTS cash_transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    flow_type       TEXT NOT NULL CHECK (flow_type IN (
        'DEPOSIT', 'WITHDRAWAL', 'TRADE_SETTLEMENT', 'DIVIDEND')
    ),
    amount          REAL NOT NULL CHECK (
        (flow_type NOT IN ('DEPOSIT', 'DIVIDEND') OR amount > 0)
        AND
        (flow_type != 'WITHDRAWAL' OR amount < 0)
    ),
    date            TEXT NOT NULL,
    description     TEXT NOT NULL DEFAULT "No description provided"
);

CREATE INDEX IF NOT EXISTS idx_transactions_ticker ON transactions(ticker);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_cash_transactions_date ON cash_transactions(date);