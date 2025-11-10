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
    account_id INT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    card_number VARCHAR(20) UNIQUE NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    expiration_date DATE NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE account_types (
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

INSERT INTO account_types (code, "name")
VALUES ('SA001', 'SAVING');

INSERT INTO account_types (code, "name")
VALUES ('CK001', 'CHECKING');
