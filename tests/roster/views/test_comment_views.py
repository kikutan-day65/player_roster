from uuid import uuid4

import pytest
from django.utils.dateparse import parse_datetime

from core.tests.test_base import TestBase
from roster.models import Comment


@pytest.mark.django_db
class TestCommentViewSet(TestBase):
    # ========================================================================
    # Create Action - Positive Cases
    # ========================================================================
    def test_create_returns_201_and_allows_authenticate_user(
        self, api_client, comment_list_url, comment_data_from_view, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.post(comment_list_url, data=comment_data_from_view)

        assert response.status_code == 201

    def test_create_saves_comment_to_database(
        self, api_client, comment_list_url, comment_data_from_view, general_user
    ):
        api_client.force_authenticate(user=general_user)
        before = Comment.objects.count()
        api_client.post(comment_list_url, data=comment_data_from_view)
        after = Comment.objects.count()

        assert after == before + 1

    def test_create_uses_correct_serializer_and_returns_correct_response(
        self, api_client, comment_list_url, comment_data_from_view, general_user
    ):
        api_client.force_authenticate(user=general_user)
        response = api_client.post(comment_list_url, data=comment_data_from_view)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "player"}

        assert set(comment_data.keys()) == expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    # ========================================================================
    # Create Action - Negative Cases
    # ========================================================================
    def test_create_returns_401_for_anonymous_user(
        self, api_client, comment_list_url, comment_data_from_view
    ):
        response = api_client.post(comment_list_url, data=comment_data_from_view)

        assert response.status_code == 401

    @pytest.mark.parametrize("field", ["body", "player_id"])
    def test_create_fails_without_required_fields(
        self, field, api_client, comment_list_url, comment_data_from_view, general_user
    ):
        comment_data_from_view.pop(field)
        api_client.force_authenticate(user=general_user)
        response = api_client.post(comment_list_url, data=comment_data_from_view)

        assert response.status_code == 400
        assert field in response.data

    def test_create_fails_due_to_nonexistent_player_id(
        self, api_client, comment_list_url, comment_data_from_view, general_user
    ):
        nonexistent_player_id = uuid4()
        comment_data_from_view["player_id"] = nonexistent_player_id

        api_client.force_authenticate(user=general_user)
        response = api_client.post(comment_list_url, data=comment_data_from_view)

        assert response.status_code == 400
        assert "player_id" in response.data

    # ========================================================================
    # List Action - Positive Cases
    # ========================================================================
    def test_list_returns_200_and_allows_anonymous_user(
        self, api_client, comment_list_url
    ):
        response = api_client.get(comment_list_url)

        assert response.status_code == 200

    def test_list_includes_soft_deleted_comment_for_admin(
        self, api_client, comment_list_url, admin_user, comments
    ):
        comment = comments[0]
        comment.soft_delete()
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(comment_list_url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(comment.id) in ids

    def test_list_excludes_soft_deleted_comment_for_public(
        self, api_client, comment_list_url, comments
    ):
        comment = comments[0]
        comment.soft_delete()
        response = api_client.get(comment_list_url)

        ids = [item["id"] for item in response.data["results"]]

        assert str(comment.id) not in ids

    def test_list_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, comment_list_url, comments
    ):
        response = api_client.get(comment_list_url)

        comment_data = response.data["results"][0]
        expected_fields = {"id", "body", "created_at", "updated_at", "player", "user"}

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_list_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, comment_list_url, admin_user, comments
    ):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(comment_list_url)

        comment_data = response.data["results"][0]
        expected_fields = {
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
            "user",
        }

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_list_returns_in_descending_order_of_created_at(
        self, api_client, comment_list_url, comments
    ):
        response = api_client.get(comment_list_url)

        response_created_at = [item["created_at"] for item in response.data["results"]]
        descending_order = sorted(response_created_at, reverse=True)

        assert response_created_at == descending_order

    def test_list_filters_by_user_username_icontains(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?user_username=2"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            assert "2" in item["user"]["username"]

    def test_list_filters_by_player_first_name(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?player_first_name=one"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["player"]["first_name"].lower()

    def test_list_filters_by_player_last_name(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?player_last_name=one"
        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "one" in item["player"]["last_name"].lower()

    def test_list_filters_by_created_at_date(
        self, api_client, comment_list_url, comment_filter_data
    ):
        target_created_at = str(comment_filter_data[0].created_at.date())

        url = comment_list_url + f"?created_at_date={target_created_at}"
        response = api_client.get(url)

        response_created_at = response.data["results"][0]["created_at"]
        response_created_at_date = response_created_at.split("T")[0]

        assert response.data["count"] == 1
        assert response_created_at_date == target_created_at

    def test_list_filters_by_created_at_year(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?created_at_year=2024"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            assert "2024" in item["created_at"]

    def test_list_filters_by_created_at_year_gte(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?created_at_year_gte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 3

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year >= 2023

    def test_list_filters_by_created_at_year_lte(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?created_at_year_lte=2023"
        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            year = int(item["created_at"][:4])
            assert year <= 2023

    def test_list_searches_by_body(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?search=example"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "example" in item["body"].lower()

    def test_list_searches_by_user_username(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?search=2"

        response = api_client.get(url)

        assert response.data["count"] == 2

        for item in response.data["results"]:
            assert "2" in item["user"]["username"]

    def test_list_searches_by_player_first_name(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?search=hello"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "hello" in item["player"]["first_name"].lower()

    def test_list_searches_by_player_last_name(
        self, api_client, comment_list_url, comment_filter_data
    ):
        url = comment_list_url + "?search=bye"

        response = api_client.get(url)

        assert response.data["count"] == 1

        for item in response.data["results"]:
            assert "bye" in item["player"]["last_name"].lower()

    def test_list_throttles_for_anonymous_user(
        self, api_client, comment_list_url, comments
    ):
        response_1 = api_client.get(comment_list_url)
        response_2 = api_client.get(comment_list_url)
        response_3 = api_client.get(comment_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_throttles_for_general_user(
        self, api_client, comment_list_url, comments, general_user
    ):
        api_client.force_authenticate(user=general_user)

        response_1 = api_client.get(comment_list_url)
        response_2 = api_client.get(comment_list_url)
        response_3 = api_client.get(comment_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_throttles_for_admin_user(
        self, api_client, comment_list_url, comments, admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        response_1 = api_client.get(comment_list_url)
        response_2 = api_client.get(comment_list_url)
        response_3 = api_client.get(comment_list_url)

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 429

    def test_list_filters_ascending_order_of_user_username_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=user__username"
        response = api_client.get(url)

        usernames = [item["user"]["username"] for item in response.data["results"]]

        ascending = sorted(
            [comment.user.username for comment in comment_ordering_filter_data]
        )

        assert usernames == ascending

    def test_list_filters_descending_order_of_user_username_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=-user__username"
        response = api_client.get(url)

        usernames = [item["user"]["username"] for item in response.data["results"]]

        descending = sorted(
            [comment.user.username for comment in comment_ordering_filter_data],
            reverse=True,
        )

        assert usernames == descending

    def test_list_filters_ascending_order_of_player_first_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=player__first_name"
        response = api_client.get(url)

        first_names = [
            item["player"]["first_name"] for item in response.data["results"]
        ]

        ascending = sorted(
            [comment.player.first_name for comment in comment_ordering_filter_data]
        )

        assert first_names == ascending

    def test_list_filters_descending_order_of_player_first_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=-player__first_name"
        response = api_client.get(url)

        first_names = [
            item["player"]["first_name"] for item in response.data["results"]
        ]

        descending = sorted(
            [comment.player.first_name for comment in comment_ordering_filter_data],
            reverse=True,
        )

        assert first_names == descending

    def test_list_filters_ascending_order_of_player_last_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=player__last_name"
        response = api_client.get(url)

        last_names = [item["player"]["last_name"] for item in response.data["results"]]

        ascending = sorted(
            [comment.player.last_name for comment in comment_ordering_filter_data]
        )

        assert last_names == ascending

    def test_list_filters_descending_order_of_player_last_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=-player__last_name"
        response = api_client.get(url)

        last_names = [item["player"]["last_name"] for item in response.data["results"]]

        descending = sorted(
            [comment.player.last_name for comment in comment_ordering_filter_data],
            reverse=True,
        )

        assert last_names == descending

    def test_list_filters_ascending_order_of_player_team_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=player__team__name"
        response = api_client.get(url)

        team_names = [
            item["player"]["team"]["name"] for item in response.data["results"]
        ]

        ascending = sorted(
            [comment.player.team.name for comment in comment_ordering_filter_data]
        )

        assert team_names == ascending

    def test_list_filters_descending_order_of_player_team_name_field(
        self,
        api_client,
        comment_list_url,
        comment_ordering_filter_data,
    ):
        url = comment_list_url + "?ordering=-player__team__name"
        response = api_client.get(url)

        team_names = [
            item["player"]["team"]["name"] for item in response.data["results"]
        ]

        descending = sorted(
            [comment.player.team.name for comment in comment_ordering_filter_data],
            reverse=True,
        )

        assert team_names == descending

    def test_list_filters_ascending_order_of_created_at_field(
        self, api_client, comment_list_url, comment_ordering_filter_data
    ):
        url = comment_list_url + "?ordering=created_at"
        response = api_client.get(url)

        created_at_data = [
            parse_datetime(item["created_at"]) for item in response.data["results"]
        ]

        ascending = sorted(
            [comment.created_at for comment in comment_ordering_filter_data]
        )

        assert created_at_data == ascending

    def test_list_filters_descending_order_of_created_at_field(
        self, api_client, comment_list_url, comment_ordering_filter_data
    ):
        url = comment_list_url + "?ordering=-created_at"
        response = api_client.get(url)

        created_at_data = [
            parse_datetime(item["created_at"]) for item in response.data["results"]
        ]

        descending = sorted(
            [comment.created_at for comment in comment_ordering_filter_data],
            reverse=True,
        )

        assert created_at_data == descending

    # ========================================================================
    # Retrieve Action - Positive Cases
    # ========================================================================
    def test_retrieve_returns_200_and_allows_anonymous_user(
        self, api_client, comment_detail_url, comments
    ):
        comment_id = comments[0].id
        url = comment_detail_url(comment_id)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_retrieve_can_get_soft_deleted_comment_for_admin(
        self, api_client, comment_detail_url, admin_user, comments
    ):
        comment = comments[0]
        comment.soft_delete()
        comment_id = comment.id

        url = comment_detail_url(comment_id)
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(url)

        assert str(comment.id) == response.data["id"]

    def test_retrieve_excludes_soft_deleted_comment_for_public(
        self,
        api_client,
        comment_detail_url,
        comments,
    ):
        comment = comments[0]
        comment.soft_delete()
        comment_id = comment.id

        url = comment_detail_url(comment_id)
        response = api_client.get(url)

        assert response.status_code == 404

    def test_retrieve_uses_correct_serializer_and_returns_correct_response_for_public(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        url = comment_detail_url(comment_id)
        response = api_client.get(url)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "updated_at", "player", "user"}

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_retrieve_uses_correct_serializer_and_returns_correct_response_for_admin(
        self, api_client, comment_detail_url, admin_user, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        response = api_client.get(url)

        comment_data = response.data
        expected_fields = {
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
            "user",
        }

        assert set(comment_data.keys()) == expected_fields

        user_data = comment_data["user"]
        user_expected_fields = {"id", "username"}

        assert set(user_data.keys()) == user_expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    # ========================================================================
    # Retrieve Action - Negative Cases
    # ========================================================================
    def test_retrieve_returns_404_for_nonexistent_comment(
        self, api_client, comment_detail_url
    ):
        nonexistent_comment_id = uuid4()

        url = comment_detail_url(nonexistent_comment_id)
        response = api_client.get(url)

        assert response.status_code == 404

    # ========================================================================
    # Patch Action - Positive Cases
    # ========================================================================
    def test_patch_returns_200_and_allows_admin_user(
        self, api_client, comment_detail_url, comments, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 200

    def test_patch_returns_200_and_allows_owner(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id
        owner = comment.user

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 200

    def test_patch_can_patch_soft_deleted_comment_with_body_for_admin(
        self, api_client, comment_detail_url, comments, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id
        comment.soft_delete()

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        patch_data = {"body": "Patch Comment Body"}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200

    def test_patch_can_patch_soft_deleted_comment_with_player_id_for_admin(
        self, api_client, comment_detail_url, comments, players, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id
        comment.soft_delete()

        player_id = players[1].id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        patch_data = {"player_id": player_id}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 200
        assert str(player_id) == response.data["player"]["id"]

    def test_patch_cannot_patch_soft_deleted_comment_with_body_for_owner(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id
        comment.soft_delete()

        owner = comment.user

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        patch_data = {"body": "Patch Comment Body"}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 404

    def test_patch_cannot_patch_soft_deleted_comment_with_player_id_for_owner(
        self, api_client, comment_detail_url, comments, players
    ):
        comment = comments[0]
        comment_id = comment.id
        comment.soft_delete()

        owner = comment.user

        player_id = players[1].id

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        patch_data = {"player_id": player_id}
        response = api_client.patch(url, data=patch_data)

        assert response.status_code == 404

    def test_patch_uses_correct_serializer_and_returns_correct_response_with_body_for_admin(
        self, api_client, comment_detail_url, comments, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        patch_data = {"body": "Patch Comment Body"}
        response = api_client.patch(url, data=patch_data)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "updated_at", "player"}

        assert set(comment_data.keys()) == expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_patch_uses_correct_serializer_and_returns_correct_response_with_player_id_for_admin(
        self, api_client, comment_detail_url, comments, players, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id

        player_id = players[1].id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        patch_data = {"player_id": player_id}
        response = api_client.patch(url, data=patch_data)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "updated_at", "player"}

        assert set(comment_data.keys()) == expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_patch_uses_correct_serializer_and_returns_correct_response_with_body_for_owner(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        owner = comment.user

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        patch_data = {"body": "Patch Comment Body"}
        response = api_client.patch(url, data=patch_data)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "updated_at", "player"}

        assert set(comment_data.keys()) == expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    def test_patch_uses_correct_serializer_and_returns_correct_response_with_player_id_for_owner(
        self, api_client, comment_detail_url, comments, players
    ):
        comment = comments[0]
        comment_id = comment.id

        owner = comment.user

        player_id = players[1].id

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        patch_data = {"player_id": player_id}
        response = api_client.patch(url, data=patch_data)

        comment_data = response.data
        expected_fields = {"id", "body", "created_at", "updated_at", "player"}

        assert set(comment_data.keys()) == expected_fields

        player_data = comment_data["player"]
        player_expected_fields = {"id", "first_name", "last_name", "team"}

        assert set(player_data.keys()) == player_expected_fields

        team_data = player_data["team"]
        team_expected_fields = {"id", "name"}

        assert set(team_data.keys()) == team_expected_fields

    # ========================================================================
    # Patch Action - Negative Cases
    # ========================================================================
    def test_patch_returns_401_for_anonymous_user(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        url = comment_detail_url(comment_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 401

    def test_patch_returns_403_for_general_user_not_owner(
        self, api_client, comment_detail_url, comments, general_user_2
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=general_user_2)
        url = comment_detail_url(comment_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 403

    def test_patch_fails_for_nonexistent_comment(
        self, api_client, comment_detail_url, admin_user
    ):
        comment_id = uuid4()

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        response = api_client.patch(url, data={})

        assert response.status_code == 404

    # ========================================================================
    # Destroy Action - Positive Cases
    # ========================================================================
    def test_delete_returns_204_and_allows_super_user(
        self, api_client, comment_detail_url, comments, super_user
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=super_user)
        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_returns_204_and_allows_owner(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id
        owner = comment.user

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_sets_deleted_at_field_for_super_user(
        self, api_client, comment_detail_url, comments, super_user
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=super_user)
        url = comment_detail_url(comment_id)
        api_client.delete(url)

        comment.refresh_from_db()

        assert comment.deleted_at is not None

    def test_delete_sets_deleted_at_field_for_owner(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        owner = comment.user

        api_client.force_authenticate(user=owner)
        url = comment_detail_url(comment_id)
        api_client.delete(url)

        comment.refresh_from_db()

        assert comment.deleted_at is not None

    # ========================================================================
    # Destroy Action - Negative Cases
    # ========================================================================
    def test_delete_returns_401_for_anonymous_user(
        self, api_client, comment_detail_url, comments
    ):
        comment = comments[0]
        comment_id = comment.id

        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 401

    def test_delete_returns_403_for_general_user_not_owner(
        self, api_client, comment_detail_url, comments, general_user_2
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=general_user_2)
        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_returns_403_for_admin_user(
        self, api_client, comment_detail_url, comments, admin_user
    ):
        comment = comments[0]
        comment_id = comment.id

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 403

    def test_delete_fails_for_nonexistent_comment(
        self, api_client, comment_detail_url, admin_user
    ):
        comment_id = uuid4()

        api_client.force_authenticate(user=admin_user)
        url = comment_detail_url(comment_id)
        response = api_client.delete(url)

        assert response.status_code == 404
