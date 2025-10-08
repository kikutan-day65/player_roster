from rest_framework import serializers

from roster.models import Player, Team
from roster.serializers.team import TeamAdminSerializer, TeamPublicSerializer


class PlayerPublicSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-xxxx-yyyy",
        "team": {
            "id": "uuid-wwww-vvvv",
            "name": "Yokohama DeNA Baystars",
            "sport": "baseball"
        },
        "first_name": "John",
        "last_name": "Doe"
    }
    """

    team = TeamPublicSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "team", "first_name", "last_name"]


class PlayerAdminSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-xxxx-yyyy",
        "team": {
            "id": "uuid-wwww-vvvv",
            "name": "Yokohama DeNA Baystars",
            "sport": "baseball",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD"
        },
        "first_name": "John",
        "last_name": "Doe"
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    """

    team_id = serializers.PrimaryKeyRelatedField(
        source="team", queryset=Team.objects.all(), write_only=True
    )

    team = TeamAdminSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "team",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
