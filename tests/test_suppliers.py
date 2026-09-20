import pytest
from fastapi import status


class TestSupplierList:
    def test_list_suppliers_empty(self, client):
        response = client.get("/suppliers/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_suppliers_with_data(self, client, test_supplier):
        response = client.get("/suppliers/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["supplier_name"] == "Coffee Beans Inc"
        assert data[0]["contact_name"] == "Jane Smith"
        assert data[0]["phone"] == "555-0100"


class TestSupplierGet:
    def test_get_supplier_success(self, client, test_supplier):
        response = client.get(f"/suppliers/{test_supplier.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_supplier.id
        assert data["supplier_name"] == "Coffee Beans Inc"
        assert data["contact_name"] == "Jane Smith"
        assert data["phone"] == "555-0100"

    def test_get_supplier_not_found(self, client):
        response = client.get("/suppliers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Supplier not found"


class TestSupplierCreate:
    def test_create_supplier_success(self, client):
        supplier_data = {
            "supplier_name": "Milk Supply Co",
            "contact_name": "Bob Wilson",
            "phone": "555-0200",
        }
        response = client.post("/suppliers/", json=supplier_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["supplier_name"] == "Milk Supply Co"
        assert data["contact_name"] == "Bob Wilson"
        assert data["phone"] == "555-0200"
        assert "id" in data

    def test_create_supplier_minimal_fields(self, client):
        supplier_data = {
            "supplier_name": "Minimal Supplier",
            "phone": "555-0300",
        }
        response = client.post("/suppliers/", json=supplier_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["supplier_name"] == "Minimal Supplier"
        assert data["phone"] == "555-0300"
        assert data["contact_name"] is None

    def test_create_supplier_missing_required_fields(self, client):
        supplier_data = {"supplier_name": "Incomplete"}
        response = client.post("/suppliers/", json=supplier_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSupplierUpdate:
    def test_update_supplier_success(self, client, test_supplier):
        update_data = {
            "supplier_name": "Updated Coffee Beans",
            "contact_name": "Updated Contact",
        }
        response = client.put(f"/suppliers/{test_supplier.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["supplier_name"] == "Updated Coffee Beans"
        assert data["contact_name"] == "Updated Contact"
        assert data["phone"] == "555-0100"

    def test_update_supplier_partial(self, client, test_supplier):
        update_data = {"phone": "555-9999"}
        response = client.put(f"/suppliers/{test_supplier.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["phone"] == "555-9999"
        assert data["supplier_name"] == "Coffee Beans Inc"

    def test_update_supplier_not_found(self, client):
        update_data = {"supplier_name": "Ghost Supplier"}
        response = client.put("/suppliers/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Supplier not found"


class TestSupplierDelete:
    def test_delete_supplier_success(self, client, test_supplier):
        response = client.delete(f"/suppliers/{test_supplier.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/suppliers/{test_supplier.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_supplier_not_found(self, client):
        response = client.delete("/suppliers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Supplier not found"