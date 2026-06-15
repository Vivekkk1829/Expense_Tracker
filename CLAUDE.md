# Spendly Project Guidelines

## Build and Run Commands
- **Run the Flask application**: `python app.py` (runs on port `5001` with debug mode enabled)
- **Install dependencies**: `pip install -r requirements.txt`
- **Run tests**: `pytest`

## Coding & Style Guidelines
- **Framework**: Flask (Python backend) with Jinja2 templates, styled with Vanilla CSS.
- **Database**: SQLite (managed via SQLite connections with `row_factory` and foreign keys enabled in `database/db.py`).
- **Styling & Theme**:
  - Theme is based on a clean, warm-paper aesthetic with a forest green accent.
  - Page-specific styles should be defined within a `<style>` block in the page template, or inside page-specific stylesheets using the standard design tokens.
  - Always use CSS variables from `static/css/style.css` for colors, fonts, margins, and sizes:
    - `--max-width`: `1200px`
    - `--ink`: `#0f0f0f` (primary text)
    - `--ink-soft`: `#2d2d2d`
    - `--ink-muted`: `#6b6b6b`
    - `--ink-faint`: `#a0a0a0`
    - `--paper`: `#f7f6f3` (background)
    - `--paper-warm`: `#f0ede6`
    - `--paper-card`: `#ffffff`
    - `--accent`: `#1a472a` (forest green brand color)
    - `--accent-light`: `#e8f0eb`
    - `--accent-2`: `#c17f24` (gold secondary color)
    - `--accent-2-light`: `#fdf3e3`
    - `--font-display`: `'DM Serif Display', Georgia, serif`
    - `--font-body`: `'DM Sans', system-ui, sans-serif`
- **HTML Layout**:
  - Page templates (e.g., `templates/terms.html`, `templates/privacy.html`) must extend `templates/base.html`.
  - The footer in `templates/base.html` must include links to the `Terms and Conditions` page (`/terms`) and the `Privacy Policy` page (`/privacy`).
  - These links must be vertically aligned by placing a `<br>` tag between them:
    ```html
    <div class="footer-links">
        <a href="/terms">Terms and Conditions</a><br>
        <a href="/privacy">Privacy Policy</a>
    </div>
    ```
- **Routing Rules**:
  - Define Flask routes directly in `app.py`.
  - Placeholder routes (to be completed by students) must be grouped under the designated separator block:
    ```python
    # ------------------------------------------------------------------ #
    # Placeholder routes — students will implement these                  #
    # ------------------------------------------------------------------ #
    ```

## Development & Git Workflow
- Verify link changes by running the local Flask server on port 5001 prior to committing.
- Commit changes with descriptive messages describing the page or feature added (e.g. `Terms and Conditions Page added`, `Privacy Policy Page added`).
