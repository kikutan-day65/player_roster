from uuid import uuid4

import pytest

from core.tests.test_base import TestBase
from user_account.models import UserAccount
from user_account.serializers import UserAccountCreateSerializer
from user_account.views import UserAccountViewSet


@pytest.mark.django_db
class TestUserAccountViewSet(TestBase):
    # ========================================================================
    # Create Action - Positive Cases
    # ========================================================================
    def test_create_allows_anonymous_user_and_returns_201(
        self, api_client, user_account_list_url, general_user_data
    ):
        response = api_client.post(user_account_list_url, general_user_data)

        assert response.status_code == 201

    def test_create_saves_user_to_database(
        self, api_client, user_account_list_url, general_user_data
    ):
        before = UserAccount.objects.count()
        api_client.post(user_account_list_url, general_user_data)
        after = UserAccount.objects.count()

        assert after == before + 1

    def test_create_uses_correct_serializer(self):
        view = UserAccountViewSet()
        view.action = "create"

        assert view.get_serializer_class() is UserAccountCreateSerializer

    def test_create_response_fields_are_correct(
        self, api_client, user_account_list_url, general_user_data
    ):
        response = api_client.post(user_account_list_url, general_user_data)
        data = response.data

        expected_fields = {"id", "username", "email", "created_at"}
        assert set(data.keys()) == expected_fields

    # ========================================================================
    # Create Action - Negative Cases
    # ========================================================================
    def test_create_returns_400_for_invalid_request(
        self, api_client, user_account_list_url
    ):
        response = api_client.post(user_account_list_url, data={})
        assert response.status_code == 400

    @pytest.mark.parametrize("missing_field", ["username", "email", "password"])
    def test_create_fails_when_missing_required_fields(
        self, missing_field, api_client, user_account_list_url, general_user_data
    ):
        general_user_data.pop(missing_field)
        response = api_client.post(user_account_list_url, data=general_user_data)

        assert response.status_code == 400
        assert missing_field in response.data

    def test_create_fails_for_invalid_email_format(
        self, api_client, user_account_list_url, general_user_data
    ):
        general_user_data["email"] = "invalid_email_format"
        response = api_client.post(user_account_list_url, data=general_user_data)

        assert response.status_code == 400
        assert "email" in response.data

    @pytest.mark.parametrize("field", ["username", "email"])
    def test_create_fails_when_violating_unique_constraint(
        self,
        field,
        api_client,
        user_account_list_url,
        general_user_data,
        general_user_2,
    ):
        general_user_data[field] = getattr(general_user_2, field)
        response = api_client.post(user_account_list_url, data=general_user_data)

        assert response.status_code == 400
        assert field in response.data

    def test_create_does_not_save_user_to_database(
        self, api_client, user_account_list_url
    ):
        before = UserAccount.objects.count()
        api_client.post(user_account_list_url, data={})
        after = UserAccount.objects.count()

        assert before == after

    def test_create_fails_when_violating_username_validator(
        self, api_client, user_account_list_url, general_user_data
    ):
        general_user_data["username"] = "invalid username"
        response = api_client.post(user_account_list_url, data=general_user_data)

        assert response.status_code == 400
        assert "username" in response.data

    # ========================================================================
    # List Action - Positive Cases
    # ========================================================================
    def test_list_allows_anonymous_user_and_returns_200(
        self, api_client, user_account_list_url
    ):
        response = api_client.get(user_account_list_url)

        assert response.status_code == 200

    def test_list_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, user_account_list_url, general_user
    ):
        response = api_client.get(user_account_list_url)
        data = response.data["results"][0]

        expected_fields = {"id", "username", "created_at"}

        assert set(data.keys()) == expected_fields

    def test_list_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, user_account_list_url, admin_user, general_user
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(user_account_list_url)
        data = response.data["results"][0]

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

        assert set(data.keys()) == expected_fields

    def test_list_excludes_soft_deleted_user_for_public(
        self, api_client, user_account_list_url, users
    ):
        users[0].soft_delete()
        response = api_client.get(user_account_list_url)
        ids = [item["id"] for item in response.data["results"]]

        assert str(users[0].id) not in ids

    def test_list_includes_soft_deleted_user_for_admin(
        self, api_client, user_account_list_url, users, admin_user
    ):
        users[0].soft_delete()
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(user_account_list_url)
        ids = [item["id"] for item in response.data["results"]]

        assert str(users[0].id) in ids

    def test_list_results_returned_in_descending_order(
        self, api_client, user_account_list_url, users
    ):
        response = api_client.get(user_account_list_url)
        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    def test_list_filters_by_username_icontains(
        self, api_client, user_account_list_url, user_filter_data
    ):
        url = user_account_list_url + "?username=one"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["username"]

    def test_list_filters_by_created_at_date(
        self, api_client, user_account_list_url, user_filter_data
    ):
        target_created_at = str(user_filter_data[0].created_at.date())

        url = user_account_list_url + f"?created_at_date={target_created_at}"
        response = api_client.get(url)

        response_created_at = response.data["results"][0]["created_at"]
        response_created_at_date = response_created_at.split("T")[0]

        assert response.data["count"] == 1
        assert response_created_at_date == target_created_at

    def test_list_filters_by_created_at_year(
        self, api_client, user_account_list_url, user_filter_data
    ):
        url = user_account_list_url + "?created_at_year=2024"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            assert "2024" in item["created_at"]

    def test_list_filters_by_created_at_year_gte(
        self, api_client, user_account_list_url, user_filter_data
    ):
        url = user_account_list_url + "?created_at_year_gte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 3

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year >= 2023

    def test_list_filters_by_created_at_year_lte(
        self, api_client, user_account_list_url, user_filter_data
    ):
        url = user_account_list_url + "?created_at_year_lte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year <= 2023

    def test_list_searches_by_username(
        self, api_client, user_account_list_url, user_filter_data
    ):
        url = user_account_list_url + "?search=one"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["username"]

    def test_list_throttles_for_anonymous_user(
        self, api_client, user_account_list_url, users
    ):
        response_1 = api_client.get(user_account_list_url)
        response_2 = api_client.get(user_account_list_url)
        response_3 = api_client.get(user_account_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_throttles_for_general_user(
        self, api_client, user_account_list_url, users, general_user
    ):
        api_client.force_authenticate(user=general_user)

        response_1 = api_client.get(user_account_list_url)
        response_2 = api_client.get(user_account_list_url)
        response_3 = api_client.get(user_account_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_throttles_for_admin_user(
        self, api_client, user_account_list_url, users, admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        response_1 = api_client.get(user_account_list_url)
        response_2 = api_client.get(user_account_list_url)
        response_3 = api_client.get(user_account_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    # ========================================================================
    # Retrieve Action - Positive Cases
    # ========================================================================
    def test_retrieve_allows_anonymous_user_and_returns_200(
        self, api_client, user_account_detail_url, general_user
    ):
        url = user_account_detail_url(general_user.id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_can_get_soft_deleted_user_for_admin(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        general_user.soft_delete()
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, user_account_detail_url, general_user
    ):
        url = user_account_detail_url(general_user.id)
        response = api_client.get(url)

        expected_fields = {"id", "username", "created_at"}

        assert set(response.data.keys()) == expected_fields

    def test_retrieve_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        response = api_client.get(url)

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

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Retrieve Action - Negative Cases
    # ========================================================================
    def test_retrieve_returns_404_when_nonexistent_user(
        self, api_client, user_account_detail_url
    ):
        nonexistent_user_id = uuid4()
        url = user_account_detail_url(nonexistent_user_id)
        response = api_client.get(url)

        assert response.status_code == 404

    def test_retrieve_cannot_get_soft_deleted_user_for_public(
        self, api_client, user_account_detail_url, general_user
    ):
        general_user.soft_delete()
        url = user_account_detail_url(general_user.id)
        response = api_client.get(url)

        assert response.status_code == 404

    # ========================================================================
    # Patch Action - Positive Cases
    # ========================================================================
    def test_patch_allows_admin_user_and_returns_200(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        patch_data = {"username": "patch_username"}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field, value",
        [
            ("username", "patch_username"),
            ("email", "patch_email@example.com"),
            ("is_active", False),
        ],
    )
    def test_patch_only_allowed_fields_are_changed(
        self,
        field,
        value,
        api_client,
        user_account_detail_url,
        general_user,
        admin_user,
    ):
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        patch_data = {field: value}
        response = api_client.patch(url, data=patch_data)

        assert response.data[field] == value

    @pytest.mark.parametrize(
        "field, value",
        [
            ("id", uuid4()),
            ("is_superuser", True),
            ("is_staff", True),
            ("created_at", "2020-01-01"),
        ],
    )
    def test_patch_not_allowed_fields_are_unchanged(
        self,
        field,
        value,
        api_client,
        user_account_detail_url,
        general_user,
        admin_user,
    ):
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        patch_data = {field: value}

        original_value = getattr(general_user, field)
        api_client.patch(url, data=patch_data)

        general_user.refresh_from_db()

        assert getattr(general_user, field) == original_value

    def test_patch_can_get_soft_deleted_user_for_admin(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        general_user.soft_delete()
        patch_data = {"username": "patch_username"}
        url = user_account_detail_url(general_user.id)
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    def test_patch_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        patch_data = {"username": "patch_username"}
        url = user_account_detail_url(general_user.id)
        response = api_client.patch(url, data=patch_data)

        expected_fields = {
            "id",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
        }

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Patch Action - Negative Cases
    # ========================================================================
    def test_patch_returns_401_for_anonymous_user(
        self, api_client, user_account_detail_url, general_user
    ):
        url = user_account_detail_url(general_user.id)
        patch_data = {"username": "patch_username"}
        response = api_client.patch(url, patch_data=patch_data)

        assert response.status_code == 401

    def test_patch_returns_403_for_general_user(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=general_user)
        url = user_account_detail_url(admin_user.id)
        patch_data = {"username": "patch_username"}
        response = api_client.patch(url, patch_data=patch_data)

        assert response.status_code == 403

    def test_patch_returns_404_when_nonexistent_user(
        self, api_client, user_account_detail_url, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        nonexistent_user_id = uuid4()
        url = user_account_detail_url(nonexistent_user_id)
        patch_data = {"username": "patch_username"}
        response = api_client.patch(url, patch_data=patch_data)

        assert response.status_code == 404

    @pytest.mark.parametrize("field", ["username", "email"])
    def test_patch_fails_when_violating_unique_constraint(
        self,
        field,
        api_client,
        user_account_detail_url,
        general_user,
        admin_user,
        users,
    ):
        api_client.force_authenticate(user=admin_user)
        patch_data = {field: getattr(users[0], field)}
        url = user_account_detail_url(general_user.id)
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert field in response.data

    def test_patch_fails_for_invalid_email_format(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        patch_data = {"email": "invalid email format"}
        url = user_account_detail_url(general_user.id)
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert "email" in response.data

    def test_patch_fails_violating_username_validator(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        patch_data = {"username": "invalid username"}
        url = user_account_detail_url(general_user.id)
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 400
        assert "username" in response.data

    # ========================================================================
    # Delete Action - Positive Cases
    # ========================================================================
    def test_delete_returns_204_and_allows_superuser(
        self, api_client, user_account_detail_url, general_user, super_user
    ):
        api_client.force_authenticate(user=super_user)
        url = user_account_detail_url(general_user.id)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_sets_deleted_at_field(
        self, api_client, user_account_detail_url, general_user, super_user
    ):
        api_client.force_authenticate(user=super_user)
        url = user_account_detail_url(general_user.id)
        api_client.delete(url)

        general_user.refresh_from_db()

        assert general_user.deleted_at is not None

    # ========================================================================
    # Delete Action - Negative Cases
    # ========================================================================
    def test_delete_returns_401_for_anonymous_user(
        self, api_client, user_account_detail_url, general_user
    ):
        url = user_account_detail_url(general_user.id)
        response = api_client.delete(url)

        assert response.status_code == 401

    def test_delete_returns_403_for_general_user(
        self, api_client, user_account_detail_url, general_user, general_user_2
    ):
        api_client.force_authenticate(user=general_user)
        url = user_account_detail_url(general_user_2.id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_returns_403_for_admin_user(
        self, api_client, user_account_detail_url, general_user, admin_user
    ):
        api_client.force_authenticate(user=admin_user)
        url = user_account_detail_url(general_user.id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_returns_404_when_nonexistent_user(
        self, api_client, user_account_detail_url, super_user
    ):
        api_client.force_authenticate(user=super_user)
        nonexistent_user_id = uuid4()
        url = user_account_detail_url(nonexistent_user_id)
        response = api_client.delete(url)

        assert response.status_code == 404

    # ========================================================================
    # Comments Action - Positive Cases
    # ========================================================================
    def test_comments_returns_200_and_allows_anonymous_user(
        self, api_client, user_account_comments_url, general_user, comments
    ):
        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_comments_cannot_get_soft_deleted_comment_for_public(
        self, api_client, user_account_comments_url, general_user, comments
    ):
        target_comment = comments[0]
        target_comment.soft_delete()

        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)
        ids = [item["id"] for item in response.data["results"]]

        assert str(target_comment.id) not in ids

    def test_comments_can_get_soft_deleted_comment_for_admin(
        self, api_client, user_account_comments_url, general_user, admin_user, comments
    ):
        target_comment = comments[0]
        target_comment.soft_delete()

        api_client.force_authenticate(user=admin_user)
        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)
        ids = [item["id"] for item in response.data["results"]]

        assert str(target_comment.id) in ids

    def test_comments_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, user_account_comments_url, general_user, comments
    ):
        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)

        comment_data = response.data["results"][0]
        comment_expected_fields = {"id", "body", "created_at", "updated_at", "player"}

        assert set(comment_data.keys()) == comment_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_comments_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, user_account_comments_url, general_user, admin_user, comments
    ):
        target_comment = comments[0]
        target_comment.soft_delete()

        api_client.force_authenticate(user=admin_user)
        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)

        comment_data = response.data["results"][0]
        comment_expected_fields = {
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
        }

        assert set(comment_data.keys()) == comment_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_comments_results_returned_in_descending_order(
        self, api_client, user_account_comments_url, general_user
    ):
        url = user_account_comments_url(general_user.id)
        response = api_client.get(url)
        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    # ========================================================================
    # Comments Action - Negative Cases
    # ========================================================================
    def test_comments_returns_404_when_nonexistent_user(
        self, api_client, user_account_comments_url
    ):
        nonexistent_user_id = uuid4()
        url = user_account_comments_url(nonexistent_user_id)
        response = api_client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestMeAPIView(TestBase):
    # ========================================================================
    # Retrieve Action - Positive Cases
    # ========================================================================
    def test_retrieve_returns_200_and_allows_authenticated_user(
        self, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_url)

        assert response.status_code == 200

    def test_retrieve_get_object_returns_request_user_object(
        self, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_url)

        assert response.data["id"] == str(general_user.id)

    def test_uses_correct_serializer_and_returns_correct_response(
        self, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_url)

        expected_fields = {"id", "username", "email", "created_at", "updated_at"}

        assert set(response.data.keys()) == expected_fields

    def test_retrieve_throttles_for_general_user(
        self, api_client, me_url, users, general_user
    ):
        api_client.force_authenticate(user=general_user)

        response_1 = api_client.get(me_url)
        response_2 = api_client.get(me_url)
        response_3 = api_client.get(me_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_retrieve_throttles_for_admin_user(
        self, api_client, me_url, users, admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        response_1 = api_client.get(me_url)
        response_2 = api_client.get(me_url)
        response_3 = api_client.get(me_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    # ========================================================================
    # Retrieve Action - Negative Cases
    # ========================================================================
    def test_returns_401_for_anonymous_user(self, api_client, me_url):
        response = api_client.get(me_url)

        assert response.status_code == 401

    # ========================================================================
    # Patch Action - Positive Cases
    # ========================================================================
    @pytest.mark.parametrize(
        "field, value",
        [("username", "patch_username"), ("email", "patch_email@example.com")],
    )
    def test_patch_returns_200_and_allows_authenticated_user(
        self, field, value, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        patch_data = {field: value}
        response = api_client.patch(me_url, data=patch_data)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field, value",
        [("username", "patch_username"), ("email", "patch_email@example.com")],
    )
    def test_patch_get_object_returns_request_user_object(
        self, field, value, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        patch_data = {field: value}
        response = api_client.patch(me_url, data=patch_data)

        assert response.data["id"] == str(general_user.id)

    @pytest.mark.parametrize(
        "field, value",
        [("username", "patch_username"), ("email", "patch_email@example.com")],
    )
    def test_patch_allowed_fields_are_updated(
        self, field, value, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        patch_data = {field: value}
        response = api_client.patch(me_url, data=patch_data)

        assert response.data[field] == value

    @pytest.mark.parametrize(
        "field, value",
        [("id", uuid4()), ("created_at", "20251111")],
    )
    def test_patch_not_allowed_fields_are_unchanged(
        self, field, value, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)

        original_value = getattr(general_user, field)

        patch_data = {field: value}
        api_client.patch(me_url, data=patch_data)

        general_user.refresh_from_db()

        assert getattr(general_user, field) == original_value

    @pytest.mark.parametrize(
        "field, value",
        [("username", "patch_username"), ("email", "patch_email@example.com")],
    )
    def test_patch_uses_correct_serializer_and_returns_correct_response(
        self, field, value, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        patch_data = {field: value}
        response = api_client.patch(me_url, data=patch_data)

        expected_fields = {"id", "username", "email", "created_at", "updated_at"}

        assert set(response.data.keys()) == expected_fields

    # ========================================================================
    # Patch Action - Negative Cases
    # ========================================================================
    def test_patch_returns_401_for_anonymous_user(self, api_client, me_url):
        response = api_client.patch(me_url)

        assert response.status_code == 401

    @pytest.mark.parametrize("field", ["username", "email"])
    def test_patch_fails_when_violating_unique_constraint(
        self, field, api_client, me_url, general_user, users
    ):
        user = users[0]

        api_client.force_authenticate(user=general_user)
        patch_data = {field: getattr(user, field)}
        response = api_client.patch(me_url, data=patch_data)

        assert response.status_code == 400
        assert field in response.data

    def test_patch_fails_for_invalid_email_format(
        self, api_client, me_url, general_user
    ):
        invalid_email_format = "invalid email format"

        api_client.force_authenticate(user=general_user)
        patch_data = {"email": invalid_email_format}
        response = api_client.patch(me_url, data=patch_data)

        assert response.status_code == 400
        assert "email" in response.data

    def test_patch_fails_when_violating_username_validator(
        self, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        patch_data = {"username": "invalid username"}
        response = api_client.patch(me_url, data=patch_data)

        assert response.status_code == 400
        assert "username" in response.data

    # ========================================================================
    # Delete Action - Positive Cases
    # ========================================================================
    def test_delete_returns_204_and_allows_authenticated_user(
        self, api_client, me_url, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.delete(me_url)

        assert response.status_code == 204

    def test_delete_sets_deleted_at_field(self, api_client, me_url, general_user):
        api_client.force_authenticate(user=general_user)
        api_client.delete(me_url)

        general_user.refresh_from_db()

        assert general_user.deleted_at is not None

    # ========================================================================
    # Destroy Action - Negative Cases
    # ========================================================================
    def test_delete_returns_401_fro_anonymous_user(self, api_client, me_url):
        response = api_client.delete(me_url)

        assert response.status_code == 401


@pytest.mark.django_db
class TestMeCommentAPIView(TestBase):
    # ========================================================================
    # List Action - Positive Cases
    # ========================================================================
    def test_list_returns_200_and_allows_authenticated_user(
        self, api_client, me_comments_url, general_user, comments
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_comments_url)

        assert response.status_code == 200

    def test_list_excludes_soft_deleted_comment(
        self, api_client, me_comments_url, general_user, comments
    ):
        comments[0].soft_delete()
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_comments_url)
        ids = [item["id"] for item in response.data["results"]]

        assert str(comments[0].id) not in ids

    def test_list_uses_correct_serializer_and_returns_correct_response(
        self, api_client, me_comments_url, general_user, comments
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_comments_url)
        comment_data = response.data["results"][0]
        nested_player_data = comment_data["player"]
        nested_team_data = nested_player_data["team"]

        comment_expected_fields = {"id", "body", "created_at", "updated_at", "player"}
        assert set(comment_data.keys()) == comment_expected_fields

        player_expected_fields = {"id", "first_name", "last_name", "team"}
        assert set(nested_player_data.keys()) == player_expected_fields

        team_expected_fields = {"id", "name"}
        assert set(nested_team_data.keys()) == team_expected_fields

    def test_list_results_returned_in_descending_order(
        self, api_client, me_comments_url, general_user, comments
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.get(me_comments_url)
        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    def test_list_team_name_icontains(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?team_name=2"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "2" in item["player"]["team"]["name"]

    def test_list_player_first_name_icontains(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?player_first_name=one"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["player"]["first_name"].lower()

    def test_list_player_last_name_icontains(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?player_last_name=one"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["player"]["last_name"].lower()

    def test_list_filters_by_created_at_date(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        target_created_at = str(me_comment_filter_data[0].created_at.date())

        url = me_comments_url + f"?created_at_date={target_created_at}"
        response = api_client.get(url)

        response_created_at = response.data["results"][0]["created_at"]
        response_created_at_date = response_created_at.split("T")[0]

        assert response.data["count"] == 1
        assert response_created_at_date == target_created_at

    def test_list_filters_by_created_at_year(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?created_at_year=2024"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            assert "2024" in item["created_at"]

    def test_list_filters_by_created_at_year_gte(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?created_at_year_gte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 3

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year >= 2023

    def test_list_filters_by_created_at_year_lte(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?created_at_year_lte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year <= 2023

    def test_list_searches_by_body(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?search=example"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "examples" in item["body"]

    def test_list_searches_by_player_first_name(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?search=hello"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "hello" in item["player"]["first_name"].lower()

    def test_list_searches_by_player_last_name(
        self, api_client, me_comments_url, general_user, me_comment_filter_data
    ):
        api_client.force_authenticate(user=general_user)

        url = me_comments_url + "?search=bye"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "bye" in item["player"]["last_name"].lower()

    def test_list_throttles_for_general_user(
        self, api_client, me_url, users, general_user
    ):
        api_client.force_authenticate(user=general_user)

        response_1 = api_client.get(me_url)
        response_2 = api_client.get(me_url)
        response_3 = api_client.get(me_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_throttles_for_admin_user(self, api_client, me_url, users, admin_user):
        api_client.force_authenticate(user=admin_user)

        response_1 = api_client.get(me_url)
        response_2 = api_client.get(me_url)
        response_3 = api_client.get(me_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    # ========================================================================
    # List Action - Negative Cases
    # ========================================================================
    def test_list_returns_401_for_anonymous_user(self, api_client, me_comments_url):
        response = api_client.get(me_comments_url)

        assert response.status_code == 401
