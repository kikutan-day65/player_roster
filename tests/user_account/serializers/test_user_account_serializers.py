import pytest

from user_account.serializers import (
    MeCommentListRetrieveSerializer,
    MeCommentPatchSerializer,
    MePatchSerializer,
    MeRetrieveSerializer,
    UserAccountCommentListRetrieveAdminSerializer,
    UserAccountCommentListRetrievePublicSerializer,
    UserAccountCreateSerializer,
    UserAccountListRetrieveAdminSerializer,
    UserAccountListRetrievePublicSerializer,
    UserAccountPatchSerializer,
)


# ==========================================================
# UserAccountCreateSerializer
# ==========================================================
class TestUserAccountCreateSerializer:
    @pytest.mark.django_db
    def test_success_to_validate_and_save_user_data(self, general_user_data):
        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid() is True

        user = serializer.save()
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at"]
        for field in expected_fields:
            assert field in output

        unexpected_field = ["password"]
        for field in unexpected_field:
            assert field not in output

        assert output["username"] == general_user_data["username"]
        assert output["email"] == general_user_data["email"]

        assert user.check_password(general_user_data["password"])

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(self, field, value, general_user_data):
        general_user_data[field] = value
        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid()

        validated_data = serializer.validated_data

        assert "id" not in validated_data
        assert "created_at" not in validated_data

    @pytest.mark.django_db
    @pytest.mark.parametrize("field", ["username", "email", "password"])
    def test_fails_to_validate_without_required_fields(self, field, general_user_data):
        general_user_data.pop(field)
        serializer = UserAccountCreateSerializer(data=general_user_data)

        assert serializer.is_valid() is False
        assert field in serializer.errors


# ==========================================================
# UserAccountListRetrievePublicSerializer
# ==========================================================
class TestUserAccountListRetrievePublicSerializer:
    @pytest.mark.django_db
    def test_success_to_serialize_user_data(self, general_user):
        serializer = UserAccountListRetrievePublicSerializer(general_user)
        output = serializer.data

        expected_fields = ["id", "username", "created_at"]
        for field in expected_fields:
            assert field in output

        unexpected_field = [
            "email",
            "password" "is_superuser",
            "is_staff",
            "is_active",
            "updated_at",
            "delete_at",
        ]
        for field in unexpected_field:
            assert field not in output

        assert output["id"] == str(general_user.id)
        assert output["username"] == general_user.username


