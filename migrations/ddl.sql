CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    rating INTEGER CHECK (rating >= 0),
    nickname VARCHAR NOT NULL
);

CREATE TABLE heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    duration TIME NOT NULL CHECK (duration <= '05:00:00'),
    radiant_win BOOLEAN NOT NULL,
    radiant_kills INTEGER NOT NULL CHECK (radiant_kills >= 0),
    dire_kills INTEGER NOT NULL CHECK (dire_kills >= 0)
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
    match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    hero_id INTEGER NOT NULL REFERENCES heroes(id) ON DELETE SET NULL,
    kills INTEGER NOT NULL CHECK (kills >= 0),
    deaths INTEGER NOT NULL CHECK (deaths >= 0),
    assistances INTEGER NOT NULL CHECK (assistances >= 0),
    is_radiant BOOLEAN NOT NULL,
    rating_change INTEGER DEFAULT 0
);

CREATE TABLE player_items (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role VARCHAR NOT NULL,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
    username VARCHAR NOT NULL UNIQUE
);
