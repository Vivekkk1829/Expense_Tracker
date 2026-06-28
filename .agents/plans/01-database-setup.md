# Implementation Plan — Step 1: Database Setup

## Overview

Replace the stub in `database/db.py` with a complete SQLite implementation,
and wire the initialisation calls into `app.py` so the database is ready before any route is served.

This establishes the **data layer foundation** for Spendly.
All future steps (authentication, profile, expense CRUD) depend on this.

---

## Depends On

Nothing — this is Step 1.

---

## Proposed Changes

### Component: Database Layer

#### [MODIFY] `database/db.py`

The file currently contains only comments (6-line stub). It will be fully replaced with:

```python
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
    with conn:
        # Guard: skip if data already exists
        row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
        if row[0] > 0:
            conn.close()
            return

        # Insert demo user
        password_hash = generate_password_hash("demo123")
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = conn.execute(
            "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
        ).fetchone()["id"]

        # Insert 8 sample expenses (covering all 7 categories)
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
            """INSERT INTO expenses (user_id, amount, category, date, description)
               VALUES (?, ?, ?, ?, ?)""",
            sample_expenses,
        )
    conn.close()
```

**Key decisions:**
- `DB_PATH` resolved relative to project root -> always creates `expense_tracker.db` at root (matches `.gitignore`).
- `with conn:` used as context manager -> auto-commit on success, rollback on exception.
- `conn.close()` called explicitly after each function (raw connection, not a factory).
- `seed_db()` checks `COUNT(*) FROM users` and returns early if rows exist -> prevents duplicates on restarts.
- All SQL uses parameterized queries (`?` placeholders). No string formatting in SQL.

---

### Component: Application Bootstrap

#### [MODIFY] `app.py`

**Change 1 — Add import at top (after existing Flask import):**

```diff
  from flask import Flask, render_template
+ from database.db import get_db, init_db, seed_db
```

**Change 2 — Add startup wiring (before the `if __name__` block):**

```diff
+ # ------------------------------------------------------------------ #
+ # Database initialisation                                             #
+ # ------------------------------------------------------------------ #
+ with app.app_context():
+     init_db()
+     seed_db()
+
  if __name__ == "__main__":
      app.run(debug=True, port=5001)
```

> Using `app.app_context()` ensures Flask's application context is active,
> consistent with Flask best practices and forward-compatible with `flask.g` usage.

---

## Files Changed

| File | Action |
|---|---|
| `database/db.py` | MODIFY — replace stub with full implementation |
| `app.py` | MODIFY — add import + app-context startup calls |

## Files Created

None.

## New Dependencies

None — uses only `sqlite3` (stdlib) and `werkzeug.security` (already installed).

---

## Verification Plan

### Automated Tests
```bash
pytest
```

### Manual Verification

1. Start the app:
   ```bash
   venv\Scripts\activate
   python app.py
   ```
2. Confirm no errors in terminal output.
3. Confirm `expense_tracker.db` is created in project root.
4. Inspect DB contents:
   ```bash
   python -c "from database.db import get_db; c=get_db(); print(c.execute('SELECT * FROM users').fetchall()); print(c.execute('SELECT COUNT(*) FROM expenses').fetchone()[0])"
   ```
   Expected: 1 user row, expense count = 8.
5. Restart the app a second time — confirm no duplicate rows (seed guard works).

---

## Definition of Done

- [ ] `expense_tracker.db` is created on app startup
- [ ] `users` and `expenses` tables exist with correct schema and constraints
- [ ] Demo user (`demo@spendly.com`) has a hashed password
- [ ] 8 sample expenses exist across all categories
- [ ] No duplicate seed data on repeated restarts
- [ ] App starts without errors
- [ ] Foreign key enforcement is active
- [ ] All queries use parameterized SQL (no f-strings or % formatting in SQL)
