from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_successes_to_delete_player(api_client, test_players, super_user):
    api_client.force_authenticate(super_user)
    player = test_players[0]
    url = reverse("player-detail", kwargs={"pk": player.id})

    response = api_client.delete(url)

    assert response.status_code == 204

    player.refresh_from_db()
    assert player.deleted_at is not None


@pytest.mark.django_db
def test_fails_to_delete_player_by_admin_user(api_client, test_players, admin_user):
    api_client.force_authenticate(admin_user)
    player = test_players[0]
    url = reverse("player-detail", kwargs={"pk": player.id})

    response = api_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_delete_player_by_general_user(api_client, test_players, test_user):
    api_client.force_authenticate(test_user)
    player = test_players[0]
    url = reverse("player-detail", kwargs={"pk": player.id})

    response = api_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_fails_to_delete_player_by_unauthenticated_user(api_client, test_players):
    player = test_players[0]
    url = reverse("player-detail", kwargs={"pk": player.id})

    response = api_client.delete(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_fails_to_delete_nonexistent_player(api_client, super_user):
    api_client.force_authenticate(super_user)
    player_id = uuid4()
    url = reverse("player-detail", kwargs={"pk": player_id})

    response = api_client.delete(url)

    assert response.status_code == 404
