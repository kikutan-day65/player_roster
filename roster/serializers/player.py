from rest_framework import serializers

from core.nested_serializers import (
    CommentNestedForPlayerSerializer,
    TeamNestedSerializer,
)
from roster.models import Player, Team


class PlayerPublicSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-xxxx-yyyy",
        "first_name": "John",
        "last_name": "Doe",
        "comments": [
            {
                "id": "yyy-yyy-yyy",
                "body": "Comment Body...",
                "created_at": "YYYY-MM-DD",
                "user": {
                    "id": "aaa-aaa-aaa",
                    "username": "john_doe"
                }
            }
        ],
        "team": {
            "id": "uuid-wwww-vvvv",
            "name": "Sample Team"
        }
    }
    """

    team = TeamNestedSerializer(read_only=True)
    comments = CommentNestedForPlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Player
        fields = ["id", "team", "first_name", "last_name", "comments", "team"]


class PlayerAdminSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-xxxx-yyyy",
        "first_name": "John",
        "last_name": "Doe"
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD",
        "comments": [
            {
                "id": "yyy-yyy-yyy",
                "body": "Comment Body...",
                "created_at": "YYYY-MM-DD",
                "user": {
                    "id": "aaa-aaa-aaa",
                    "username": "john_doe"
                }
            }
        ],
        "team": {
            "id": "uuid-wwww-vvvv",
            "name": "Sample Team"
        }
    }
    """

    team_id = serializers.PrimaryKeyRelatedField(
        source="team", queryset=Team.objects.all(), write_only=True
    )

    team = TeamNestedSerializer(read_only=True)
    comments = CommentNestedForPlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "comments",
            "team",
            "team_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at", "comments"]
