import pytest
from fastapi import status


class TestCustomerList:
    def test_list_customers_empty(self, client):
        response = client.get("/customers/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_customers_with_data(self, client, test_customer):
        response = client.get("/customers/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["first_name"] == "John"
        assert data[0]["last_name"] == "Doe"
        assert data[0]["email"] == "john.doe@example.com"
        assert data[0]["phone_number"] == "123-456-7890"


class TestCustomerGet:
    def test_get_customer_success(self, client, test_customer):
        response = client.get(f"/customers/{test_customer.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_customer.id
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john.doe@example.com"

    def test_get_customer_not_found(self, client):
        response = client.get("/customers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Customer not found"


class TestCustomerCreate:
    def test_create_customer_success(self, client):
        customer_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone_number": "987-654-3210",
        }
        response = client.post("/customers/", json=customer_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Smith"
        assert data["email"] == "jane.smith@example.com"
        assert data["phone_number"] == "987-654-3210"
        assert "id" in data

    def test_create_customer_minimal_fields(self, client):
        customer_data = {
            "first_name": "Minimal",
            "last_name": "User",
        }
        response = client.post("/customers/", json=customer_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["first_name"] == "Minimal"
        assert data["last_name"] == "User"
        assert data["email"] is None
        assert data["phone_number"] is None

    def test_create_customer_missing_required_fields(self, client):
        customer_data = {"first_name": "Incomplete"}
        response = client.post("/customers/", json=customer_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCustomerUpdate:
    def test_update_customer_success(self, client, test_customer):
        update_data = {
            "first_name": "Johnny",
            "email": "johnny.doe@example.com",
        }
        response = client.put(f"/customers/{test_customer.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Johnny"
        assert data["email"] == "johnny.doe@example.com"
        assert data["last_name"] == "Doe"

    def test_update_customer_partial(self, client, test_customer):
        update_data = {"phone_number": "555-0000"}
        response = client.put(f"/customers/{test_customer.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["phone_number"] == "555-0000"
        assert data["first_name"] == "John"

    def test_update_customer_not_found(self, client):
        update_data = {"first_name": "Ghost"}
        response = client.put("/customers/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Customer not found"


class TestCustomerDelete:
    def test_delete_customer_success(self, client, test_customer):
        response = client.delete(f"/customers/{test_customer.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/customers/{test_customer.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_customer_not_found(self, client):
        response = client.delete("/customers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Customer not found"