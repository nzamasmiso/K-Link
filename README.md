# K-Link MVP

A responsive Flask prototype for discovering local businesses and exploring order-ahead workflows.

## Included
- Responsive home page and category filters
- Search by business name, category, description, and area
- Sample business cards and detail pages
- SQLite database initialization for the first business records
- Health endpoint at `/health`
- Basic SEO description and mobile-friendly layout

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Important prototype notes
- The business listings and photos are demo content, not verified real businesses.
- Order submission, authentication, owner dashboards, map API integration, and production database workflows are not implemented yet.
- The current home page uses sample data to keep the first visual prototype easy to run. Next step is to make listings fully database-driven and add owner registration and order requests.
- Before public deployment, add CSRF protection, input validation, secure session configuration, migrations, logging, rate limiting, privacy notices, and tests.
