# Coffee Shop POS Backend

A Python-based backend system for a busy local Coffee Shop Point of Sale (POS) application. This system acts as a smart cash register to process sales, handle customer checkouts, and automatically track store inventory.

## Main Features
* **Fast Checkout** — Instantly calculates order totals and sales taxes so counter lines move quickly.
* **Menu Organization** — Groups coffee shop items into clean categories (like Espresso, Pastries, or Cold Beverages).
* **Live Stock Tracking** — Automatically lowers ingredient and item quantities the moment a drink or pastry is sold.
* **Payment Log Tracking** — Records payment methods (like Cards or Mobile Wallets) and links transactions directly to printed receipts.

## Database Core Structure
The system maps coffee shop workflows across 8 core database tables:
1. **Category** — Defines item groups and their specific sales tax rates.
2. **Product** — Stores item descriptions, base prices, current stock levels, and category/supplier links.
3. **Supplier** — Maintains contact information for wholesale ingredient distributors.
4. **Customer** — Keeps simple customer profiles for order histories and digital invoices.
5. **Sale** — Tracks transaction summaries, timestamps, and order grand totals.
6. **Sale Item** — Logs individual product items, prices, and quantities inside a single sale line.
7. **Payment** — Records processing channels (Card, Mobile Wallet) and monetary footprints.
8. **Receipt** — Links completed sales directly to paper voucher print records.

## Technology Stack
* **Language** — Python
* **Web Framework** — FastAPI
* **Database ORM** — SQLAlchemy
* **Database Migrations** — Alembic

## How to Run the Project
1. Activate your virtual environment: `source env/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the local FastAPI dev server: `fastapi dev main.py`

## Running Tests

### Local Testing
1. Install test dependencies:
   ```bash
   pip install -e .[test]
   # or
   pip install pytest pytest-asyncio httpx
   ```

2. Run the full test suite:
   ```bash
   pytest tests/ -v
   ```

3. Run tests with coverage:
   ```bash
   pytest tests/ -v --cov=app --cov-report=term-missing
   ```

4. Run specific test file:
   ```bash
   pytest tests/test_users.py -v
   ```

### Test Structure
- `tests/conftest.py` — Shared fixtures and test database setup (SQLite in-memory)
- `tests/test_users.py` — User CRUD operations and validation tests
- `tests/test_customers.py` — Customer CRUD operations and validation tests
- `tests/test_suppliers.py` — Supplier CRUD operations and validation tests
- `tests/test_categories.py` — Category CRUD operations and validation tests
- `tests/test_products.py` — Product CRUD operations and validation tests
- `tests/test_sales.py` — Sale CRUD operations and validation tests
- `tests/test_sale_items.py` — Sale Item CRUD operations and validation tests
- `tests/test_payments.py` — Payment CRUD operations and validation tests
- `tests/test_receipts.py` — Receipt CRUD operations and validation tests

### CI/CD
Tests run automatically on every push and pull request via GitHub Actions (`.github/workflows/ci.yml`). The workflow:
1. Checks out the repository
2. Sets up Python 3.10
3. Installs dependencies
4. Runs the complete test suite
5. Fails if any test fails
