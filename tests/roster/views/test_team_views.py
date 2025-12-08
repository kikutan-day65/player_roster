from uuid import uuid4

import pytest

from core.tests.test_base import TestBase
from roster.models import Team


@pytest.mark.django_db
class TestTeamViewSet(TestBase):
    # ========================================================================
    # Create Action - Positive Cases
    # ========================================================================
    def test_create_returns_201_and_allows_admin_user(
        self, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(team_list_url, data=team_data)

        assert response.status_code == 201

    def test_create_saves_team_to_database(
        self, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)

        before = Team.objects.count()
        api_client.post(team_list_url, data=team_data)
        after = Team.objects.count()

        assert after == before + 1

    def test_create_uses_correct_serializer_and_returns_correct_response(
        self, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(team_list_url, data=team_data)

        expected_fields = {"id", "name", "sport", "created_at"}

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Create Action - Negative Cases
    # ========================================================================
    def test_create_returns_401_for_anonymous_user(self, api_client, team_list_url):
        response = api_client.post(team_list_url)

        assert response.status_code == 401

    def test_create_returns_403_for_general_user(
        self, api_client, team_list_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.post(team_list_url)

        assert response.status_code == 403

    @pytest.mark.parametrize("field", ["name", "sport"])
    def test_create_fails_when_missing_required_field(
        self, field, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)
        team_data.pop(field)
        response = api_client.post(team_list_url, data=team_data)

        assert response.status_code == 400
        assert field in response.data

    def test_create_fails_with_invalid_choice(
        self, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)
        team_data["sport"] = "invalid choice"
        response = api_client.post(team_list_url, data=team_data)

        assert response.status_code == 400
        assert "sport" in response.data

    def test_create_fails_when_violating__only_letters_numerics_validator(
        self, api_client, team_list_url, admin_user, team_data
    ):
        api_client.force_authenticate(user=admin_user)
        team_data["name"] = "invalid@name"
        response = api_client.post(team_list_url, data=team_data)

        assert response.status_code == 400
        assert "name" in response.data

    # ========================================================================
    # List Action - Positive Cases
    # ========================================================================
    def test_list_returns_200_and_allows_anonymous_user(
        self, api_client, team_list_url, teams
    ):
        response = api_client.get(team_list_url)

        assert response.status_code == 200

    def test_list_excludes_soft_deleted_team_for_public_account(
        self, api_client, team_list_url, teams
    ):
        teams[0].soft_delete()
        response = api_client.get(team_list_url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(teams[0].id) not in ids

    def test_list_includes_soft_deleted_team_for_admin_account(
        self, api_client, team_list_url, admin_user, teams
    ):
        teams[0].soft_delete()
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(team_list_url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(teams[0].id) in ids

    def test_list_uses_correct_serializer_and_returns_expected_fields_for_public_account(
        self, api_client, team_list_url, teams
    ):
        response = api_client.get(team_list_url)
        data = response.data["results"][0]

        expected_fields = {"id", "name", "sport", "created_at"}

        assert set(data.keys()) == expected_fields

    def test_list_uses_correct_serializer_and_returns_expected_fields_for_admin_account(
        self, api_client, team_list_url, admin_user, teams
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(team_list_url)
        data = response.data["results"][0]

        expected_fields = {
            "id",
            "name",
            "sport",
            "created_at",
            "updated_at",
            "deleted_at",
        }

        assert set(data.keys()) == expected_fields

    def test_list_results_returned_in_descending_order(
        self, api_client, team_list_url, teams
    ):
        response = api_client.get(team_list_url)
        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    # ========================================================================
    # Retrieve Action - Positive Cases
    # ========================================================================
    def test_retrieve_returns_200_and_allows_anonymous_user(
        self, api_client, team_detail_url, teams
    ):
        team_id = teams[0].id
        url = team_detail_url(team_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_can_get_soft_deleted_team_for_admin_account(
        self, api_client, team_detail_url, teams, admin_user
    ):
        teams[0].soft_delete()
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_uses_correct_serializer_and_returns_expected_fields_for_public_account(
        self, api_client, team_detail_url, teams
    ):
        team_id = teams[0].id
        url = team_detail_url(team_id)
        response = api_client.get(url)

        expected_fields = {"id", "name", "sport", "created_at"}

        assert set(response.data.keys()) == expected_fields

    def test_retrieve_uses_correct_serializer_and_returns_expected_fields_for_admin_account(
        self, api_client, team_detail_url, teams, admin_user
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team_id)
        response = api_client.get(url)

        expected_fields = {
            "id",
            "name",
            "sport",
            "created_at",
            "updated_at",
            "deleted_at",
        }

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Retrieve Action - Negative Cases
    # ========================================================================
    def test_retrieve_returns_404_for_nonexistent_team(
        self, api_client, team_detail_url
    ):
        nonexistent_team_id = uuid4()
        url = team_detail_url(nonexistent_team_id)
        response = api_client.get(url)

        assert response.status_code == 404

    def test_retrieve_cannot_get_soft_deleted_team_for_public_account(
        self, api_client, team_detail_url, teams
    ):
        teams[0].soft_delete()
        team_id = teams[0].id
        url = team_detail_url(team_id)
        response = api_client.get(url)

        assert response.status_code == 404

    # ========================================================================
    # Patch Action - Positive Cases
    # ========================================================================
    @pytest.mark.parametrize(
        "field, value", [("name", "patch name"), ("sport", "football")]
    )
    def test_patch_returns_200_and_allows_admin_user(
        self, field, value, api_client, team_detail_url, admin_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        patch_data = {field: value}
        url = team_detail_url(team_id)
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field, value", [("name", "patch name"), ("sport", "football")]
    )
    def test_patch_only_allowed_fields_are_changed(
        self, field, value, api_client, team_detail_url, admin_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team_id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        assert response.data[field] == value

    @pytest.mark.parametrize(
        "field, value",
        [("id", uuid4()), ("created_at", "2020-01-01")],
    )
    def test_patch_not_allowed_fields_are_unchanged(
        self, field, value, api_client, team_detail_url, teams, admin_user
    ):
        team = teams[0]
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team.id)
        patch_data = {field: value}

        original_value = getattr(team, field)
        api_client.patch(url, data=patch_data)

        team.refresh_from_db()

        assert getattr(team, field) == original_value

    def test_patch_can_get_soft_deleted_team_for_admin(
        self, api_client, team_detail_url, teams, admin_user
    ):
        teams[0].soft_delete()
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team_id)
        patch_data = {"name": "patch name"}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    def test_patch_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, team_detail_url, teams, admin_user
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        patch_data = {"name": "patch name"}
        url = team_detail_url(team_id)
        response = api_client.patch(url, data=patch_data)

        expected_fields = {"id", "name", "sport", "created_at", "updated_at"}

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Patch Action - Negative Cases
    # ========================================================================
    def test_returns_401_for_anonymous_user(self, api_client, team_detail_url, teams):
        team_id = teams[0].id
        url = team_detail_url(team_id)
        response = api_client.patch(url)

        assert response.status_code == 401

    def test_returns_403_for_general_user(
        self, api_client, team_detail_url, teams, general_user
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=general_user)
        url = team_detail_url(team_id)
        response = api_client.patch(url)

        assert response.status_code == 403

    def test_patch_returns_404_when_nonexistent_team(
        self, api_client, team_detail_url, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        nonexistent_team_id = uuid4()
        url = team_detail_url(nonexistent_team_id)
        patch_data = {"name": "patch name"}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 404

    def test_patch_fails_due_to_invalid_choice(
        self, api_client, team_detail_url, admin_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        invalid_choice = "golf"
        url = team_detail_url(team_id)
        patch_data = {"sport": invalid_choice}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert "sport" in response.data

    def test_patch_fails_due_to_violating_only_letters_numerics_validator(
        self, api_client, team_detail_url, admin_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        invalid_name = "invalid@name"
        url = team_detail_url(team_id)
        patch_data = {"name": invalid_name}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert "name" in response.data

    # ========================================================================
    # Delete Action - Positive Cases
    # ========================================================================
    def test_delete_returns_204_and_allows_super_user(
        self, api_client, team_detail_url, super_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=super_user)
        url = team_detail_url(team_id)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_sets_deleted_at_field(
        self, api_client, team_detail_url, super_user, teams
    ):
        team = teams[0]
        api_client.force_authenticate(user=super_user)
        url = team_detail_url(team.id)
        api_client.delete(url)

        team.refresh_from_db()

        assert team.deleted_at is not None

    # ========================================================================
    # Delete Action - Negative Cases
    # ========================================================================
    def test_delete_returns_401_for_anonymous_user(
        self, api_client, team_detail_url, teams
    ):
        team_id = teams[0].id
        url = team_detail_url(team_id)
        response = api_client.delete(url)

        assert response.status_code == 401

    def test_delete_returns_403_for_general_user(
        self, api_client, team_detail_url, general_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=general_user)
        url = team_detail_url(team_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_returns_403_for_admin_user(
        self, api_client, team_detail_url, admin_user, teams
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_detail_url(team_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_fails_due_to_nonexistent_team(
        self, api_client, team_detail_url, super_user
    ):
        nonexistent_team_id = uuid4()
        api_client.force_authenticate(user=super_user)
        url = team_detail_url(nonexistent_team_id)
        response = api_client.delete(url)

        assert response.status_code == 404

    # ========================================================================
    # Players Action - Positive Cases
    # ========================================================================
    def test_players_returns_200_and_allows_anonymous_user(
        self, api_client, team_players_url, teams, players
    ):
        team_id = teams[0].id
        url = team_players_url(team_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_players_cannot_get_soft_deleted_player_for_public(
        self, api_client, team_players_url, teams, players
    ):
        players[0].soft_delete()
        team_id = teams[0].id
        url = team_players_url(team_id)
        response = api_client.get(url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(players[0].id) not in ids

    def test_players_can_get_soft_deleted_player_for_admin(
        self, api_client, team_players_url, admin_user, teams, players
    ):
        players[0].soft_delete()
        team_id = teams[0].id

        api_client.force_authenticate(user=admin_user)
        url = team_players_url(team_id)
        response = api_client.get(url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(players[0].id) in ids

    def test_players_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, team_players_url, teams, players
    ):
        team_id = teams[0].id
        url = team_players_url(team_id)
        response = api_client.get(url)
        data = response.data["results"][0]

        expected_fields = {"id", "first_name", "last_name", "created_at"}

        assert set(data.keys()) == expected_fields

    def test_players_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, team_players_url, admin_user, teams, players
    ):
        team_id = teams[0].id
        api_client.force_authenticate(user=admin_user)
        url = team_players_url(team_id)
        response = api_client.get(url)
        data = response.data["results"][0]

        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
        }

        assert set(data.keys()) == expected_fields

    def test_players_results_returned_in_descending_order(
        self, api_client, team_players_url, teams, players
    ):
        team_id = teams[0].id
        url = team_players_url(team_id)
        response = api_client.get(url)
        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order
