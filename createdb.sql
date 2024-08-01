CREATE TABLE IF NOT EXISTS profiles (
    tg_id BIGINT PRIMARY KEY,
    username VARCHAR(32),
    balance DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    buyer_tg_id BIGINT NOT NULL,
    account_type VARCHAR(64) CHECK (account_type IN ('discord', 'twitter')), -- discord | twitter
    amount INTEGER NOT NULL, -- кол-во акков
    total_sum DECIMAL(10, 2) NOT NULL,
    created TEXT NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (buyer_tg_id) REFERENCES profile (tg_id)
);
