import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_player_creation_success(api_client, test_player_data, admin_user):
    player_fields = {
        "id",
        "team",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "deleted_at",
        "comments",
        "team",
    }
    team_fields = {"id", "name"}

    api_client.force_authenticate(admin_user)

    url = reverse("player-list")
    response = api_client.post(url, data=test_player_data)

    assert response.status_code == 201

    player_data = response.data
    assert player_data["first_name"] == test_player_data["first_name"]
    assert player_data["last_name"] == test_player_data["last_name"]
    assert len(player_data["comments"]) == 0
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert team_data["id"] == test_player_data["team_id"]
    assert set(team_data.keys()) == team_fields


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


@pytest.mark.django_db
def test_team_creation_success(api_client, test_team_data, admin_user):
    team_fields = {
        "id",
        "name",
        "sport",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    api_client.force_authenticate(admin_user)

    url = reverse("team-list")
    response = api_client.post(url, data=test_team_data)

    assert response.status_code == 201

    team_data = response.data
    assert team_data["name"] == test_team_data["name"]
    assert team_data["sport"] == test_team_data["sport"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_create_team_by_general_user(api_client, test_team_data, test_user):
    api_client.force_authenticate(test_user)

    url = reverse("team-list")
    response = api_client.post(url, data=test_team_data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_create_team_by_unauthenticated_user(api_client, test_team_data):

    url = reverse("team-list")
    response = api_client.post(url, data=test_team_data)

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, value",
    [("name", ""), ("sport", "")],
    ids=["without name", "without sport"],
)
def test_team_creation_fails_without_required_fields(
    api_client, test_team_data, admin_user, field, value
):
    api_client.force_authenticate(admin_user)
    test_team_data[field] = value

    url = reverse("team-list")
    response = api_client.post(url, data=test_team_data)

    assert response.status_code == 400
    assert field in response.data
