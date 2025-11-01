from rest_framework import serializers

from core.nested_serializers import PlayerNestedSerializer, UserAccountNestedSerializer
from roster.models import Comment, Player


class CommentCreateSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(
        source="player",  # field name (FK) on Comment model
        queryset=Player.objects.all(),
        write_only=True,
    )

    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "player", "player_id"]
        read_only_fields = ["id", "created_at"]


class CommentListRetrievePublicSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)
    user = UserAccountNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "player", "user"]
        read_only_fields = ["id", "body", "created_at", "updated_at", "player", "user"]


class CommentListRetrieveAdminSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)
    user = UserAccountNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
            "user",
        ]
        read_only_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
            "user",
        ]


class CommentPatchSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(
        source="player",  # field name (FK) on Comment model
        queryset=Player.objects.all(),
        write_only=True,
    )

    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "player", "player_id"]
        read_only_fields = ["id", "created_at", "updated_at"]
