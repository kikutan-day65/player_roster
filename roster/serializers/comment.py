from rest_framework import serializers

from core.nested_serializers import PlayerNestedSerializer, UserAccountNestedSerializer
from roster.models import Comment, Player
from user_account.models import UserAccount


# ==================================================
# Comment
# ==================================================
class CommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",  # field name (FK) on Comment model
        queryset=UserAccount.objects.all(),
        write_only=True,
    )

    player_id = serializers.PrimaryKeyRelatedField(
        source="player",  # field name (FK) on Comment model
        queryset=Player.objects.all(),
        write_only=True,
    )

    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "player", "user_id", "player_id"]
        read_only_fields = ["id", "created_at", "player"]


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
        read_only_fields = ["id", "created_at", "updated_at", "player"]
