from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("first_name", "updated first name"), ("last_name", "updated last name")],
)
def test_successes_to_change_player_first_name_last_name(
    api_client, test_players, admin_user, field, data
):
    expected_fields = {
        "id",
        "team",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    expected_fields_for_team = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    api_client.force_authenticate(admin_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {field: data}

    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data
    assert set(response.data.keys()) == expected_fields
    assert set(response.data["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_successes_to_change_player_team(
    api_client, test_players, admin_user, test_teams
):
    expected_fields = {
        "id",
        "team",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    expected_fields_for_team = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    api_client.force_authenticate(admin_user)
    url = reverse("player-detail", kwargs={"pk": test_players[0].id})

    change_data = {"team_id": test_teams[1].id}

    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data["team"]["id"] == str(test_teams[1].id)
    assert response.data["team"]["name"] == test_teams[1].name
    assert response.data["team"]["sport"] == test_teams[1].sport
    assert set(response.data.keys()) == expected_fields
    assert set(response.data["team"].keys()) == expected_fields_for_team


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
    print(response.data)
