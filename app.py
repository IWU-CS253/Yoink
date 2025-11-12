from flask import Flask, g
import sqlite3
import os

app = Flask(__name__)

# Override config from an environment variable 
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
))

# Manually setup the secret key from a .env file to increase security
app.secret_key = os.getenv("SECRET_KEY")

def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Initialized the database")

def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)