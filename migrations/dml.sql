-- Accounts (10 уникальных аккаунтов)
INSERT INTO accounts (rating, nickname)
VALUES
    (1500, 'Player_1'),
    (1600, 'Player_2'),
    (1700, 'Player_3'),
    (1800, 'Player_4'),
    (1900, 'Player_5'),
    (2000, 'Player_6'),
    (2100, 'Player_7'),
    (2200, 'Player_8'),
    (2300, 'Player_9'),
    (2400, 'Player_10');

-- Users (10 пользователей, каждому аккаунту по пользователю)
INSERT INTO users (username, role, account_id, password_hash)
VALUES
    ('User_1', 'user', 1, 'hash_1'),
    ('User_2', 'user', 2, 'hash_2'),
    ('User_3', 'user', 3, 'hash_3'),
    ('User_4', 'user', 4, 'hash_4'),
    ('User_5', 'user', 5, 'hash_5'),
    ('User_6', 'user', 6, 'hash_6'),
    ('User_7', 'user', 7, 'hash_7'),
    ('User_8', 'user', 8, 'hash_8'),
    ('User_9', 'user', 9, 'hash_9'),
    ('User_10', 'user', 10, 'hash_10');

-- Heroes (добавим больше героев)
INSERT INTO heroes (name)
VALUES
    ('Axe'),
    ('Phantom Assassin'),
    ('Crystal Maiden'),
    ('Sniper'),
    ('Juggernaut'),
    ('Pudge'),
    ('Invoker'),
    ('Lina'),
    ('Drow Ranger'),
    ('Earthshaker');

-- Items (добавим больше предметов)
INSERT INTO items (name)
VALUES
    ('Black King Bar'),
    ('Blink Dagger'),
    ('Divine Rapier'),
    ('Aghanims Scepter'),
    ('Heart of Tarrasque'),
    ('Shadow Blade'),
    ('Desolator'),
    ('Battle Fury'),
    ('Manta Style'),
    ('Satanic');

-- Matches (3 матча)
INSERT INTO matches (start_time, duration, radiant_win, radiant_kills, dire_kills)
VALUES
    ('2024-12-16 18:00:00', '00:50:15', TRUE, 32, 28),
    ('2024-12-17 19:30:00', '01:02:30', FALSE, 40, 45),
    ('2024-12-18 20:15:00', '00:39:45', TRUE, 28, 15);

-- Players (по 10 уникальных игроков на каждый матч)
INSERT INTO players (account_id, match_id, kills, deaths, assistances, is_radiant, rating_change, hero_id)
VALUES
    -- Матч 1
    (1, 1, 10, 2, 12, TRUE, 50, 1),
    (2, 1, 8, 4, 10, TRUE, 40, 2),
    (3, 1, 7, 3, 8, TRUE, 30, 3),
    (4, 1, 5, 6, 6, TRUE, 20, 4),
    (5, 1, 3, 7, 4, TRUE, 10, 5),
    (6, 1, 12, 4, 15, FALSE, -10, 6),
    (7, 1, 9, 5, 10, FALSE, -20, 7),
    (8, 1, 6, 8, 8, FALSE, -30, 8),
    (9, 1, 4, 6, 5, FALSE, -40, 9),
    (10, 1, 3, 9, 2, FALSE, -50, 10),

    -- Матч 2
    (1, 2, 15, 3, 20, TRUE, 60, 1),
    (2, 2, 12, 2, 18, TRUE, 50, 2),
    (3, 2, 10, 5, 15, TRUE, 40, 3),
    (4, 2, 7, 4, 12, TRUE, 30, 4),
    (5, 2, 5, 6, 9, TRUE, 20, 5),
    (6, 2, 10, 7, 14, FALSE, -10, 6),
    (7, 2, 8, 9, 11, FALSE, -20, 7),
    (8, 2, 6, 5, 10, FALSE, -30, 8),
    (9, 2, 4, 8, 6, FALSE, -40, 9),
    (10, 2, 3, 10, 3, FALSE, -50, 10),

    -- Матч 3
    (1, 3, 18, 1, 25, TRUE, 70, 1),
    (2, 3, 14, 2, 20, TRUE, 60, 2),
    (3, 3, 12, 3, 18, TRUE, 50, 3),
    (4, 3, 10, 5, 15, TRUE, 40, 4),
    (5, 3, 8, 7, 12, TRUE, 30, 5),
    (6, 3, 7, 8, 10, FALSE, -10, 6),
    (7, 3, 5, 10, 8, FALSE, -20, 7),
    (8, 3, 4, 9, 6, FALSE, -30, 8),
    (9, 3, 3, 11, 5, FALSE, -40, 9),
    (10, 3, 2, 12, 4, FALSE, -50, 10);

-- Player Items (каждому игроку добавим минимум 2-3 предмета)
INSERT INTO player_items (player_id, item_id)
VALUES
    -- Матч 1
    (1, 1), (1, 4), (1, 6),
    (2, 2), (2, 5), (2, 7),
    (3, 3), (3, 6), (3, 8),
    (4, 1), (4, 7), (4, 9),
    (5, 2), (5, 8), (5, 10),
    (6, 3), (6, 4), (6, 7),
    (7, 1), (7, 6), (7, 10),
    (8, 2), (8, 5), (8, 9),
    (9, 3), (9, 4), (9, 8),
    (10, 1), (10, 7), (10, 9),

    -- Матч 2
    (11, 1), (11, 4), (11, 7),
    (12, 2), (12, 5), (12, 8),
    (13, 3), (13, 6), (13, 9),
    (14, 1), (14, 5), (14, 10),
    (15, 2), (15, 6), (15, 8),
    (16, 3), (16, 4), (16, 9),
    (17, 1), (17, 6), (17, 7),
    (18, 2), (18, 5), (18, 10),
    (19, 3), (19, 4), (19, 9),
    (20, 1), (20, 7), (20, 8),

    -- Матч 3
    (21, 2), (21, 4), (21, 6),
    (22, 3), (22, 5), (22, 7),
    (23, 1), (23, 6), (23, 9),
    (24, 2), (24, 7), (24, 10),
    (25, 3), (25, 5), (25, 8),
    (26, 1), (26, 4), (26, 7),
    (27, 2), (27, 6), (27, 9),
    (28, 3), (28, 5), (28, 10),
    (29, 1), (29, 6), (29, 8),
    (30, 2), (30, 7), (30, 9);
