import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_creation_success(api_client, test_user_data):
    expected_fields = {"id", "username", "email", "created_at", "updated_at"}

    url = reverse("user_account-list")
    response = api_client.post(url, data=test_user_data)

    assert response.status_code == 201
    assert response.data["username"] == test_user_data["username"]
    assert response.data["email"] == test_user_data["email"]
    assert set(response.data.keys()) == expected_fields


@pytest.mark.django_db
def test_user_creation_fails_when_username_is_duplicate(api_client, test_user_data):
    url = reverse("user_account-list")
    api_client.post(url, data=test_user_data)

    data = {
        "username": test_user_data["username"],
        "email": "sample@example.com",
        "password": "duplicate123",
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 400
    assert "username" in response.data


@pytest.mark.django_db
def test_user_creation_fails_when_email_duplicate(api_client, test_user_data):
    url = reverse("user_account-list")
    api_client.post(url, data=test_user_data)

    data = {
        "username": "sample",
        "email": test_user_data["email"],
        "password": "duplicate123",
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["username", "email", "password"])
def test_user_creation_fails_when_required_field_is_empty(
    api_client, test_user_data, field
):
    test_user_data[field] = ""

    url = reverse("user_account-list")
    response = api_client.post(url, data=test_user_data)

    assert response.status_code == 400
    assert field in response.data
