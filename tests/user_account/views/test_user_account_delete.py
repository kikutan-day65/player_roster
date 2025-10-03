import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_successes_to_delete_user_by_super_user(api_client, super_user, test_user):
    url = reverse("user_account-detail", kwargs={"pk": test_user.id})
    api_client.force_authenticate(user=super_user)

    response = api_client.delete(url)

    assert response.status_code == 204

    test_user.refresh_from_db()
    assert test_user.deleted_at is not None


@pytest.mark.django_db
def test_fails_to_delete_user_by_admin_user(api_client, admin_user, test_user):
    url = reverse("user_account-detail", kwargs={"pk": test_user.id})
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_delete_user_by_authenticated_user(api_client, test_user, test_user_2):
    url = reverse("user_account-detail", kwargs={"pk": test_user_2.id})
    api_client.force_authenticate(user=test_user)

    response = api_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_delete_user_by_unauthenticated_user(api_client, test_user):
    url = reverse("user_account-detail", kwargs={"pk": test_user.id})

    response = api_client.delete(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_to_delete_user_by_unauthenticated_user(api_client):
    url = reverse("user_account_me")

    response = api_client.delete(url)

    assert response.status_code == 401
