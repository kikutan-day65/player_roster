from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserAccount


class UserAccountCreateSerializer(serializers.ModelSerializer):
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


class UserAccountListSerializer(serializers.ModelSerializer):
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


class UserAccountRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "created_at", "updated_at"]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "username", "email", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
