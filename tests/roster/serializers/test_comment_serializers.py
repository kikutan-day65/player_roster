import pytest

from core.tests.test_base import TestBase
from roster.serializers.comment import (
    CommentCreateSerializer,
    CommentListRetrieveAdminSerializer,
    CommentListRetrievePublicSerializer,
    CommentPatchSerializer,
)


@pytest.mark.django_db
class TestCommentCreateSerializer(TestBase):
    def test_success_to_validate_and_save_comment_data(
        self, comment_data, general_user
    ):
        serializer = CommentCreateSerializer(data=comment_data)

        assert serializer.is_valid() is True

        serializer.save(user=general_user)
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "player"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["user", "updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output["body"] == comment_data["body"]

        player_output = output["player"]
        assert player_output["id"] == str(comment_data["player_id"])

        assert isinstance(output["player"], dict)
        assert "team" in output["player"]

    @pytest.mark.parametrize(
        "target_field, value", [("id", "dummy_id"), ("created_at", "dummy_date")]
    )
    def test_success_to_ignore_read_only_fields(
        self, target_field, value, comment_data
    ):
        comment_data[target_field] = value
        serializer = CommentCreateSerializer(data=comment_data)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data

    @pytest.mark.parametrize("missing_field", ["player_id", "body"])
    def test_fails_to_validate_when_missing_required_fields(
        self, missing_field, comment_data
    ):
        comment_data.pop(missing_field)
        serializer = CommentCreateSerializer(data=comment_data)

        assert serializer.is_valid() is False
        assert missing_field in serializer.errors


@pytest.mark.django_db
class TestCommentListRetrievePublicSerializer(TestBase):
    def test_success_to_serialize_comment_instance(self, comments):
        comment = comments[0]
        serializer = CommentListRetrievePublicSerializer(comment)
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "updated_at", "player", "user"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert isinstance(output["player"], dict)
        assert "team" in output["player"]


@pytest.mark.django_db
class TestCommentListRetrieveAdminSerializer(TestBase):
    def test_success_to_serialize_comment_instance(self, comments):
        comment = comments[0]
        serializer = CommentListRetrieveAdminSerializer(comment)
        output = serializer.data

        expected_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
            "user",
        ]
        self.assert_expected_fields(output, expected_fields)

        assert isinstance(output["player"], dict)
        assert "team" in output["player"]


@pytest.mark.django_db
class TestCommentPatchSerializer(TestBase):
    @pytest.mark.parametrize("target_field, value", [("body", "Patch Comment Body")])
    def test_success_to_validate_and_save_comment_data_with_single_field(
        self, target_field, value, comments
    ):
        comment = comments[0]
        patch_data = {target_field: value}
        serializer = CommentPatchSerializer(comment, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "updated_at", "player"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["user", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert isinstance(output["player"], dict)
        assert "team" in output["player"]

        assert output[target_field] == value

    def test_success_to_validate_and_save_comment_data_with_player_id(
        self, comments, players
    ):
        comment = comments[0]
        player_id = players[1].id
        patch_data = {"player_id": player_id}
        serializer = CommentPatchSerializer(comment, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        player_output = serializer.data["player"]

        assert player_output["id"] == str(patch_data["player_id"])

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, target_field, value, comments):
        comment = comments[0]
        patch_data = {target_field: value}
        serializer = CommentPatchSerializer(comment, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data
