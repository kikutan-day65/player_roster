from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("username", "updated_username"), ("email", "updated_email@example.com")],
)
def test_successes_to_patch_user_information_by_admin_user(
    api_client, test_user, admin_user, test_comments, field, data
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

    url = reverse("user_account-detail", kwargs={"pk": test_user.id})
    api_client.force_authenticate(user=admin_user)

    change_data = {field: data}
    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data

    user_data = response.data
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
def test_fails_to_patch_user_information_by_general_user(
    api_client, test_user, test_user_2
):
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})
    api_client.force_authenticate(user=test_user)

    change_data = {"username": "updated_username"}
    response = api_client.patch(url, change_data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_patch_user_information_by_unauthenticated_user(
    api_client, test_user_2
):
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    change_data = {"username": "updated_username"}
    response = api_client.patch(url, change_data)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_to_patch_nonexistent_user_information(api_client, admin_user):
    api_client.force_authenticate(admin_user)
    nonexistent_user = uuid4()
    url = reverse("user_account-detail", kwargs={"pk": nonexistent_user})

    change_data = {"username": "updated_username"}
    response = api_client.patch(url, change_data)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("username", "updated_username"), ("email", "updated_email@example.com")],
)
def test_successes_to_patch_user_information_by_current_user(
    api_client, test_user, test_comments, field, data
):
    user_fields = {"id", "username", "email", "created_at", "updated_at", "comments"}
    comment_fields = {"id", "body", "created_at", "player"}
    player_fields = {"id", "first_name", "last_name", "team"}
    team_fields = {"id", "name"}

    url = reverse("user_account_me")
    api_client.force_authenticate(user=test_user)

    change_data = {field: data}
    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data

    user_data = response.data
    assert set(user_data.keys()) == user_fields

    comment_data = user_data["comments"][0]
    assert set(comment_data.keys()) == comment_fields

    player_data = comment_data["player"]
    assert set(player_data.keys()) == player_fields

    team_data = player_data["team"]
    assert set(team_data.keys()) == team_fields


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("username", "updated_username"), ("email", "updated_email@example.com")],
)
def test_fails_to_patch_user_information_by_unauthenticated_user(
    api_client, test_user, field, data
):
    url = reverse("user_account_me")

    change_data = {field: data}
    response = api_client.patch(url, change_data)

    assert response.status_code == 401
