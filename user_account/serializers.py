from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from roster.serializers.comment import CommentNestedSerializer

from .models import UserAccount


class UserAccountCreateSerializer(serializers.ModelSerializer):
    """
    {
        "id": "xxx-xxx-xxx",
        "username": "john_doe",
        "email": "john_doe@gmail.com",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    """

    class Meta:
        model = UserAccount
        fields = ["id", "username", "email", "password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")

        if not password:
            raise serializers.ValidationError({"password": "Password is required."})

        validate_password(password)

        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserAccountAdminSerializer(serializers.ModelSerializer):
    """
    {
        "id": "xxx-xxx-xxx",
        "username": "john_doe",
        "email": "john_doe@gmail.com",
        "is_superuser": True/False,
        "is_staff": True/False,
        "is_active": True/False,
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
        "comments": [
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
        ]
    }
    """

    comments = CommentNestedSerializer(read_only=True, many=True)

    class Meta:
        model = UserAccount
        fields = [
            "id",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "comments",
        ]
        read_only_fields = [
            "id",
            "is_superuser",
            "is_staff",
            "created_at",
            "updated_at",
            "deleted_at",
            "comments",
        ]


class UserAccountPublicSerializer(serializers.ModelSerializer):
    """
    {
        "id": "xxx-xxx-xxx",
        "username": "john_doe",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "comments": [
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
        ]
    }
    """

    comments = CommentNestedSerializer(read_only=True, many=True)

    class Meta:
        model = UserAccount
        fields = [
            "id",
            "username",
            "created_at",
            "updated_at",
            "comments",
        ]


class UserAccountMeSerializer(serializers.ModelSerializer):
    """
    {
        "id": "xxx-xxx-xxx",
        "username": "john_doe",
        "email": "john_doe@gmail.com",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "comments": [
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
        ]
    }
    """

    comments = CommentNestedSerializer(read_only=True, many=True)

    class Meta:
        model = UserAccount
        fields = [
            "id",
            "username",
            "email",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
