from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_successes_to_get_user_list_by_admin_user(
    api_client, test_user, test_comments, admin_user
):
    user_fields = {
        "id",
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
        "deleted_at",
        "comments",
    }
    comment_fields = {"id", "body", "created_at", "player"}
    player_fields = {"id", "first_name", "last_name", "team"}
    team_fields = {"id", "name"}

    url = reverse("user_account-list")
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3

    user_data = response.data[1]
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_get_user_list_by_general_user(api_client, test_user):
    url = reverse("user_account-list")
    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_get_user_list_by_unauthenticated_user(api_client):
    url = reverse("user_account-list")

    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_successes_to_get_specific_user_by_admin_user(
    api_client, test_user_2, admin_user, test_comments
):
    user_fields = {
        "id",
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
        "deleted_at",
        "comments",
    }
    comment_fields = {"id", "body", "created_at", "player"}
    player_fields = {"id", "first_name", "last_name", "team"}
    team_fields = {"id", "name"}
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    api_client.force_authenticate(user=admin_user)

    response = api_client.get(url)

    assert response.status_code == 200

    user_data = response.data
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_successes_to_get_specific_user_by_authenticated_user(
    api_client, test_user_2, test_user, test_comments
):
    user_fields = {"id", "username", "created_at", "updated_at", "comments"}
    comment_fields = {"id", "body", "created_at", "player"}
    player_fields = {"id", "first_name", "last_name", "team"}
    team_fields = {"id", "name"}

    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 200

    user_data = response.data
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_get_specific_user_by_unauthenticated_user(api_client, test_user_2):
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_get_nonexistent_user(api_client, test_user):
    nonexistent_user = uuid4()
    url = reverse("user_account-detail", kwargs={"pk": nonexistent_user})

    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_successes_to_get_current_user_by_authenticated_user(
    api_client, test_user, test_comments
):
    user_fields = {"id", "username", "email", "created_at", "updated_at", "comments"}
    comment_fields = {"id", "body", "created_at", "player"}
    player_fields = {"id", "first_name", "last_name", "team"}
    team_fields = {"id", "name"}

    url = reverse("user_account_me")
    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == test_user.username
    assert response.data["email"] == test_user.email

    user_data = response.data
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_get_current_user_by_unauthenticated_user(api_client):
    url = reverse("user_account_me")

    response = api_client.get(url)

    assert response.status_code == 401
