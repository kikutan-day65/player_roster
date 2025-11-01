from rest_framework import serializers

from roster.models import Player, Team
from user_account.models import UserAccount


class TeamNestedSerializer(serializers.ModelSerializer):
    """
    {
        "id": "yyy-yyy-yyy",
        "name": "Team Name"
    }
    """

    class Meta:
        model = Team
        fields = ["id", "name"]


class PlayerNestedSerializer(serializers.ModelSerializer):
    """
    {
        "id": "xxx-xxx-xxx",
        "first_name": "FirstName",
        "last_name": "LastName",
        "team": {
            "id": "yyy-yyy-yyy",
            "name": "Team Name"
        }
    }
    """

    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name", "team"]


class UserAccountNestedSerializer(serializers.ModelSerializer):
    """
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name"
    }
    """

    class Meta:
        model = UserAccount
        fields = ["id", "username"]
