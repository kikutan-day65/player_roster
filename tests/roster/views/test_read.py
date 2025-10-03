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

    url = reverse("player-detail", kwargs={"pk": "nonexistent-id"})
    response = api_client.get(url)

    assert response.status_code == 404
