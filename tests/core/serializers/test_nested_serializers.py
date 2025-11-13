import pytest

from core.nested_serializers import (
    PlayerNestedSerializer,
    TeamNestedSerializer,
    UserAccountNestedSerializer,
)
from core.tests.test_base import TestBase


@pytest.mark.django_db
class TestTeamNestedSerializer(TestBase):
    def test_success_to_serialize_team_instance(self, teams):
        team = teams[0]
        serializer = TeamNestedSerializer(team)
        output = serializer.data

        expected_fields = ["id", "name"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["sport", "created_at", "updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestPlayerNestedSerializer(TestBase):
    def test_success_to_serialize_player_instance(self, players):
        player = players[0]
        serializer = PlayerNestedSerializer(player)
        output = serializer.data

        expected_fields = ["id", "first_name", "last_name", "team"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = ["created_at", "updated_at", "deleted_at"]
        self.assert_unexpected_fields(output, unexpected_fields)


@pytest.mark.django_db
class TestUserAccountNestedSerializer(TestBase):
    def test_success_to_serialize_user_instance(self, general_user):
        serializer = UserAccountNestedSerializer(general_user)
        output = serializer.data

        expected_fields = ["id", "username"]
        self.assert_expected_fields(output, expected_fields)

        unexpected_fields = [
            "password",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        self.assert_unexpected_fields(output, unexpected_fields)
