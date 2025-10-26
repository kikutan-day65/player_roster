from django.utils import timezone
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsSuperUser

from .models import UserAccount
from .serializers import (
    UserAccountCreateSerializer,
    UserAccountListAdminSerializer,
    UserAccountListPublicSerializer,
    UserAccountMePatchSerializer,
    UserAccountMeRetrieveSerializer,
    UserAccountPatchSerializer,
    UserAccountRetrieveAdminSerializer,
    UserAccountRetrievePublicSerializer,
)


class UserAccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserAccount.objects.all().order_by("-created_at")
        return UserAccount.objects.filter(deleted_at__isnull=True).order_by(
            "-created_at"
        )

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "partial_update":
            permission_classes = [IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return UserAccountCreateSerializer
        elif self.action == "list":
            if self.request.user.is_staff:
                return UserAccountListAdminSerializer
            return UserAccountListPublicSerializer
        elif self.action == "retrieve":
            if self.request.user.is_staff:
                return UserAccountRetrieveAdminSerializer
            return UserAccountRetrievePublicSerializer
        elif self.action == "partial_update":
            return UserAccountPatchSerializer
        return UserAccountRetrievePublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class UserAccountMeViewSet(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserAccountMeRetrieveSerializer
        elif self.request.method == "PATCH":
            return UserAccountMePatchSerializer
        return UserAccountMeRetrieveSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class UserAccountCommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.filter(user=self.kwargs["user_pk"]).order_by(
                "-created_at"
            )
        return Comment.objects.filter(
            user=self.kwargs["user_pk"], deleted_at__isnull=True
        ).order_by("-created_at")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "partial_update":
            permission_classes = [IsAdminUser | IsAuthenticatedOwner]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser | IsAuthenticatedOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return UserAccountCommentListRetrieveAdminSerializer
            return UserAccountCommentListRetrievePublicSerializer
        elif self.action == "partial_update":
            return UserAccountCommentPatchSerializer
        return UserAccountCommentListRetrievePublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
