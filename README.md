# Coffee Shop POS Backend

A FastAPI-based backend for a coffee shop point-of-sale system. It manages sales, customer records, inventory, suppliers, and payments for a small retail operation.

## Features

- Fast order checkout and total calculation
- Product categories with tax handling
- Inventory tracking for sold items
- Customer, supplier, and payment records
- Receipt generation tied to each completed sale
- REST API endpoints for CRUD operations across the main entities

## Data model

The application is built around these core entities:

1. **Category** — product groups and tax settings
2. **Product** — item details, pricing, stock, and supplier/category links
3. **Supplier** — supplier contact details
4. **Customer** — customer information used in sales
5. **Sale** — transaction summary and totals
6. **Sale Item** — individual products within a sale
7. **Payment** — payment method and amount paid
8. **Receipt** — document linked to a completed sale

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite for the isolated test database

## Run locally

1. Activate the virtual environment:
   ```bash
   source .venv-1/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## Test setup

The test suite uses SQLite in memory and is isolated from the normal PostgreSQL development database.

### Run the full suite

```bash
pytest tests/ -v
```

### Run a single test file

```bash
pytest tests/test_users.py -v
```

### Test files

- tests/conftest.py
- tests/test_users.py
- tests/test_customers.py
- tests/test_suppliers.py
- tests/test_categories.py
- tests/test_products.py
- tests/test_sales.py
- tests/test_sale_items.py
- tests/test_payments.py
- tests/test_receipts.py

## CI

GitHub Actions runs the full test suite on pushes and pull requests through [.github/workflows/ci.yml](.github/workflows/ci.yml). The workflow installs dependencies, sets the test database URL, and fails when any test fails.
