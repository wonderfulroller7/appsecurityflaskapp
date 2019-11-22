DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT UNIQUE NOT NULL,
    phone_number TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO user(id, uname, phone_number, password) 
VALUES (1, 'admin', '12345678901', 'Administrator@1');