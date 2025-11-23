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


-- Card table
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    card_number VARCHAR(16) NOT NULL,
    last4 CHAR(4) NOT NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    expiry_month SMALLINT NOT NULL CHECK (expiry_month BETWEEN 1 AND 12),
    expiry_year SMALLINT NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    network VARCHAR(20),
    issuer VARCHAR(50),
    daily_limit INTEGER,
    online_payments_enabled BOOLEAN,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP DEFAULT NULL
);



CREATE TABLE account_types (
    code VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE branch_codes (
    code VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


-- TESTING DATA -----------------------------------

INSERT INTO accounts (
    username,
    user_id,
    account_number,
    account_type,
    currency,
    balance,
    available_balance,
    credit_limit,
    interest_rate,
    last_activity,
    status,
    is_joint,
    branch_code,
    product_code
) VALUES (
    'zqaz1234@gmail.com',          
    1,                             
    'IT60X0542811101000000123456', 
    'checking',                    
    'EUR',                         
    1500.75,                       
    1450.75,                       
    500.00,                        
    1.25,                          
    NOW(),                         
    'active',                      
    FALSE,                         
    'BR001',                       
    'CHK001'                       
);


INSERT INTO cards (
    user_id,
    account_id,
    cardholder_name,
    card_type,
    network,
    issuer,
    card_number,
    last4,
    expiry_month,
    expiry_year,
    status,
    daily_limit,
    online_payments_enabled,
    created_at,
    last_used_at
) VALUES (
    1,                         -- user_id
    1,                         -- account_id (linked to the account above)
    'John D. Smith',           -- cardholder_name
    'debit',                   -- card_type
    'Visa',                    -- network
    'National Bank',           -- issuer
    '1234123412341234',      -- card_number
    '1234',                    -- last4 digits
    8,                         -- expiry_month
    2028,                      -- expiry_year
    'active',                  -- status
    2000.00,                   -- daily_limit
    TRUE,                      -- online_payments_enabled
    NOW(),
    NOW()                      -- last_used_at
);


INSERT INTO account_types (code, "name")
VALUES ('SA001', 'SAVING');
INSERT INTO account_types (code, "name")
VALUES ('CK001', 'CHECKING');

INSERT INTO branch_codes (code, "name")
VALUES ('NA001', 'NAPOLI_01');
INSERT INTO branch_codes (code, "name")
VALUES ('NA002', 'NAPOLI_02');
INSERT INTO branch_codes (code, "name")
VALUES ('RM001', 'ROMA_01');
