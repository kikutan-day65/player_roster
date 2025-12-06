from rest_framework import serializers

from core.nested_serializers import TeamNestedSerializer, UserAccountNestedSerializer
from roster.models import Comment, Player, Team


# ==================================================
# Player
# ==================================================
class PlayerCreateSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        source="team",  # field name (FK) on Player model
        queryset=Team.objects.all(),
        write_only=True,
    )

    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name", "created_at", "team", "team_id"]
        read_only_fields = ["id", "created_at", "team"]


class PlayerListRetrievePublicSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name", "created_at", "team"]
        read_only_fields = ["id", "first_name", "last_name", "created_at", "team"]


class PlayerListRetrieveAdminSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team",
        ]
        read_only_fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
            "team",
        ]


class PlayerPatchSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        source="team",  # field name (FK) on Player model
        queryset=Team.objects.all(),
        write_only=True,
    )

    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "team",
            "team_id",
        ]
        read_only_fields = read_only_fields = ["id", "created_at", "updated_at", "team"]


# ==================================================
# PlayerComment
# ==================================================
class PlayerCommentListPublicSerializer(serializers.ModelSerializer):
    user = UserAccountNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "user"]
        read_only_fields = ["id", "body", "created_at", "updated_at", "user"]


class PlayerCommentListAdminSerializer(serializers.ModelSerializer):
    user = UserAccountNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "deleted_at", "user"]
        read_only_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "user",
        ]
