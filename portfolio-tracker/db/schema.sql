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
    date            TEXT NOT NULL,
    realized_gain   REAL
);

CREATE INDEX IF NOT EXISTS idx_transactions_ticker ON transactions(ticker);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);