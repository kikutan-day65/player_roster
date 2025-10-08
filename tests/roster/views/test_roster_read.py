from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_success_to_get_list_of_all_players(api_client, test_players):
    expected_fields = {"id", "team", "first_name", "last_name"}
    expected_fields_for_team = {"id", "name", "sport"}

    url = reverse("player-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert set(response.data[0].keys()) == expected_fields
    assert set(response.data[0]["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_success_to_get_list_of_all_players_by_staff(
    api_client, test_players, admin_user
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
    url = reverse("player-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert set(response.data[0].keys()) == expected_fields
    assert set(response.data[0]["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_success_to_get_specific_player(api_client, test_players):
    expected_fields = {"id", "team", "first_name", "last_name"}
    expected_fields_for_team = {"id", "name", "sport"}

    url = reverse("player-detail", kwargs={"pk": test_players[0].id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == expected_fields
    assert set(response.data["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_success_to_get_specific_player_by_staff(api_client, test_players, admin_user):
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
    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == expected_fields
    assert set(response.data["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_fails_to_get_the_nonexistent_player(api_client):
    nonexistent_player_id = uuid4()
    url = reverse("player-detail", kwargs={"pk": nonexistent_player_id})
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_success_to_get_list_of_all_teams(api_client, test_teams):
    expected_fields = {"id", "name", "sport"}

    url = reverse("team-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert set(response.data[0].keys()) == expected_fields


@pytest.mark.django_db
def test_success_to_get_list_of_all_teams_by_staff(api_client, test_teams, admin_user):
    expected_fields = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    api_client.force_authenticate(admin_user)
    url = reverse("team-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert set(response.data[0].keys()) == expected_fields


@pytest.mark.django_db
def test_success_to_get_specific_team(api_client, test_teams):
    expected_fields = {"id", "name", "sport"}

    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == expected_fields


@pytest.mark.django_db
def test_success_to_get_specific_team_by_staff(api_client, test_teams, admin_user):
    expected_fields = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    api_client.force_authenticate(admin_user)
    url = reverse("team-detail", kwargs={"pk": test_teams[0].id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == expected_fields


@pytest.mark.django_db
def test_fails_to_get_the_nonexistent_team(api_client):
    nonexistent_team_id = uuid4()
    url = reverse("team-detail", kwargs={"pk": nonexistent_team_id})
    response = api_client.get(url)

    assert response.status_code == 404
