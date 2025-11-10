CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    email TEXT,
    password TEXT

);
CREATE TABLE IF NOT EXISTS items (
    name TEXT PRIMARY KEY,
    status TEXT,
    image_url TEXT,
    Description TEXT,
    time_created TEXT
);
