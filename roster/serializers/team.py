from rest_framework import serializers

from roster.models import Team


class TeamPublicSerializer(serializers.ModelSerializer):
    """
    {
        "id": "uuid-wwww-vvvv",
        "name": "Yokohama DeNA Baystars",
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
        "name": "Yokohama DeNA Baystars",
        "sport": "baseball"
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    """

    class Meta:
        model = Team
        fields = "__all__"
