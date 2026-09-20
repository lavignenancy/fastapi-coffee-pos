import pytest
from decimal import Decimal
from fastapi import status


class TestPaymentList:
    def test_list_payments_empty(self, client):
        response = client.get("/payments/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_payments_with_data(self, client, test_payment):
        response = client.get("/payments/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["sale_id"] == test_payment.sale_id
        assert data[0]["payment_method"] == "Card"
        assert data[0]["amount_paid"] == "5.00"


class TestPaymentGet:
    def test_get_payment_success(self, client, test_payment):
        response = client.get(f"/payments/{test_payment.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_payment.id
        assert data["sale_id"] == test_payment.sale_id
        assert data["payment_method"] == "Card"
        assert data["amount_paid"] == "5.00"

    def test_get_payment_not_found(self, client):
        response = client.get("/payments/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Payment not found"


class TestPaymentCreate:
    def test_create_payment_success(self, client, test_sale):
        payment_data = {
            "sale_id": test_sale.id,
            "payment_method": "Mobile Wallet",
            "amount_paid": "10.00",
        }
        response = client.post("/payments/", json=payment_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["sale_id"] == test_sale.id
        assert data["payment_method"] == "Mobile Wallet"
        assert data["amount_paid"] == "10.00"
        assert "id" in data

    def test_create_payment_missing_required_fields(self, client):
        payment_data = {"payment_method": "Card"}
        response = client.post("/payments/", json=payment_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestPaymentUpdate:
    def test_update_payment_success(self, client, test_payment):
        update_data = {
            "payment_method": "Cash",
            "amount_paid": "5.50",
        }
        response = client.put(f"/payments/{test_payment.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["payment_method"] == "Cash"
        assert data["amount_paid"] == "5.50"
        assert data["sale_id"] == test_payment.sale_id

    def test_update_payment_partial(self, client, test_payment):
        update_data = {"payment_method": "Card"}
        response = client.put(f"/payments/{test_payment.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["payment_method"] == "Card"
        assert data["amount_paid"] == "5.00"

    def test_update_payment_not_found(self, client):
        update_data = {"payment_method": "Ghost"}
        response = client.put("/payments/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Payment not found"


class TestPaymentDelete:
    def test_delete_payment_success(self, client, test_payment):
        response = client.delete(f"/payments/{test_payment.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/payments/{test_payment.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_payment_not_found(self, client):
        response = client.delete("/payments/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Payment not found"