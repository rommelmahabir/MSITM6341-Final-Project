"""
data/db.py - SQLite data layer
Owner: Rommel

Opens the database connection and creates the three tables:
trips, expenses, rate_cache. Routes never touch the database
directly; they go through the service layer, which calls this module.
"""

import sqlite3

from flask import current_app, g

# The schema. "IF NOT EXISTS" makes it safe to run every time the app starts:
# existing tables (and their data) are left alone.
SCHEMA = """
CREATE TABLE IF NOT EXISTS trips (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    home_currency TEXT    NOT NULL,
    budget        REAL    NOT NULL CHECK (budget > 0),
    start_date    TEXT    NOT NULL,
    end_date      TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id          INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    amount           REAL    NOT NULL CHECK (amount > 0),
    currency         TEXT    NOT NULL,
    rate             REAL    NOT NULL,
    converted_amount REAL    NOT NULL,
    category         TEXT    NOT NULL,
    expense_date     TEXT    NOT NULL,
    used_cached_rate INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS rate_cache (
    base       TEXT NOT NULL,
    quote      TEXT NOT NULL,
    rate_date  TEXT NOT NULL,
    rate       REAL NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (base, quote, rate_date)
);
"""


def get_db():
    """Return one database connection per request, reusing it if already open."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row             # rows act like dicts: row["name"]
        g.db.execute("PRAGMA foreign_keys = ON")   # SQLite needs this for ON DELETE CASCADE
    return g.db


def close_db(error=None):
    """Close the connection at the end of each request (Flask calls this for us)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the tables if they do not exist yet."""
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


def init_app(app):
    """Hook the database into the Flask app. Called once from app.py."""
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()