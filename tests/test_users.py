import pytest
from fastapi import status


class TestUserList:
    def test_list_users_empty(self, client):
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_users_with_data(self, client, test_user):
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == "testuser"
        assert data[0]["role"] == "cashier"
        assert data[0]["is_active"] is True


class TestUserGet:
    def test_get_user_success(self, client, test_user):
        response = client.get(f"/users/{test_user.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == "testuser"
        assert data["role"] == "cashier"
        assert data["is_active"] is True

    def test_get_user_not_found(self, client):
        response = client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"


class TestUserCreate:
    def test_create_user_success(self, client):
        user_data = {
            "username": "newuser",
            "hashed_password": "secure_hash",
            "role": "manager",
            "is_active": True,
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["role"] == "manager"
        assert data["is_active"] is True
        assert "id" in data

    def test_create_user_missing_required_fields(self, client):
        user_data = {
            "username": "incomplete",
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_duplicate_username(self, client, test_user):
        user_data = {
            "username": "testuser",
            "hashed_password": "another_hash",
            "role": "cashier",
            "is_active": True,
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserUpdate:
    def test_update_user_success(self, client, test_user):
        update_data = {
            "username": "updateduser",
            "role": "admin",
        }
        response = client.put(f"/users/{test_user.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["role"] == "admin"
        assert data["is_active"] is True

    def test_update_user_partial(self, client, test_user):
        update_data = {"is_active": False}
        response = client.put(f"/users/{test_user.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False
        assert data["username"] == "testuser"

    def test_update_user_not_found(self, client):
        update_data = {"username": "ghost"}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    def test_update_user_duplicate_username(self, client, test_user):
        client.post(
            "/users/",
            json={
                "username": "another",
                "hashed_password": "hash",
                "role": "cashier",
                "is_active": True,
            },
        )
        update_data = {"username": "another"}
        response = client.put(f"/users/{test_user.id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserDelete:
    def test_delete_user_success(self, client, test_user):
        response = client.delete(f"/users/{test_user.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/users/{test_user.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        response = client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"