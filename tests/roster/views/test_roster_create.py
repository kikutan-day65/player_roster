import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_player_creation_success(api_client, test_player_data, admin_user):
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
    response = api_client.post(url, data=test_player_data)

    assert response.status_code == 201
    assert response.data["first_name"] == test_player_data["first_name"]
    assert response.data["last_name"] == test_player_data["last_name"]
    assert response.data["team"]["id"] == test_player_data["team_id"]
    assert set(response.data.keys()) == expected_fields
    assert set(response.data["team"].keys()) == expected_fields_for_team


@pytest.mark.django_db
def test_fails_to_create_player_by_general_user(
    api_client, test_player_data, test_user
):
    api_client.force_authenticate(test_user)

    url = reverse("player-list")
    response = api_client.post(url, data=test_player_data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_create_player_by_unauthenticated_user(api_client, test_player_data):

    url = reverse("player-list")
    response = api_client.post(url, data=test_player_data)

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field,value",
    [
        ("first_name", ""),
        ("last_name", ""),
        ("team_id", ""),
    ],
    ids=["without first_name", "without last_name", "without team_id"],
)
def test_player_creation_fails_without_required_fields(
    api_client, test_player_data, admin_user, field, value
):
    api_client.force_authenticate(admin_user)
    test_player_data[field] = value

    url = reverse("player-list")
    response = api_client.post(url, data=test_player_data)

    assert response.status_code == 400
    assert field in response.data
