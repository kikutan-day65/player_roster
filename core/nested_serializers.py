from rest_framework import serializers

from roster.models import Comment, Player, Team
from user_account.models import UserAccount


class TeamNestedSerializer(serializers.ModelSerializer):
    """
    {
        "id": "zzz-zzz-zzz",
        "name": "Sample Team"
    }
    """

    class Meta:
        model = Team
        fields = ["id", "name"]


class PlayerNestedSerializer(serializers.ModelSerializer):
    """
    {
        "id": "lll-mmm-nnn",
        "first_name": "Player_first_name",
        "last_name": "Player_last_name",
        "team" : {
            "id": "zzz-zzz-zzz",
            "name": "Sample Team"
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
        "id": "xxx-xxx-xxx",
        "username": "john_doe"
    }
    """

    class Meta:
        model = UserAccount
        fields = ["id", "username"]


class CommentNestedForUserAccountSerializer(serializers.ModelSerializer):
    """
    {
        "id": "yyy-yyy-yyy",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "player": {
            "id": "lll-mmm-nnn",
            "first_name": "Player_first_name",
            "last_name": "Player_last_name",
            "team" : {
                "id": "zzz-zzz-zzz",
                "name": "Sample Team"
            }
        }
    }
    """

    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "player"]


class CommentNestedForPlayerSerializer(serializers.ModelSerializer):
    """
    {
        "id": "yyy-yyy-yyy",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "user": {
            "id": "aaa-aaa-aaa",
            "username": "john_doe"
        }
    }
    """

    user = UserAccountNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "user"]
