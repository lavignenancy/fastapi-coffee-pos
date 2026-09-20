import pytest
from decimal import Decimal
from fastapi import status


class TestSaleList:
    def test_list_sales_empty(self, client):
        response = client.get("/sales/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_sales_with_data(self, client, test_sale):
        response = client.get("/sales/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["total_amount"] == "5.00"
        assert data[0]["user_id"] == test_sale.user_id
        assert data[0]["customer_id"] == test_sale.customer_id


class TestSaleGet:
    def test_get_sale_success(self, client, test_sale):
        response = client.get(f"/sales/{test_sale.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_sale.id
        assert data["total_amount"] == "5.00"
        assert data["user_id"] == test_sale.user_id
        assert data["customer_id"] == test_sale.customer_id
        assert "timestamp" in data

    def test_get_sale_not_found(self, client):
        response = client.get("/sales/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale not found"


class TestSaleCreate:
    def test_create_sale_success(self, client, test_user, test_customer):
        sale_data = {
            "total_amount": "10.00",
            "user_id": test_user.id,
            "customer_id": test_customer.id,
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["total_amount"] == "10.00"
        assert data["user_id"] == test_user.id
        assert data["customer_id"] == test_customer.id
        assert "id" in data
        assert "timestamp" in data

    def test_create_sale_without_user(self, client, test_customer):
        sale_data = {
            "total_amount": "7.50",
            "customer_id": test_customer.id,
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["total_amount"] == "7.50"
        assert data["user_id"] is None
        assert data["customer_id"] == test_customer.id

    def test_create_sale_without_customer(self, client, test_user):
        sale_data = {
            "total_amount": "3.00",
            "user_id": test_user.id,
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["total_amount"] == "3.00"
        assert data["user_id"] == test_user.id
        assert data["customer_id"] is None

    def test_create_sale_minimal_fields(self, client):
        sale_data = {
            "total_amount": "1.00",
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["total_amount"] == "1.00"
        assert data["user_id"] is None
        assert data["customer_id"] is None

    def test_create_sale_invalid_user_id(self, client, test_customer):
        sale_data = {
            "total_amount": "5.00",
            "user_id": 999,
            "customer_id": test_customer.id,
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user_id or customer_id" in response.json()["detail"]

    def test_create_sale_invalid_customer_id(self, client, test_user):
        sale_data = {
            "total_amount": "5.00",
            "user_id": test_user.id,
            "customer_id": 999,
        }
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user_id or customer_id" in response.json()["detail"]

    def test_create_sale_missing_required_fields(self, client):
        sale_data = {}
        response = client.post("/sales/", json=sale_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSaleUpdate:
    def test_update_sale_success(self, client, test_sale):
        update_data = {"total_amount": "15.00"}
        response = client.put(f"/sales/{test_sale.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_amount"] == "15.00"
        assert data["user_id"] == test_sale.user_id
        assert data["customer_id"] == test_sale.customer_id

    def test_update_sale_partial(self, client, test_sale):
        update_data = {"user_id": None}
        response = client.put(f"/sales/{test_sale.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user_id"] is None
        assert data["total_amount"] == "5.00"

    def test_update_sale_not_found(self, client):
        update_data = {"total_amount": "20.00"}
        response = client.put("/sales/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale not found"

    def test_update_sale_invalid_user_id(self, client, test_sale):
        update_data = {"user_id": 999}
        response = client.put(f"/sales/{test_sale.id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestSaleDelete:
    def test_delete_sale_success(self, client, test_sale):
        response = client.delete(f"/sales/{test_sale.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/sales/{test_sale.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_sale_not_found(self, client):
        response = client.delete("/sales/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale not found"