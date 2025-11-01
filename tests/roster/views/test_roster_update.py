from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("first_name", "updated first name"), ("last_name", "updated last name")],
)
def test_successes_to_change_player_first_name_last_name(
    api_client, test_players, admin_user, test_comments, field, data
):
    player_fields = {
        "id",
        "team",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "deleted_at",
        "comments",
    }
    comment_fields = {"id", "body", "created_at", "user"}
    user_fields = {"id", "username"}
    team_fields = {"id", "name"}

    api_client.force_authenticate(admin_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {field: data}

    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data

    player_data = response.data
    assert set(player_data.keys()) == player_fields

    comment_data = player_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    user_data = comment_data["user"]
    assert set(user_data.keys()) == user_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_successes_to_change_player_team(
    api_client, test_players, admin_user, test_teams, test_comments
):
    player_fields = {
        "id",
        "team",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "deleted_at",
        "comments",
    }
    comment_fields = {"id", "body", "created_at", "user"}
    user_fields = {"id", "username"}
    team_fields = {"id", "name"}

    api_client.force_authenticate(admin_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {"team_id": test_teams[1].id}

    response = api_client.patch(url, change_data)

    assert response.status_code == 200

    player_data = response.data
    assert set(player_data.keys()) == player_fields

    comment_data = player_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    user_data = comment_data["user"]
    assert set(user_data.keys()) == user_fields

    team_data = player_data["team"]
    assert team_data["id"] == str(test_teams[1].id)
    assert team_data["name"] == test_teams[1].name
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_change_player_by_general_user(api_client, test_players, test_user):
    api_client.force_authenticate(test_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {"first_name": "updated first name"}

    response = api_client.patch(url, change_data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_change_player_by_unauthenticated_user(api_client, test_players):
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {"first_name": "updated first name"}

    response = api_client.patch(url, change_data)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_to_change_nonexistent_player_information(api_client, admin_user):
    nonexistent_player_id = uuid4()
    url = reverse("player-detail", kwargs={"pk": nonexistent_player_id})

    change_data = {"first_name": "updated first name"}

    api_client.force_authenticate(admin_user)
    response = api_client.patch(url, change_data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_fails_to_change_player_information_with_nonexistent_team(
    api_client, test_players, admin_user
):
    api_client.force_authenticate(admin_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    nonexistent_team_id = uuid4()
    change_data = {"team_id": nonexistent_team_id}

    response = api_client.patch(url, change_data)

    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data", [("name", "updated name"), ("sport", "basketball")]
)
def test_successes_to_change_team_name_sport(
    api_client, test_teams, admin_user, field, data
):
    team_fields = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    api_client.force_authenticate(admin_user)
    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})

    change_data = {field: data}

    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data

    team_data = response.data
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_change_team_by_general_user(api_client, test_teams, test_user):
    api_client.force_authenticate(test_user)
    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})

    change_data = {"name": "updated name"}

    response = api_client.patch(url, change_data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_change_team_by_unauthenticated_user(api_client, test_teams):
    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})

    change_data = {"name": "updated name"}

    response = api_client.patch(url, change_data)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_to_change_nonexistent_team_information(api_client, admin_user):
    nonexistent_team_id = uuid4()
    url = reverse("team-detail", kwargs={"pk": nonexistent_team_id})

    change_data = {"first_name": "updated first name"}

    api_client.force_authenticate(admin_user)
    response = api_client.patch(url, change_data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_fails_to_change_team_information_with_nonexistent_sport_choice(
    api_client, test_teams, admin_user
):
    api_client.force_authenticate(admin_user)
    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})

    change_data = {"sport": "nonexistent_sport"}

    response = api_client.patch(url, change_data)

    assert response.status_code == 400
