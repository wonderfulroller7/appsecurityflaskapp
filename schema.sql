DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT UNIQUE NOT NULL,
    phone_number TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO user(id, uname, phone_number, password) 
VALUES (1, 'admin', '12345678901', 'Administrator@1');

INSERT INTO user(id, uname, phone_number, password) 
VALUES (2, 'sb', '9292197847', 'welcome1');

INSERT INTO user(id, uname, phone_number, password) 
VALUES (3, 'sb6856', '9339752654', 'welcome1');

DROP TABLE IF EXISTS logs;

CREATE TABLE logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT NOT NULL,
    request TEXT NOT NULL,
    result TEXT NOT NULL
);

DROP TABLE IF EXISTS logins;

CREATE TABLE logins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT NOT NULL,
    request TEXT NOT NULL,
    access_time TEXT NOT NULL
);