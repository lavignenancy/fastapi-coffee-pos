import os
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

ROOT_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if ROOT_APP not in sys.path:
    sys.path.insert(0, ROOT_APP)

from database import Base, get_db
from main import app
from models import (
    User, Customer, Supplier, Category, Product,
    Sale, SaleItem, Payment, Receipt
)

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    user = User(
        username="testuser",
        hashed_password="hashed_password",
        role="cashier",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_customer(db_session: Session) -> Customer:
    customer = Customer(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="123-456-7890",
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def test_supplier(db_session: Session) -> Supplier:
    supplier = Supplier(
        supplier_name="Coffee Beans Inc",
        contact_name="Jane Smith",
        phone="555-0100",
    )
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier


@pytest.fixture
def test_category(db_session: Session) -> Category:
    category = Category(
        category_name="Espresso",
        tax_rate=8.50,
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_product(
    db_session: Session,
    test_category: Category,
    test_supplier: Supplier,
) -> Product:
    product = Product(
        barcode="1234567890123",
        product_name="Espresso Shot",
        unit_price=2.50,
        stock_qty=100,
        category_id=test_category.id,
        supplier_id=test_supplier.id,
        is_active=True,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def test_sale(
    db_session: Session,
    test_user: User,
    test_customer: Customer,
) -> Sale:
    sale = Sale(
        total_amount=5.00,
        user_id=test_user.id,
        customer_id=test_customer.id,
    )
    db_session.add(sale)
    db_session.commit()
    db_session.refresh(sale)
    return sale


@pytest.fixture
def test_sale_item(
    db_session: Session,
    test_sale: Sale,
    test_product: Product,
) -> SaleItem:
    sale_item = SaleItem(
        sale_id=test_sale.id,
        product_id=test_product.id,
        quantity=2,
        item_price=2.50,
    )
    db_session.add(sale_item)
    db_session.commit()
    db_session.refresh(sale_item)
    return sale_item


@pytest.fixture
def test_payment(
    db_session: Session,
    test_sale: Sale,
) -> Payment:
    payment = Payment(
        sale_id=test_sale.id,
        payment_method="Card",
        amount_paid=5.00,
    )
    db_session.add(payment)
    db_session.commit()
    db_session.refresh(payment)
    return payment


@pytest.fixture
def test_receipt(
    db_session: Session,
    test_sale: Sale,
) -> Receipt:
    receipt = Receipt(
        sale_id=test_sale.id,
        receipt_number="RCP-001",
    )
    db_session.add(receipt)
    db_session.commit()
    db_session.refresh(receipt)
    return receipt