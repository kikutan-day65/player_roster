import pytest

from core.tests.test_base import TestBase
from roster.serializers.team import (
    TeamCreateSerializer,
    TeamListRetrieveAdminSerializer,
    TeamListRetrievePublicSerializer,
    TeamPatchSerializer,
    TeamPlayerListAdminSerializer,
    TeamPlayerListPublicSerializer,
)


@pytest.mark.django_db
class TestTeamCreateSerializer(TestBase):
    def test_success_to_validate_and_save_team_data(self, team_data):
        serializer = TeamCreateSerializer(data=team_data)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "name", "sport", "created_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output["name"] == team_data["name"]
        assert output["sport"] == team_data["sport"]

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, target_field, value, team_data):
        team_data[target_field] = value
        serializer = TeamCreateSerializer(data=team_data)

        assert serializer.is_valid()

        validated_data = serializer.validated_data

        assert target_field not in validated_data

    @pytest.mark.parametrize("missing_field", ["name", "sport"])
    def test_fails_to_validate_when_required_fields_are_missing(
        self, missing_field, team_data
    ):
        team_data.pop(missing_field)
        serializer = TeamCreateSerializer(data=team_data)

        assert serializer.is_valid() is False
        assert missing_field in serializer.errors


@pytest.mark.django_db
class TestTeamListRetrievePublicSerializer(TestBase):
    def test_success_to_serialize_team_instance(self, teams):
        team = teams[0]
        serializer = TeamListRetrievePublicSerializer(team)
        output = serializer.data

        expected_fields = ["id", "name", "sport", "created_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestTeamListRetrieveAdminSerializer(TestBase):
    def test_success_to_serialize_team_instance(self, teams):
        team = teams[0]
        serializer = TeamListRetrieveAdminSerializer(team)
        output = serializer.data

        expected_fields = [
            "id",
            "name",
            "sport",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        self.assert_expected_fields(output, expected_fields)


@pytest.mark.django_db
class TestTeamPatchSerializer(TestBase):
    @pytest.mark.parametrize(
        "target_field, value", [("name", "Patch Team Name"), ("sport", "basketball")]
    )
    def test_success_to_validate_and_save_team_data_with_single_field(
        self, target_field, value, teams
    ):
        patch_data = {target_field: value}
        team = teams[0]
        serializer = TeamPatchSerializer(team, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "name", "sport", "created_at", "updated_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output[target_field] == value

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, target_field, value, teams):
        patch_data = {target_field: value}
        team = teams[0]
        serializer = TeamPatchSerializer(team, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


@pytest.mark.django_db
class TestTeamPlayerListPublicSerializer(TestBase):
    def test_success_to_serialize_player_instance_on_team(self, players):
        player = players[0]
        serializer = TeamPlayerListPublicSerializer(player)
        output = serializer.data

        expected_fields = ["id", "first_name", "last_name", "created_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["team", "updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestTeamPlayerListAdminSerializer(TestBase):
    def test_success_to_serialize_player_instance_on_team(self, players):
        player = players[0]
        serializer = TeamPlayerListAdminSerializer(player)
        output = serializer.data

        expected_fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["team"]
        self.assert_unexpected_fields(output, unexpected_fields)
