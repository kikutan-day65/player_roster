from uuid import uuid4

import pytest

from core.tests.test_base import TestBase
from roster.models import Player


@pytest.mark.django_db
class TestPlayerViewSet(TestBase):
    # ========================================================================
    # Create Action - Positive Cases
    # ========================================================================
    def test_create_returns_201_and_allows_admin_user(
        self, api_client, player_list_url, admin_user, player_data
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 201

    def test_create_saves_player_to_database(
        self, api_client, player_list_url, admin_user, player_data
    ):
        api_client.force_authenticate(user=admin_user)

        before = Player.objects.count()
        api_client.post(player_list_url, data=player_data)
        after = Player.objects.count()

        assert after == before + 1

    def test_create_uses_correct_serializer_and_returns_correct_response(
        self, api_client, player_list_url, admin_user, player_data
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(player_list_url, data=player_data)

        player_data = response.data
        expected_fields = {"id", "first_name", "last_name", "created_at", "team"}

        assert set(player_data.keys()) == expected_fields

        nested_team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team_data.keys()) == team_expected_fields

    # ========================================================================
    # Create Action - Negative Cases
    # ========================================================================
    def test_create_returns_401_for_anonymous_user(
        self, api_client, player_list_url, player_data
    ):
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 401

    def test_create_returns_403_for_general_user(
        self, api_client, player_list_url, player_data, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 403

    @pytest.mark.parametrize("field", ["first_name", "last_name", "team_id"])
    def test_create_fails_without_required_fields(
        self, field, api_client, player_list_url, player_data, admin_user
    ):
        player_data.pop(field)
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 400
        assert field in response.data

    def test_create_fails_due_to_nonexistent_team_id(
        self, api_client, player_list_url, player_data, admin_user
    ):
        nonexistent_team_id = uuid4()
        player_data["team_id"] = nonexistent_team_id
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "field, value",
        [("first_name", "invalid@firstname"), ("last_name", "invalid@lastname")],
    )
    def test_create_fails_when_only_letters_validator_violation(
        self, field, value, api_client, player_list_url, player_data, admin_user
    ):
        player_data[field] = value
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(player_list_url, data=player_data)

        assert response.status_code == 400
        assert field in response.data

    # ========================================================================
    # List Action - Positive Cases
    # ========================================================================
    def test_list_returns_200_and_allows_anonymous_user(
        self, api_client, player_list_url, players
    ):
        response = api_client.get(player_list_url)

        assert response.status_code == 200

    def test_list_get_soft_deleted_player_for_admin(
        self, api_client, player_list_url, players, admin_user
    ):
        players[0].soft_delete()
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(player_list_url)

        items = [item["id"] for item in response.data["results"]]

        assert str(players[0].id) in items

    def test_list_cannot_get_soft_deleted_player_for_public(
        self, api_client, player_list_url, players
    ):
        players[0].soft_delete()
        response = api_client.get(player_list_url)

        items = [item["id"] for item in response.data["results"]]

        assert str(players[0].id) not in items

    def test_list_uses_correct_serializer_and_returns_correct_fields_for_public(
        self, api_client, player_list_url, players
    ):
        response = api_client.get(player_list_url)

        player_data = response.data["results"][0]
        expected_fields = {"id", "first_name", "last_name", "created_at", "team"}

        assert set(player_data.keys()) == expected_fields

        nested_team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team_data.keys()) == team_expected_fields

    def test_list_uses_correct_serializer_and_returns_correct_fields_for_admin(
        self, api_client, player_list_url, players, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(player_list_url)

        player_data = response.data["results"][0]
        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team",
        }

        assert set(player_data.keys()) == expected_fields

        nested_team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team_data.keys()) == team_expected_fields

    def test_list_returns_in_descending_order(
        self, api_client, player_list_url, players
    ):
        response = api_client.get(player_list_url)

        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    # ========================================================================
    # Retrieve Action - Positive Cases
    # ========================================================================
    def test_retrieve_returns_200_and_allows_anonymous_user(
        self, api_client, player_detail_url, players
    ):
        player_id = players[0].id
        url = player_detail_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_can_get_soft_deleted_user_for_admin(
        self, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id
        player.soft_delete()

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_cannot_get_soft_deleted_user_for_public(
        self, api_client, player_detail_url, players
    ):
        player = players[0]
        player_id = player.id
        player.soft_delete()

        url = player_detail_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 404

    def test_retrieve_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, player_detail_url, players
    ):
        player_id = players[0].id
        url = player_detail_url(player_id)
        response = api_client.get(url)

        player_data = response.data
        expected_fields = {"id", "first_name", "last_name", "created_at", "team"}

        assert set(player_data.keys()) == expected_fields

        nested_team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team_data.keys()) == team_expected_fields

    def test_retrieve_uses_correct_serializer_and_returns_correct_fields_for_admin(
        self, api_client, player_detail_url, players, admin_user
    ):
        player_id = players[0].id
        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        response = api_client.get(url)

        player_data = response.data
        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team",
        }

        assert set(player_data.keys()) == expected_fields

        nested_team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team_data.keys()) == team_expected_fields

    # ========================================================================
    # Retrieve Action - Negative Cases
    # ========================================================================
    def test_retrieve_returns_404_due_to_nonexistent_player(
        self, api_client, player_detail_url
    ):
        player_id = uuid4()
        url = player_detail_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 404

    # ========================================================================
    # Patch Action - Positive Cases
    # ========================================================================
    @pytest.mark.parametrize(
        "field, value",
        [("first_name", "PatchFirstName"), ("last_name", "PatchLastName")],
    )
    def test_patch_returns_200_and_allows_admin_user(
        self, field, value, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    def test_patch_returns_200_and_allows_admin_user_with_team_id(
        self, api_client, player_detail_url, players, teams, admin_user
    ):
        player = players[0]
        player_id = player.id

        team_id = teams[1].id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {"team_id": team_id}
        response = api_client.patch(url, data=patch_data)

        print(team_id)
        print(response.data["team"]["id"])

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field, value",
        [("first_name", "PatchFirstName"), ("last_name", "PatchLastName")],
    )
    def test_patch_only_allowed_fields_are_changed(
        self, field, value, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        assert response.data[field] == value

    def test_patch_only_allowed_fields_are_changed_with_team_id(
        self, api_client, player_detail_url, players, teams, admin_user
    ):
        player = players[0]
        player_id = player.id

        team_id = teams[1].id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {"team_id": team_id}
        response = api_client.patch(url, data=patch_data)

        assert response.data["team"]["id"] == str(team_id)

    @pytest.mark.parametrize(
        "field, value",
        [("id", uuid4()), ("created_at", "2020-01-01")],
    )
    def test_patch_not_allowed_fields_are_unchanged(
        self, field, value, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {field: value}

        original_value = getattr(player, field)

        api_client.patch(url, data=patch_data)

        player.refresh_from_db()

        assert getattr(player, field) == original_value

    def test_patch_get_soft_deleted_player(
        self, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player.soft_delete()
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {"first_name": "PatchFirstName"}
        response = api_client.patch(url, data=patch_data)

        assert str(player.id) == response.data["id"]

    @pytest.mark.parametrize(
        "field, value",
        [("first_name", "PatchFirstName"), ("last_name", "PatchLastName")],
    )
    def test_patch_uses_correct_serializer_and_returns_correct_response(
        self, field, value, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        player_data = response.data
        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "team",
        }

        assert set(player_data.keys()) == expected_fields

        nested_team = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team.keys()) == team_expected_fields

    def test_patch_uses_correct_serializer_and_returns_correct_response_with_team_id(
        self, api_client, player_detail_url, players, teams, admin_user
    ):
        player = players[0]
        player_id = player.id

        team_id = teams[1].id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {"team_id": team_id}
        response = api_client.patch(url, data=patch_data)

        player_data = response.data
        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "team",
        }

        assert set(player_data.keys()) == expected_fields

        nested_team = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(nested_team.keys()) == team_expected_fields

    # ========================================================================
    # Patch Action - Negative Cases
    # ========================================================================
    def test_patch_returns_401_for_anonymous_user(
        self, api_client, player_detail_url, players
    ):
        player = players[0]
        player_id = player.id

        url = player_detail_url(player_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 401

    def test_patch_returns_403_for_general_user(
        self, api_client, player_detail_url, general_user, players
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=general_user)
        url = player_detail_url(player_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 403

    def test_patch_fails_due_to_nonexistent_team_id(
        self, api_client, player_detail_url, admin_user, players
    ):
        player = players[0]
        player_id = player.id

        nonexistent_team_id = uuid4()

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {"team_id": nonexistent_team_id}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert "team_id" in response.data

    def test_patch_fails_due_to_nonexistent_player(
        self, api_client, player_detail_url, admin_user
    ):
        player_id = uuid4()

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "field, value",
        [("first_name", "Invalid@FirstName"), ("last_name", "Invalid@LastName")],
    )
    def test_patch_fails_due_to_only_letters_validator_violation(
        self, field, value, api_client, player_detail_url, players, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert field in response.data

    # ========================================================================
    # Destroy Action - Positive Cases
    # ========================================================================
    def test_delete_returns_204_and_allows_super_user(
        self, api_client, player_detail_url, players, super_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=super_user)
        url = player_detail_url(player_id)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_sets_deleted_at_field(
        self, api_client, player_detail_url, super_user, players
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=super_user)
        url = player_detail_url(player_id)
        api_client.delete(url)

        player.refresh_from_db()

        assert player.deleted_at is not None

    # ========================================================================
    # Destroy Action - Negative Cases
    # ========================================================================
    def test_delete_returns_401_for_anonymous_user(
        self, api_client, player_detail_url, players
    ):
        player_id = players[0].id
        url = player_detail_url(player_id)
        response = api_client.delete(url)

        assert response.status_code == 401

    def test_delete_returns_403_for_general_user(
        self, api_client, player_detail_url, general_user, players
    ):
        player_id = players[0].id
        api_client.force_authenticate(user=general_user)
        url = player_detail_url(player_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_returns_403_for_admin_user(
        self, api_client, player_detail_url, admin_user, players
    ):
        player_id = players[0].id
        api_client.force_authenticate(user=admin_user)
        url = player_detail_url(player_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_fails_due_to_nonexistent_player(
        self, api_client, player_detail_url, super_user
    ):
        nonexistent_player_id = uuid4()
        api_client.force_authenticate(user=super_user)
        url = player_detail_url(nonexistent_player_id)
        response = api_client.delete(url)

        assert response.status_code == 404

    # ========================================================================
    # Comments Action - Positive Cases
    # ========================================================================
    def test_comments_returns_200_and_allows_anonymous_user(
        self, api_client, player_comments_url, players, comments
    ):
        player = players[0]
        player_id = player.id

        url = player_comments_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_comments_can_get_soft_deleted_comments_for_admin(
        self, api_client, player_comments_url, players, comments, admin_user
    ):
        player = players[0]
        player_id = player.id

        comment = comments[0]
        comment.soft_delete()
        comment_id = comment.id

        api_client.force_authenticate(user=admin_user)
        url = player_comments_url(player_id)
        response = api_client.get(url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(comment_id) in ids

    def test_comments_cannot_get_soft_deleted_comments_for_public(
        self, api_client, player_comments_url, players, comments
    ):
        player = players[0]
        player_id = player.id

        comment = comments[0]
        comment.soft_delete()
        comment_id = comment.id

        url = player_comments_url(player_id)
        response = api_client.get(url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(comment_id) not in ids

    def test_comments_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, player_comments_url, players, comments
    ):
        player = players[0]
        player_id = player.id

        url = player_comments_url(player_id)
        response = api_client.get(url)

        comment_data = response.data["results"][0]
        expected_fields = {"id", "body", "created_at", "updated_at", "user"}

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

    def test_comments_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, player_comments_url, players, comments, admin_user
    ):
        player = players[0]
        player_id = player.id

        api_client.force_authenticate(user=admin_user)
        url = player_comments_url(player_id)
        response = api_client.get(url)

        comment_data = response.data["results"][0]
        expected_fields = {
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "user",
        }

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

    def test_comments_returns_in_descending_order(
        self, api_client, player_comments_url, players, comments
    ):
        player_id = players[0].id

        url = player_comments_url(player_id)
        response = api_client.get(url)

        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    # ========================================================================
    # Comments Action - Negative Cases
    # ========================================================================
    def test_comments_returns_404_due_to_nonexistent_player(
        self, api_client, player_comments_url
    ):
        player_id = uuid4()
        url = player_comments_url(player_id)
        response = api_client.get(url)

        assert response.status_code == 404
