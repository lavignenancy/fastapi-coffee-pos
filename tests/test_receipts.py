import pytest
from fastapi import status


class TestReceiptList:
    def test_list_receipts_empty(self, client):
        response = client.get("/receipts/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_receipts_with_data(self, client, test_receipt):
        response = client.get("/receipts/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["sale_id"] == test_receipt.sale_id
        assert data[0]["receipt_number"] == "RCP-001"


class TestReceiptGet:
    def test_get_receipt_success(self, client, test_receipt):
        response = client.get(f"/receipts/{test_receipt.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_receipt.id
        assert data["sale_id"] == test_receipt.sale_id
        assert data["receipt_number"] == "RCP-001"

    def test_get_receipt_not_found(self, client):
        response = client.get("/receipts/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Receipt not found"


class TestReceiptCreate:
    def test_create_receipt_success(self, client, test_sale):
        receipt_data = {
            "sale_id": test_sale.id,
            "receipt_number": "RCP-002",
        }
        response = client.post("/receipts/", json=receipt_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["sale_id"] == test_sale.id
        assert data["receipt_number"] == "RCP-002"
        assert "id" in data
        assert "created_at" in data

    def test_create_receipt_duplicate_receipt_number(self, client, test_sale, test_receipt):
        receipt_data = {
            "sale_id": test_sale.id,
            "receipt_number": "RCP-001",
        }
        response = client.post("/receipts/", json=receipt_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_receipt_missing_required_fields(self, client):
        receipt_data = {"receipt_number": "RCP-003"}
        response = client.post("/receipts/", json=receipt_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestReceiptUpdate:
    def test_update_receipt_success(self, client, test_receipt):
        update_data = {
            "receipt_number": "RCP-001-UPDATED",
        }
        response = client.put(f"/receipts/{test_receipt.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["receipt_number"] == "RCP-001-UPDATED"
        assert data["sale_id"] == test_receipt.sale_id

    def test_update_receipt_partial(self, client, test_receipt):
        update_data = {"sale_id": test_receipt.sale_id}
        response = client.put(f"/receipts/{test_receipt.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["receipt_number"] == "RCP-001"
        assert data["sale_id"] == test_receipt.sale_id

    def test_update_receipt_not_found(self, client):
        update_data = {"receipt_number": "GHOST"}
        response = client.put("/receipts/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Receipt not found"

    def test_update_receipt_duplicate_receipt_number(self, client, test_receipt, test_sale):
        response = client.post("/receipts/", json={"sale_id": test_sale.id, "receipt_number": "RCP-003"})
        assert response.status_code == status.HTTP_201_CREATED
        update_data = {"receipt_number": "RCP-003"}
        response = client.put(f"/receipts/{test_receipt.id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestReceiptDelete:
    def test_delete_receipt_success(self, client, test_receipt):
        response = client.delete(f"/receipts/{test_receipt.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/receipts/{test_receipt.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_receipt_not_found(self, client):
        response = client.delete("/receipts/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Receipt not found"