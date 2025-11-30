\c transactiondb

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    s_account_id INTEGER NOT NULL,
    r_account_id INTEGER,
    s_account_number VARCHAR NOT NULL,
    r_account_number VARCHAR NOT NULL,
    s_user_id INTEGER NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR DEFAULT 'PENDING',
    reject_reason VARCHAR,
    description VARCHAR,
    is_internal BOOLEAN,
    is_same_user BOOLEAN,
    is_blocking_account BOOLEAN
);

-- Useful indexes
CREATE INDEX idx_transactions_s_account_id ON transactions (s_account_id);
CREATE INDEX idx_transactions_r_account_id ON transactions (r_account_id);
CREATE INDEX idx_transactions_s_user_id ON transactions (s_user_id);
CREATE INDEX idx_transactions_timestamp ON transactions (created_at);
