import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_successes_to_get_user_list_by_admin_user(api_client, test_user, admin_user):
    expected_fields = {
        "id",
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    url = reverse("user_account-list")
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert set(response.data[0].keys()) == expected_fields


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
def test_successes_to_get_specific_user_by_authenticated_user(
    api_client, test_user_2, test_user
):
    expected_fields = {"id", "username", "created_at", "updated_at"}

    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == expected_fields


@pytest.mark.django_db
def test_fails_to_get_specific_user_by_unauthenticated_user(api_client, test_user_2):
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})

    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_successes_to_get_current_user_by_authenticated_user(api_client, test_user):
    expected_fields = {"id", "username", "email", "created_at", "updated_at"}

    url = reverse("user_account_me")
    api_client.force_authenticate(user=test_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == test_user.username
    assert response.data["email"] == test_user.email
    assert set(response.data.keys()) == expected_fields


@pytest.mark.django_db
def test_fails_to_get_current_user_by_unauthenticated_user(api_client):
    url = reverse("user_account_me")

    response = api_client.get(url)

    assert response.status_code == 401
