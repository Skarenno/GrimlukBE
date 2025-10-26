\c accountdb

-- 1. Accounts table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    user_id INTEGER NOT NULL,
    account_number VARCHAR(34) UNIQUE NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    balance NUMERIC(15, 2) DEFAULT 0.00,
    available_balance NUMERIC(15, 2) DEFAULT 0.00,
    credit_limit NUMERIC(15, 2) DEFAULT 0.00,
    interest_rate NUMERIC(5, 2) DEFAULT 0.00,
    opened_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'active',
    is_joint BOOLEAN DEFAULT FALSE,
    branch_code VARCHAR(10),
    product_code VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    CONSTRAINT accounts_userid_idx UNIQUE (user_id, account_number)
);

CREATE INDEX idx_accounts_user_id ON accounts (user_id);
CREATE INDEX idx_accounts_username ON accounts (username);

-- 2. Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    description VARCHAR,
    target_account VARCHAR(20)
);

CREATE INDEX idx_transactions_account_id ON transactions (account_id);
