from datetime import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
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
def users(db):
    return [
        UserAccount.objects.create_user(
            username="user_1",
            email="user_1@example.com",
            password="generalUser123",
        ),
        UserAccount.objects.create_user(
            username="user_2",
            email="user_2@example.com",
            password="generalUser123",
        ),
        UserAccount.objects.create_user(
            username="user_3",
            email="user_3@example.com",
            password="adminUser123",
            is_staff=True,
        ),
    ]


@pytest.fixture
def user_filter_data(db):
    user_objects = [
        UserAccount.objects.create(
            username="user_one",
            email="user_one@example.com",
            password="userOne123",
        ),
        UserAccount.objects.create(
            username="user_two",
            email="user_two@example.com",
            password="userTwo123",
        ),
        UserAccount.objects.create(
            username="user_three",
            email="user_three@example.com",
            password="userThree123",
        ),
        UserAccount.objects.create(
            username="user_four",
            email="user_four@example.com",
            password="userFour123",
        ),
    ]

    created_at_objects = [
        timezone.make_aware(datetime(2022, 1, 1)),
        timezone.make_aware(datetime(2023, 1, 1)),
        timezone.make_aware(datetime(2024, 1, 1)),
        timezone.make_aware(datetime(2024, 6, 1)),
    ]

    for user, created_at in zip(user_objects, created_at_objects):
        user.created_at = created_at

    UserAccount.objects.bulk_update(user_objects, fields=["created_at"])

    return user_objects


@pytest.fixture
def team_data():
    return {"name": "Team Name", "sport": "baseball"}


@pytest.fixture
def teams(db):
    return [
        Team.objects.create(name="Team Name", sport="baseball"),
        Team.objects.create(name="Team Name 2", sport="basketball"),
        Team.objects.create(name="Team Name 3", sport="football"),
    ]


@pytest.fixture
def team_filter_data(db):
    team_objects = [
        Team.objects.create(name="Team A", sport="baseball"),
        Team.objects.create(name="Team B", sport="basketball"),
        Team.objects.create(name="Team C", sport="football"),
        Team.objects.create(name="Team D", sport="baseball"),
    ]

    created_at_objects = [
        timezone.make_aware(datetime(2022, 1, 1)),
        timezone.make_aware(datetime(2023, 1, 1)),
        timezone.make_aware(datetime(2024, 1, 1)),
        timezone.make_aware(datetime(2024, 6, 1)),
    ]

    for team, created_at in zip(team_objects, created_at_objects):
        team.created_at = created_at

    Team.objects.bulk_update(team_objects, fields=["created_at"])

    return team_objects


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
        Player.objects.create(
            first_name="FirstNameThree",
            last_name="LastNameThree",
            team_id=str(
                teams[0].id,
            ),
        ),
    ]


@pytest.fixture
def player_filter_data(db, teams):
    player_objects = [
        Player.objects.create(
            first_name="FistNameOne", last_name="LastNameOne", team=teams[0]
        ),
        Player.objects.create(
            first_name="FistNameTwo", last_name="LastNameTwo", team=teams[1]
        ),
        Player.objects.create(
            first_name="FistNameThree", last_name="LastNameThree", team=teams[2]
        ),
        Player.objects.create(
            first_name="FistNameFour", last_name="LastNameFour", team=teams[2]
        ),
    ]

    created_at_objects = [
        timezone.make_aware(datetime(2022, 1, 1)),
        timezone.make_aware(datetime(2023, 1, 1)),
        timezone.make_aware(datetime(2024, 1, 1)),
        timezone.make_aware(datetime(2024, 6, 1)),
    ]

    for player, created_at in zip(player_objects, created_at_objects):
        player.created_at = created_at

    Player.objects.bulk_update(player_objects, fields=["created_at"])

    return player_objects


@pytest.fixture
def comment_data(db, general_user, players):
    return {
        "user_id": general_user.id,
        "player_id": players[0].id,
        "body": "Comment Body",
    }


@pytest.fixture
def comment_data_from_view(db, players):
    return {
        "player_id": players[0].id,
        "body": "Comment Body From View",
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
            player=players[0],
            body="Comment Body 1",
        ),
        Comment.objects.create(
            user=general_user,
            player=players[1],
            body="Comment Body over 100 characters" * 10,
        ),
    ]


@pytest.fixture
def comment_filter_data(db, general_user, general_user_2, players):
    comment_objects = [
        Comment.objects.create(
            user=general_user, player=players[0], body="Comment Body One"
        ),
        Comment.objects.create(
            user=general_user, player=players[1], body="Comment Body Two"
        ),
        Comment.objects.create(
            user=general_user_2, player=players[2], body="Comment Body Three"
        ),
        Comment.objects.create(
            user=general_user_2, player=players[2], body="Comment Body Four"
        ),
    ]

    created_at_objects = [
        timezone.make_aware(datetime(2022, 1, 1)),
        timezone.make_aware(datetime(2023, 1, 1)),
        timezone.make_aware(datetime(2024, 1, 1)),
        timezone.make_aware(datetime(2024, 6, 1)),
    ]

    for team, created_at in zip(comment_objects, created_at_objects):
        team.created_at = created_at

    Comment.objects.bulk_update(comment_objects, fields=["created_at"])

    return comment_objects


@pytest.fixture
def user_account_list_url():
    return reverse("user_account-list")


@pytest.fixture
def user_account_detail_url():
    def build_url(pk):
        return reverse("user_account-detail", args=[pk])

    return build_url


@pytest.fixture
def user_account_comments_url():
    def build_url(pk):
        return reverse("user_account-comments", args=[pk])

    return build_url


@pytest.fixture
def me_url():
    return reverse("me")


@pytest.fixture
def me_comments_url():
    return reverse("me_comments")


@pytest.fixture
def team_list_url():
    return reverse("team-list")


@pytest.fixture
def team_detail_url():
    def build_url(pk):
        return reverse("team-detail", args=[pk])

    return build_url


@pytest.fixture
def team_players_url():
    def build_url(pk):
        return reverse("team-players", args=[pk])

    return build_url


@pytest.fixture
def player_list_url():
    return reverse("player-list")


@pytest.fixture
def player_detail_url():
    def build_url(pk):
        return reverse("player-detail", args=[pk])

    return build_url


@pytest.fixture
def player_comments_url():
    def build_url(pk):
        return reverse("player-comments", args=[pk])

    return build_url


@pytest.fixture
def comment_list_url():
    return reverse("comment-list")


@pytest.fixture
def comment_detail_url():
    def build_url(pk):
        return reverse("comment-detail", args=[pk])

    return build_url
