import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from roster.models import Player, Team
from user_account.models import UserAccount


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user_data():
    return {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "testuser123",
    }


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


@pytest.fixture
def test_team(db):
    return Team.objects.create(name="Test Team", sport="baseball")


@pytest.fixture
def test_player_data(test_team):
    return {"first_name": "John", "last_name": "Doe", "team_id": str(test_team.id)}


@pytest.fixture
def test_players(test_team):
    players = [
        Player.objects.create(
            first_name="John", last_name="Doe", team_id=str(test_team.id)
        ),
        Player.objects.create(
            first_name="Jane", last_name="Doe", team_id=str(test_team.id)
        ),
        Player.objects.create(
            first_name="Deleted",
            last_name="User",
            team_id=str(test_team.id),
            deleted_at=timezone.now(),
        ),
    ]
    return players
