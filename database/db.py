import sqlite3
import os
from werkzeug.security import generate_password_hash

# Resolve DB path relative to project root (one level above this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS. Safe to call repeatedly."""
    conn = get_db()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                description TEXT,
                created_at  TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
    conn.close()


def seed_db():
    """Insert demo data once. Skips if users table already has rows."""
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    if row[0] > 0:
        conn.close()
        return

    with conn:
        password_hash = generate_password_hash("demo123")
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = conn.execute(
            "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
        ).fetchone()["id"]

        sample_expenses = [
            (user_id, 12.50,  "Food",          "2026-06-01", "Lunch at cafe"),
            (user_id, 45.00,  "Transport",     "2026-06-03", "Monthly bus pass"),
            (user_id, 120.00, "Bills",         "2026-06-05", "Electricity bill"),
            (user_id, 30.00,  "Health",        "2026-06-10", "Pharmacy"),
            (user_id, 25.00,  "Entertainment", "2026-06-12", "Movie tickets"),
            (user_id, 80.00,  "Shopping",      "2026-06-15", "New shoes"),
            (user_id, 9.99,   "Other",         "2026-06-18", "Miscellaneous"),
            (user_id, 18.75,  "Food",          "2026-06-22", "Dinner with friends"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses,
        )
    conn.close()
