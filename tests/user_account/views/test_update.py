import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, data",
    [("username", "updated_username"), ("email", "updated_email@example.com")],
)
def test_successes_to_patch_user_information_by_admin_user(
    api_client, test_user, admin_user, field, data
):
    expected_fields = {"id", "username", "email", "created_at", "updated_at"}

    url = reverse("user_account-detail", kwargs={"pk": test_user.id})
    api_client.force_authenticate(user=admin_user)

    change_data = {field: data}
    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data
    assert set(response.data.keys()) == expected_fields


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
@pytest.mark.parametrize(
    "field, data",
    [("username", "updated_username"), ("email", "updated_email@example.com")],
)
def test_successes_to_patch_user_information_by_current_user(
    api_client, test_user, field, data
):
    expected_fields = {"id", "username", "email", "created_at", "updated_at"}

    url = reverse("user_account_me")
    api_client.force_authenticate(user=test_user)

    change_data = {field: data}
    response = api_client.patch(url, change_data)

    assert response.status_code == 200
    assert response.data[field] == data
    assert set(response.data.keys()) == expected_fields


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
