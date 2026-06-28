# GEMINI.md — Project Intelligence File
# Spendly — Expense Tracker

## 🏗️ Project Overview

**Spendly** is a personal expense-tracking web application built as a step-by-step
student project. It allows users to register, log in, and manage (add/edit/delete)
their financial expenses.

---

## 🧰 Technology Stack

| Layer         | Technology                               | Version         |
|---------------|------------------------------------------|-----------------|
| **Backend**   | Python + Flask                           | 3.1.3           |
| **WSGI**      | Werkzeug                                 | 3.1.6           |
| **Database**  | SQLite (via Python stdlib `sqlite3`)   | built-in        |
| **Frontend**  | Jinja2 HTML Templates                    | (Flask bundled) |
| **Styling**   | Vanilla CSS (`static/css/style.css`)   | —               |
| **Scripting** | Vanilla JavaScript (`static/js/main.js`)| —              |
| **Fonts**     | Google Fonts — DM Serif Display, DM Sans | —               |
| **Testing**   | pytest + pytest-flask                    | 8.3.5 / 1.3.0   |

---

## 📁 Project Structure

```
Expense_tracker/
├── app.py                  # Flask app entry point; all route definitions
├── requirements.txt        # Python dependencies
├── GEMINI.md               # Project intelligence file (this file)
├── .gitignore              # Git exclusions (venv, db, cache, .env)
├── database/
│   ├── __init__.py
│   └── db.py               # DB helpers: get_db(), init_db(), seed_db() [student task]
├── templates/
│   ├── base.html           # Base layout (navbar, footer, font links)
│   ├── landing.html        # Public landing / home page
│   ├── login.html          # Login form
│   ├── register.html       # Registration form
│   ├── terms.html          # Terms & Conditions page
│   └── privacy.html        # Privacy Policy page
├── static/
│   ├── css/style.css       # Main stylesheet (~18 KB, Vanilla CSS)
│   └── js/main.js          # Frontend JavaScript entry point
└── venv/                   # Python virtual environment (git-ignored)
```

---

## 🛤️ Defined Routes

| Method | URL                     | Handler            | Status      |
|--------|-------------------------|--------------------|-------------|
| GET    | /                       | landing()          | ✅ Complete |
| GET    | /register               | register()         | ✅ Complete |
| GET    | /login                  | login()            | ✅ Complete |
| GET    | /terms                  | terms()            | ✅ Complete |
| GET    | /privacy                | privacy()          | ✅ Complete |
| GET    | /logout                 | logout()           | 🔲 Step 3  |
| GET    | /profile                | profile()          | 🔲 Step 4  |
| GET    | /expenses/add           | add_expense()      | 🔲 Step 7  |
| GET    | /expenses/<id>/edit     | edit_expense()     | 🔲 Step 8  |
| GET    | /expenses/<id>/delete   | delete_expense()   | 🔲 Step 9  |

---

## ⚙️ Operational Rules

### Running the App

```bash
# 1. Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python app.py                  # Starts on http://127.0.0.1:5001
```

### Development Rules

- **Port**: App runs on port 5001 (not default 5000).
- **Debug mode**: Always True during development (app.run(debug=True)).
- **Database**: SQLite — file is expense_tracker.db at project root (git-ignored).
- **Environment secrets**: Store in .env file (git-ignored). Never commit secrets.
- **Virtual env**: Always use venv/ — never install packages globally.

### Database Setup (Student Steps)

Complete database/db.py by implementing:

1. get_db() — Returns a SQLite connection with row_factory and foreign keys enabled.
2. init_db() — Creates all tables using CREATE TABLE IF NOT EXISTS.
3. seed_db() — Inserts sample/development data.

### Code Conventions

- All routes live in app.py.
- All HTML pages extend base.html using Jinja2 extends / block tags.
- CSS changes go to static/css/style.css only.
- JavaScript changes go to static/js/main.js only.
- Do not modify venv/, .git/, or __pycache__/.

### Testing

```bash
pytest          # Runs all tests via pytest-flask
```

---

## 🔲 Pending Student Implementation Steps

| Step | Task                                            |
|------|-------------------------------------------------|
| 1    | Implement database/db.py                        |
| 2    | Wire init_db() into app startup                 |
| 3    | Implement /logout route with session clear      |
| 4    | Implement /profile page                         |
| 5    | Implement expense listing (dashboard)           |
| 6    | Implement user authentication (login/register)  |
| 7    | Implement /expenses/add                         |
| 8    | Implement /expenses/<id>/edit                   |
| 9    | Implement /expenses/<id>/delete                 |

---

## 🚫 Git-Ignored Files

| File / Pattern       | Reason                        |
|----------------------|-------------------------------|
| venv/                | Virtual environment           |
| expense_tracker.db   | SQLite database file          |
| __pycache__/         | Python bytecode cache         |
| *.pyc, *.pyo         | Compiled Python files         |
| .env                 | Environment variables/secrets |
| .DS_Store            | macOS metadata                |
