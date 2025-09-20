import pytest
from rest_framework.test import APIClient

from user_account.models import UserAccount


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user_data():
    data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "testuser123",
    }

    return data


@pytest.fixture
def test_user(db):
    return UserAccount.objects.create_user(
        username="test_user", email="test_user@example.com", password="testuser123"
    )


@pytest.fixture
def test_user_2(db):
    return UserAccount.objects.create_user(
        username="test_user_2", email="test_user_2@example.com", password="testuser123"
    )


@pytest.fixture
def admin_user(db):
    return UserAccount.objects.create_user(
        username="admin", email="admin@example.com", password="admin123", is_staff=True
    )


@pytest.fixture
def super_user(db):
    return UserAccount.objects.create_superuser(
        username="super", email="super@example.com", password="super123"
    )
