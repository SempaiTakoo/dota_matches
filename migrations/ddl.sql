-- Таблица аккаунтов пользователей
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    rating INTEGER CHECK (rating >= 0),
    nickname VARCHAR NOT NULL
);

-- Таблица героев
CREATE TABLE heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

-- Таблица предметов
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

-- Таблица матчей
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    duration TIME NOT NULL CHECK (duration <= '05:00:00'),
    radiant_win BOOLEAN NOT NULL,
    radiant_kills INTEGER NOT NULL CHECK (radiant_kills >= 0),
    dire_kills INTEGER NOT NULL CHECK (dire_kills >= 0)
);

-- Таблица игроков (участников конкретного матча)
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
    match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    hero_id INTEGER NOT NULL REFERENCES heroes(id) ON DELETE SET NULL,
    kills INTEGER NOT NULL CHECK (kills >= 0),
    deaths INTEGER NOT NULL CHECK (deaths >= 0),
    assistances INTEGER NOT NULL CHECK (assistances >= 0),
    is_radiant BOOLEAN NOT NULL,
    rating_change INTEGER DEFAULT 0 CHECK (rating_change BETWEEN -100 AND 100)
);

-- Таблица связи игрока и предметов
CREATE TABLE player_items (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE
);

-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role VARCHAR NOT NULL,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
    username VARCHAR NOT NULL UNIQUE
);

-- Функция для обновления рейтинга аккаунта
CREATE OR REPLACE FUNCTION update_account_rating()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.account_id IS NOT NULL THEN
        UPDATE accounts
        SET rating = rating + NEW.rating_change
        WHERE id = NEW.account_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер, вызывающий функцию при добавлении записи в players
CREATE TRIGGER update_account_rating_trigger
AFTER INSERT ON players
FOR EACH ROW
EXECUTE FUNCTION update_account_rating();