# ==========================================================
# UserAccountListRetrieveAdminSerializer
# ==========================================================
class TestUserAccountListRetrieveAdminSerializer:
    @pytest.mark.django_db
    def test_success_to_serialize_user_data(self, general_user):
        serializer = UserAccountListRetrieveAdminSerializer(general_user)
        output = serializer.data

        expected_field = [
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
        for field in expected_field:
            assert field in output

        assert output["id"] == str(general_user.id)
        assert output["username"] == general_user.username
        assert output["email"] == general_user.email
        assert output["is_superuser"] == general_user.is_superuser
        assert output["is_staff"] == general_user.is_staff
        assert output["is_active"] == general_user.is_active


# ==========================================================
# UserAccountPatchSerializer
# ==========================================================
class TestUserAccountPatchSerializer:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("username", "patch_username"),
            ("email", "patch_email@example.com"),
            ("is_active", False),
        ],
    )
    def test_success_to_validate_and_save_with_single_target_field(
        self, target_field, value, general_user
    ):
        partial_data = {target_field: value}
        serializer = UserAccountPatchSerializer(
            instance=general_user, data=partial_data, partial=True
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
        for field in expected_fields:
            assert field in output

        unexpected_fields = ["password", "deleted_at"]
        for field in unexpected_fields:
            assert field not in output

        assert output[target_field] == value

    @pytest.mark.django_db
    def test_success_to_validate_and_save_with_all_fields(
        self, general_user_patch_data, general_user
    ):
        serializer = UserAccountPatchSerializer(
            instance=general_user, data=general_user_patch_data, partial=True
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
        for field in expected_fields:
            assert field in output

        unexpected_fields = ["password", "deleted_at"]
        for field in unexpected_fields:
            assert field not in output

        assert output["username"] == general_user_patch_data["username"]
        assert output["email"] == general_user_patch_data["email"]
        assert output["is_active"] == general_user_patch_data["is_active"]

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("password", "Password123"),
            ("is_superuser", True),
            ("is_staff", True),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_fields(
        self, target_field, value, general_user
    ):
        ignored_field = {target_field: value}
        serializer = UserAccountPatchSerializer(
            instance=general_user, data=ignored_field, partial=True
        )

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


# ==========================================================
# UserAccountCommentListRetrievePublicSerializer
# ==========================================================
class TestUserAccountCommentListRetrievePublicSerializer:
    @pytest.mark.django_db
    def test_success_to_serialize_comment_data_on_user(self, comments):
        serializer = UserAccountCommentListRetrievePublicSerializer(comments[0])

        comment_output = serializer.data

        comment_expected_fields = ["id", "body", "created_at", "updated_at", "player"]
        for field in comment_expected_fields:
            assert field in comment_expected_fields

        comment_unexpected_fields = ["user", "deleted_at"]
        for field in comment_unexpected_fields:
            assert field not in comment_output

        assert comment_output["id"] == str(comments[0].id)
        assert comment_output["body"] == comments[0].body

        nested_player_output = comment_output["player"]

        player_expected_fields = ["id", "first_name", "last_name", "team"]
        for field in player_expected_fields:
            assert field in nested_player_output

        player_unexpected_fields = ["created_at", "updated_at", "deleted_at"]
        for field in player_unexpected_fields:
            assert field not in nested_player_output

        nested_team_output = nested_player_output["team"]

        team_expected_field = ["id", "name"]
        for field in team_expected_field:
            assert field in nested_team_output

        team_unexpected_field = ["sport", "created_at", "updated_at", "deleted_at"]
        for field in team_unexpected_field:
            assert field not in nested_team_output


# ==========================================================
# UserAccountCommentListRetrieveAdminSerializer
# ==========================================================
class TestUserAccountCommentListRetrieveAdminSerializer:
    @pytest.mark.django_db
    def test_success_to_serialize_comment_data_on_user(self, comments):
        serializer = UserAccountCommentListRetrieveAdminSerializer(comments[0])

        comment_output = serializer.data

        comment_expected_field = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
        ]
        for field in comment_expected_field:
            assert field in comment_output

        comment_unexpected_field = ["user"]
        for field in comment_unexpected_field:
            assert field not in comment_output

        assert comment_output["id"] == str(comments[0].id)
        assert comment_output["body"] == comments[0].body

        nested_player_output = comment_output["player"]

        player_expected_fields = ["id", "first_name", "last_name", "team"]
        for field in player_expected_fields:
            assert field in nested_player_output

        player_unexpected_fields = ["created_at", "updated_at", "deleted_at"]
        for field in player_unexpected_fields:
            assert field not in nested_player_output

        nested_team_output = nested_player_output["team"]

        team_expected_field = ["id", "name"]
        for field in team_expected_field:
            assert field in nested_team_output

        team_unexpected_field = ["sport", "created_at", "updated_at", "deleted_at"]
        for field in team_unexpected_field:
            assert field not in nested_team_output


# ==========================================================
# MeRetrieveSerializer
# ==========================================================
class TestMeRetrieveSerializer:
    @pytest.mark.django_db
    def test_success_to_serializer_current_user_data(self, general_user):
        serializer = MeRetrieveSerializer(general_user)
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in output

        unexpected_fields = ["is_superuser", "is_staff", "is_active", "deleted_at"]
        for field in unexpected_fields:
            assert field not in output

        assert output["id"] == str(general_user.id)
        assert output["username"] == general_user.username
        assert output["email"] == general_user.email


# ==========================================================
# MePatchSerializer
# ==========================================================
class TestMePatchSerializer:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("username", "patch_username"),
            ("email", "patch_email@example.com"),
        ],
    )
    def test_success_to_validate_and_save_with_single_field(
        self, target_field, value, general_user
    ):
        patch_data = {target_field: value}
        serializer = MePatchSerializer(
            instance=general_user, data=patch_data, partial=True
        )

        assert serializer.is_valid()

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in output

        unexpected_fields = ["password", "deleted_at"]
        for field in unexpected_fields:
            assert field not in output

        assert output[target_field] == value

    @pytest.mark.django_db
    def test_success_to_validate_and_save_with_all_fields(
        self, general_user_patch_data, general_user
    ):
        serializer = MePatchSerializer(
            instance=general_user, data=general_user_patch_data, partial=True
        )

        assert serializer.is_valid() is True

        serializer.save()
        output = serializer.data

        expected_fields = ["id", "username", "email", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in output

        unexpected_fields = ["password", "deleted_at"]
        for field in unexpected_fields:
            assert field not in output

        assert output["username"] == general_user.username
        assert output["email"] == general_user.email

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("password", "Password123"),
            ("is_superuser", True),
            ("is_staff", True),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_field(self, target_field, value, general_user):
        patch_data = {target_field: value}
        serializer = MePatchSerializer(
            instance=general_user, data=patch_data, partial=True
        )

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data


class TestMeCommentListRetrieveSerializer:
    @pytest.mark.django_db
    def test_success_to_validate_and_save_comment_data_on_current_user(self, comments):
        serializer = MeCommentListRetrieveSerializer(comments[0])
        comment_output = serializer.data

        comment_expected_fields = ["id", "body", "created_at", "updated_at", "player"]
        for field in comment_expected_fields:
            assert field in comment_expected_fields

        comment_unexpected_fields = ["user", "deleted_at"]
        for field in comment_unexpected_fields:
            assert field not in comment_output

        assert comment_output["id"] == str(comments[0].id)
        assert comment_output["body"] == comments[0].body

        nested_player_output = comment_output["player"]

        player_expected_fields = ["id", "first_name", "last_name", "team"]
        for field in player_expected_fields:
            assert field in nested_player_output

        player_unexpected_fields = ["created_at", "updated_at", "deleted_at"]
        for field in player_unexpected_fields:
            assert field not in nested_player_output

        nested_team_output = nested_player_output["team"]

        team_expected_field = ["id", "name"]
        for field in team_expected_field:
            assert field in nested_team_output

        team_unexpected_field = ["sport", "created_at", "updated_at", "deleted_at"]
        for field in team_unexpected_field:
            assert field not in nested_team_output


class TestMeCommentPatchSerializer:
    @pytest.mark.django_db
    def test_success_to_validate_and_save_with_single_field(self, comments):
        patch_data = {"body": "Patch Comment Body"}
        serializer = MeCommentPatchSerializer(
            instance=comments[0], data=patch_data, partial=True
        )

        assert serializer.is_valid() is True

        serializer.save()
        comment_output = serializer.data

        comment_expected_field = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "player",
        ]
        for field in comment_expected_field:
            assert field in comment_output

        comment_unexpected_field = ["user"]
        for field in comment_unexpected_field:
            assert field not in comment_output

        assert comment_output["id"] == str(comments[0].id)
        assert comment_output["body"] == comments[0].body

        nested_player_output = comment_output["player"]

        player_expected_fields = ["id", "first_name", "last_name", "team"]
        for field in player_expected_fields:
            assert field in nested_player_output

        player_unexpected_fields = ["created_at", "updated_at", "deleted_at"]
        for field in player_unexpected_fields:
            assert field not in nested_player_output

        nested_team_output = nested_player_output["team"]

        team_expected_field = ["id", "name"]
        for field in team_expected_field:
            assert field in nested_team_output

        team_unexpected_field = ["sport", "created_at", "updated_at", "deleted_at"]
        for field in team_unexpected_field:
            assert field not in nested_team_output

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "target_field, value",
        [
            ("id", "dummy_id"),
            ("created_at", "dummy_date"),
            ("updated_at", "dummy_date"),
            ("deleted_at", "dummy_date"),
        ],
    )
    def test_success_to_ignore_read_only_field(self, target_field, value, comments):
        patch_data = {target_field: value}
        serializer = MeCommentPatchSerializer(
            instance=comments[0], data=patch_data, partial=True
        )

        assert serializer.is_valid() is True

        validated_data = serializer.validated_data

        assert target_field not in validated_data
