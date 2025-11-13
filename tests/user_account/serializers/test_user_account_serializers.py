import pytest

from core.tests.test_base import TestBase
from user_account.serializers import (
    MeCommentListSerializer,
    MePatchSerializer,
    MeRetrieveSerializer,
    UserAccountCommentListAdminSerializer,
    UserAccountCommentListPublicSerializer,
    UserAccountCreateSerializer,
    UserAccountListRetrieveAdminSerializer,
    UserAccountListRetrievePublicSerializer,
    UserAccountPatchSerializer,
)


@pytest.mark.django_db
class TestUserAccountCreateSerializer(TestBase):
    def test_success_to_validate_and_save_user_data(self, general_user_data):
        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid() is True

        user = serializer.save()
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "updated_at",
            "deleted_at",
        ]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output["username"] == general_user_data["username"]
        assert output["email"] == general_user_data["email"]

        assert user.check_password(general_user_data["password"]) is True

    @pytest.mark.parametrize(
        "target_field, value", [("id", "dummy_id"), ("created_at", "dummy_date")]
    )
    def test_success_to_ignore_read_only_fields(
        self, target_field, value, general_user_data
    ):
        general_user_data[target_field] = value
        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid() is True

        assert target_field not in serializer.validated_data

    @pytest.mark.parametrize("missing_field", ["username", "email", "password"])
    def test_fails_to_validate_when_required_field_is_missing(
        self, missing_field, general_user_data
    ):
        general_user_data.pop(missing_field)

        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid() is False
        assert missing_field in serializer.errors


@pytest.mark.django_db
class TestUserAccountListRetrievePublicSerializer(TestBase):
    def test_success_to_serialize_user_instance(self, general_user):
        serializer = UserAccountListRetrievePublicSerializer(general_user)
        output = serializer.data

        expected_fields = ["id", "username", "created_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = [
            "password",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "updated_at",
            "deleted_at",
        ]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestUserAccountListRetrieveAdminSerializer(TestBase):
    def test_success_to_serialize_user_instance(self, general_user):
        serializer = UserAccountListRetrieveAdminSerializer(general_user)
        output = serializer.data

        expected_fields = [
            "id",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["password"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestUserAccountPatchSerializer(TestBase):
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("username", "patch_user_name"),
            ("email", "path_email@example.com"),
            ("is_active", False),
        ],
    )
    def test_success_to_validate_and_save_user_data_with_single_field(
        self, target_field, value, general_user
    ):
        patch_data = {target_field: value}
        serializer = UserAccountPatchSerializer(
            general_user, data=patch_data, partial=True
        )

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = [
            "id",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["password", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert output[target_field] == value

    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("is_superuser", True),
            ("is_staff", True),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(
        self, target_field, value, general_user
    ):
        patch_data = {target_field: value}
        serializer = UserAccountPatchSerializer(
            general_user, data=patch_data, partial=True
        )

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


@pytest.mark.django_db
class TestUserAccountCommentListRetrievePublicSerializer(TestBase):
    def test_success_to_serialize_comment_instance_on_user(self, comments):
        comment = comments[0]
        serializer = UserAccountCommentListPublicSerializer(comment)
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "updated_at", "player"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["user", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        assert isinstance(output["player"], dict)
        assert "team" in output["player"]


@pytest.mark.django_db
class TestUserAccountCommentListRetrieveAdminSerializer(TestBase):
    def test_success_to_serialize_comment_instance_on_user(self, comments):
        comment = comments[0]
        serializer = UserAccountCommentListAdminSerializer(comment)
        output = serializer.data

        expected_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
        ]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["user"]
        self.assert_unexpected_fields(output, unexpected_fields)

        player_output = output["player"]
        assert "team" in player_output
        assert isinstance(player_output["team"], dict)


@pytest.mark.django_db
class TestMeRetrieveSerializer(TestBase):
    def test_success_to_serialize_current_user_instance(self, general_user):
        serializer = MeRetrieveSerializer(general_user)
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at", "updated_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "deleted_at",
        ]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestMePatchSerializer(TestBase):
    @pytest.mark.parametrize(
        "target_field, value",
        [("username", "patch_username"), ("email", "patch_email@example.com")],
    )
    def test_success_to_validate_and_save_current_user_data_with_single_field(
        self, target_field, value, general_user
    ):
        patch_data = {target_field: value}
        serializer = MePatchSerializer(general_user, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at", "updated_at"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "deleted_at",
        ]
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
    def test_success_to_ignore_read_only_fields(
        self, target_field, value, general_user
    ):
        patch_data = {target_field: value}
        serializer = MePatchSerializer(general_user, data=patch_data, partial=True)

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


@pytest.mark.django_db
class TestMeCommentListSerializer(TestBase):
    def test_success_to_serialize_comment_instance_on_current_user(self, comments):
        comment = comments[0]
        serializer = MeCommentListSerializer(comment)
        output = serializer.data

        expected_fields = ["id", "body", "created_at", "updated_at", "player"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["user", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)

        player_output = output["player"]
        assert "team" in player_output
        assert isinstance(player_output["team"], dict)
