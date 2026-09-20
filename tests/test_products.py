import pytest
from decimal import Decimal
from fastapi import status


class TestProductList:
    def test_list_products_empty(self, client):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_products_with_data(self, client, test_product):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["product_name"] == "Espresso Shot"
        assert data[0]["unit_price"] == "2.50"
        assert data[0]["stock_qty"] == 100
        assert data[0]["barcode"] == "1234567890123"
        assert data[0]["is_active"] is True


class TestProductGet:
    def test_get_product_success(self, client, test_product):
        response = client.get(f"/products/{test_product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_product.id
        assert data["product_name"] == "Espresso Shot"
        assert data["unit_price"] == "2.50"
        assert data["stock_qty"] == 100

    def test_get_product_not_found(self, client):
        response = client.get("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"


class TestProductCreate:
    def test_create_product_success(self, client, test_category, test_supplier):
        product_data = {
            "barcode": "9876543210987",
            "product_name": "Latte",
            "unit_price": "4.50",
            "stock_qty": 50,
            "category_id": test_category.id,
            "supplier_id": test_supplier.id,
            "is_active": True,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["product_name"] == "Latte"
        assert data["unit_price"] == "4.50"
        assert data["stock_qty"] == 50
        assert data["barcode"] == "9876543210987"
        assert data["category_id"] == test_category.id
        assert data["supplier_id"] == test_supplier.id
        assert data["is_active"] is True
        assert "id" in data

    def test_create_product_minimal_fields(self, client):
        product_data = {
            "product_name": "Simple Coffee",
            "unit_price": "2.00",
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["product_name"] == "Simple Coffee"
        assert data["unit_price"] == "2.00"
        assert data["stock_qty"] == 0
        assert data["barcode"] is None
        assert data["category_id"] is None
        assert data["supplier_id"] is None
        assert data["is_active"] is True

    def test_create_product_missing_required_fields(self, client):
        product_data = {"product_name": "Incomplete"}
        response = client.post("/products/", json=product_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_product_invalid_category_id(self, client):
        product_data = {
            "product_name": "Invalid Category Product",
            "unit_price": "3.00",
            "category_id": 999,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_product_invalid_supplier_id(self, client):
        product_data = {
            "product_name": "Invalid Supplier Product",
            "unit_price": "3.00",
            "supplier_id": 999,
        }
        response = client.post("/products/", json=product_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestProductUpdate:
    def test_update_product_success(self, client, test_product):
        update_data = {
            "product_name": "Double Espresso",
            "unit_price": "3.50",
            "stock_qty": 80,
        }
        response = client.put(f"/products/{test_product.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_name"] == "Double Espresso"
        assert data["unit_price"] == "3.50"
        assert data["stock_qty"] == 80
        assert data["barcode"] == "1234567890123"

    def test_update_product_partial(self, client, test_product):
        update_data = {"is_active": False}
        response = client.put(f"/products/{test_product.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False
        assert data["product_name"] == "Espresso Shot"

    def test_update_product_not_found(self, client):
        update_data = {"product_name": "Ghost Product"}
        response = client.put("/products/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"

    def test_update_product_invalid_category_id(self, client, test_product):
        update_data = {"category_id": 999}
        response = client.put(f"/products/{test_product.id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestProductDelete:
    def test_delete_product_success(self, client, test_product):
        response = client.delete(f"/products/{test_product.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/products/{test_product.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_not_found(self, client):
        response = client.delete("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"