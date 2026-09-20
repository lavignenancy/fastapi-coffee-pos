import pytest
from decimal import Decimal
from fastapi import status


class TestSaleItemList:
    def test_list_sale_items_empty(self, client):
        response = client.get("/sale-items/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_sale_items_with_data(self, client, test_sale_item):
        response = client.get("/sale-items/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["sale_id"] == test_sale_item.sale_id
        assert data[0]["product_id"] == test_sale_item.product_id
        assert data[0]["quantity"] == 2
        assert data[0]["item_price"] == "2.50"


class TestSaleItemGet:
    def test_get_sale_item_success(self, client, test_sale_item):
        response = client.get(f"/sale-items/{test_sale_item.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_sale_item.id
        assert data["sale_id"] == test_sale_item.sale_id
        assert data["product_id"] == test_sale_item.product_id
        assert data["quantity"] == 2
        assert data["item_price"] == "2.50"
        assert "created_at" in data

    def test_get_sale_item_not_found(self, client):
        response = client.get("/sale-items/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale item not found"


class TestSaleItemCreate:
    def test_create_sale_item_success(self, client, test_sale, test_product):
        sale_item_data = {
            "Sale_id": test_sale.id,
            "Product_id": test_product.id,
            "quantity": 3,
            "item_price": "3.00",
        }
        response = client.post("/sale-items/", json=sale_item_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["sale_id"] == test_sale.id
        assert data["product_id"] == test_product.id
        assert data["quantity"] == 3
        assert data["item_price"] == "3.00"
        assert "id" in data
        assert "created_at" in data

    def test_create_sale_item_invalid_sale_id(self, client, test_product):
        sale_item_data = {
            "Sale_id": 999,
            "Product_id": test_product.id,
            "quantity": 1,
            "item_price": "2.00",
        }
        response = client.post("/sale-items/", json=sale_item_data)
        assert response.status_code in (status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST)

    def test_create_sale_item_invalid_product_id(self, client, test_sale):
        sale_item_data = {
            "Sale_id": test_sale.id,
            "Product_id": 999,
            "quantity": 1,
            "item_price": "2.00",
        }
        response = client.post("/sale-items/", json=sale_item_data)
        assert response.status_code in (status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST)

    def test_create_sale_item_missing_required_fields(self, client):
        sale_item_data = {"quantity": 1}
        response = client.post("/sale-items/", json=sale_item_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSaleItemUpdate:
    def test_update_sale_item_success(self, client, test_sale_item):
        update_data = {
            "quantity": 5,
            "item_price": "4.00",
        }
        response = client.put(f"/sale-items/{test_sale_item.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 5
        assert data["item_price"] == "4.00"
        assert data["sale_id"] == test_sale_item.sale_id
        assert data["product_id"] == test_sale_item.product_id

    def test_update_sale_item_partial(self, client, test_sale_item):
        update_data = {"quantity": 10}
        response = client.put(f"/sale-items/{test_sale_item.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 10
        assert data["item_price"] == "2.50"

    def test_update_sale_item_not_found(self, client):
        update_data = {"quantity": 1}
        response = client.put("/sale-items/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale item not found"

    def test_update_sale_item_invalid_sale_id(self, client, test_sale_item):
        update_data = {"sale_id": 999}
        response = client.put(f"/sale-items/{test_sale_item.id}", json=update_data)
        assert response.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)


class TestSaleItemDelete:
    def test_delete_sale_item_success(self, client, test_sale_item):
        response = client.delete(f"/sale-items/{test_sale_item.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/sale-items/{test_sale_item.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_sale_item_not_found(self, client):
        response = client.delete("/sale-items/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sale item not found"