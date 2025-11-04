import pytest
from rest_framework.test import APIClient

from roster.models import Comment, Player, Team
from user_account.models import UserAccount


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def general_user_data():
    return {
        "username": "general_user",
        "email": "general_user@example.com",
        "password": "generalUser123",
    }


@pytest.fixture
def general_user(db):
    return UserAccount.objects.create_user(
        username="general_user",
        email="general_user@example.com",
        password="generalUser123",
    )


@pytest.fixture
def general_user_2(db):
    return UserAccount.objects.create_user(
        username="general_user_2",
        email="general_user_2@example.com",
        password="generalUser123",
    )


@pytest.fixture
def admin_user_data():
    return {
        "username": "admin_user",
        "email": "admin_user@example.com",
        "password": "adminUser123",
        "is_staff": True,
    }


@pytest.fixture
def admin_user(db):
    return UserAccount.objects.create_user(
        username="admin_user",
        email="admin_user@example.com",
        password="adminUser123",
        is_staff=True,
    )


@pytest.fixture
def super_user_data():
    return {
        "username": "super_user",
        "email": "super_user@example.com",
        "password": "superUser123",
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def super_user(db):
    return UserAccount.objects.create_superuser(
        username="super_user",
        email="super_user@example.com",
        password="superUser123",
    )


@pytest.fixture
def team_data():
    return {"name": "Team Name", "sport": "baseball"}


@pytest.fixture
def teams(db):
    return [
        Team.objects.create(name="Team Name", sport="baseball"),
        Team.objects.create(name="Team Name 2", sport="basketball"),
    ]


@pytest.fixture
def player_data(teams):
    return {
        "first_name": "FirstName",
        "last_name": "LastName",
        "team_id": str(teams[0].id),
    }


@pytest.fixture
def players(db, teams):
    return [
        Player.objects.create(
            first_name="FirstNameOne",
            last_name="LastNameOne",
            team_id=str(
                teams[0].id,
            ),
        ),
        Player.objects.create(
            first_name="FirstNameTwo",
            last_name="LastNameTwo",
            team_id=str(
                teams[0].id,
            ),
        ),
    ]


@pytest.fixture
def comment_data(general_user, players):
    return {
        "user": general_user,
        "player": players[0],
        "body": "Comment Body",
    }


@pytest.fixture
def comments(db, general_user, players):
    return [
        Comment.objects.create(
            user=general_user,
            player=players[0],
            body="Comment Body",
        ),
        Comment.objects.create(
            user=general_user,
            player=players[1],
            body="Comment Body over 100 characters" * 100,
        ),
    ]
