from rest_framework import serializers

from roster.models import Team


class TeamPublicSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-wwww-vvvv",
        "name": "Sample Team",
        "sport": "baseball"
    }
    """

    class Meta:
        model = Team
        fields = ["id", "name", "sport"]


class TeamAdminSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-wwww-vvvv",
        "name": "Sample Team",
        "sport": "baseball"
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    """

    class Meta:
        model = Team
        fields = ["id", "name", "sport", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
