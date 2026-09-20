import pytest
from decimal import Decimal
from fastapi import status


class TestCategoryList:
    def test_list_categories_empty(self, client):
        response = client.get("/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_categories_with_data(self, client, test_category):
        response = client.get("/categories/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_name"] == "Espresso"
        assert data[0]["tax_rate"] == "8.50"


class TestCategoryGet:
    def test_get_category_success(self, client, test_category):
        response = client.get(f"/categories/{test_category.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_category.id
        assert data["category_name"] == "Espresso"
        assert data["tax_rate"] == "8.50"

    def test_get_category_not_found(self, client):
        response = client.get("/categories/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Category not found"


class TestCategoryCreate:
    def test_create_category_success(self, client):
        category_data = {
            "category_name": "Pastries",
            "tax_rate": "10.00",
        }
        response = client.post("/categories/", json=category_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["category_name"] == "Pastries"
        assert data["tax_rate"] == "10.00"
        assert "id" in data

    def test_create_category_missing_required_fields(self, client):
        category_data = {"category_name": "Incomplete"}
        response = client.post("/categories/", json=category_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCategoryUpdate:
    def test_update_category_success(self, client, test_category):
        update_data = {
            "category_name": "Cold Beverages",
            "tax_rate": "5.00",
        }
        response = client.put(f"/categories/{test_category.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["category_name"] == "Cold Beverages"
        assert data["tax_rate"] == "5.00"

    def test_update_category_partial(self, client, test_category):
        update_data = {"tax_rate": "12.00"}
        response = client.put(f"/categories/{test_category.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tax_rate"] == "12.00"
        assert data["category_name"] == "Espresso"

    def test_update_category_not_found(self, client):
        update_data = {"category_name": "Ghost Category"}
        response = client.put("/categories/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Category not found"


class TestCategoryDelete:
    def test_delete_category_success(self, client, test_category):
        response = client.delete(f"/categories/{test_category.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/categories/{test_category.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_not_found(self, client):
        response = client.delete("/categories/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Category not found"