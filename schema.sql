CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT UNIQUE NOT NULL,
    phone_number TEXT NOT NULL,
    password TEXT NOT NULL
)