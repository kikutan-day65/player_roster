from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.nested_serializers import PlayerNestedSerializer
from roster.models import Comment

from .models import UserAccount


# ==================================================
# UserAccount
# ==================================================
class UserAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "email", "password", "created_at"]
        read_only_fields = ["id", "created_at"]
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


class UserAccountListRetrievePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "created_at"]
        read_only_fields = ["id", "username", "created_at"]


class UserAccountListRetrieveAdminSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class UserAccountPatchSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = [
            "id",
            "is_superuser",
            "is_staff",
            "created_at",
            "updated_at",
        ]


# ==================================================
# UserAccountComment
# ==================================================
class UserAccountCommentListRetrievePublicSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "player"]
        read_only_fields = ["id", "body", "created_at", "updated_at", "player"]


class UserAccountCommentListRetrieveAdminSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "deleted_at", "player"]
        read_only_fields = [
            "id",
            "body",
            "created_at",
            "updated_at",
            "deleted_at",
            "player",
        ]


# ==================================================
# Me
# ==================================================
class MeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "email", "created_at", "updated_at"]
        read_only_fields = ["id", "username", "email", "created_at", "updated_at"]


class MePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "email", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================================================
# MeComment
# ==================================================
class MeCommentListRetrieveSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "player"]
        read_only_fields = ["id", "body", "created_at", "updated_at", "player"]


class MeCommentPatchSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "player"]
        read_only_fields = ["id", "created_at", "updated_at", "player"]
