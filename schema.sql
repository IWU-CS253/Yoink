CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT,
    blocked_user_ids TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id integer NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    condition TEXT,
    location TEXT,
    contact TEXT NOT NULL,
    image_path TEXT,
    status TEXT NOT NULL DEFAULT 'available',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_items_owner   ON items(owner_id);
CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at);