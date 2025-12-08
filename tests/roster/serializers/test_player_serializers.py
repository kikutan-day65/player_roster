import pytest

from core.tests.test_base import TestBase
from roster.serializers.player import (
    PlayerCommentListAdminSerializer,
    PlayerCommentListPublicSerializer,
    PlayerCreateSerializer,
    PlayerListRetrieveAdminSerializer,
    PlayerListRetrievePublicSerializer,
    PlayerPatchSerializer,
)


@pytest.mark.django_db
class TestPlayerCreateSerializer(TestBase):
    def test_success_to_validate_and_save_player_data(self, player_data):
        serializer = PlayerCreateSerializer(data=player_data)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "first_name", "last_name", "created_at", "team"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output["first_name"] == player_data["first_name"]
        assert output["last_name"] == player_data["last_name"]

        nested_team_output = output["team"]
        assert nested_team_output["id"] == player_data["team_id"]

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, target_field, value, player_data):
        player_data[target_field] = value
        serializer = PlayerCreateSerializer(data=player_data)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data

    @pytest.mark.parametrize("missing_field", ["team_id", "first_name", "last_name"])
    def test_fails_to_validation_when_missing_required_fields(
        self, missing_field, player_data
    ):
        player_data.pop(missing_field)
        serializer = PlayerCreateSerializer(data=player_data)

        assert serializer.is_valid() is False
        assert missing_field in serializer.errors


@pytest.mark.django_db
class TestPlayerListRetrievePublicSerializer(TestBase):
    def test_success_to_serialize_player_instance(self, players):
        player = players[0]
        serializer = PlayerListRetrievePublicSerializer(player)
        output = serializer.data

        expected_fields = ["id", "first_name", "last_name", "created_at", "team"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestPlayerListRetrieveAdminSerializer(TestBase):
    def test_success_to_serialize_player_instance(self, players):
        player = players[0]
        serializer = PlayerListRetrieveAdminSerializer(player)
        output = serializer.data

        expected_fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team",
        ]
        self.assert_expected_fields(output, expected_fields)


@pytest.mark.django_db
class TestPlayerPatchSerializer(TestBase):
    @pytest.mark.parametrize(
        "target_field, value",
        [("first_name", "PatchFirstName"), ("last_name", "PatchLastName")],
    )
    def test_success_to_validate_and_save_player_data_with_single_field(
        self, target_field, value, players
    ):
        patch_data = {target_field: value}
        player = players[0]
        serializer = PlayerPatchSerializer(player, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "team",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output[target_field] == value

    def test_success_to_validate_and_save_player_data_with_team_id(
        self, players, teams
    ):
        team_id = teams[1].id
        patch_data = {"team_id": team_id}
        player = players[0]
        serializer = PlayerPatchSerializer(player, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        team_output = serializer.data["team"]

        assert team_output["id"] == str(patch_data["team_id"])

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("updated_at", "dummy_date"),
            ("deleted_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, target_field, value, players):
        patch_data = {target_field: value}
        player = players[0]
        serializer = PlayerPatchSerializer(player, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


@pytest.mark.django_db
class TestPlayerCommentListPublicSerializer(TestBase):
    def test_success_to_serialize_comment_instance_on_player(self, comments):
        comment = comments[0]
        serializer = PlayerCommentListPublicSerializer(comment)
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "updated_at", "user"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["player", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestPlayerCommentListAdminSerializer(TestBase):
    def test_success_to_serialize_comment_instance_on_player(self, comments):
        comment = comments[0]
        serializer = PlayerCommentListAdminSerializer(comment)
        output = serializer.data

        expected_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "user",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["player"]
        self.assert_unexpected_fields(output, unexpected_fields)
