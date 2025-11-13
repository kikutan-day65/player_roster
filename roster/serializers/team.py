from rest_framework import serializers

from roster.models import Player, Team


# ==================================================
# Team
# ==================================================
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "sport", "created_at"]
        read_only_fields = ["id", "created_at"]


class TeamListRetrievePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "sport"]
        read_only_fields = ["id", "name", "sport"]


class TeamListRetrieveAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "sport", "created_at", "updated_at", "deleted_at"]
        read_only_fields = [
            "id",
            "name",
            "sport",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TeamPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "sport", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================================================
# TeamPlayer
# ==================================================
class TeamPlayerListPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["id", "first_name", "last_name"]


class TeamPlayerListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
