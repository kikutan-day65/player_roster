from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsAuthenticatedOwner, IsSuperUser
from roster.models import Comment

from .models import UserAccount
from .serializers import (
    MeCommentListRetrieveSerializer,
    MeCommentPatchSerializer,
    MePatchSerializer,
    MeRetrieveSerializer,
    UserAccountCommentListRetrieveAdminSerializer,
    UserAccountCommentListRetrievePublicSerializer,
    UserAccountCommentPatchSerializer,
    UserAccountCreateSerializer,
    UserAccountListRetrieveAdminSerializer,
    UserAccountListRetrievePublicSerializer,
    UserAccountPatchSerializer,
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
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return UserAccountListRetrieveAdminSerializer
            return UserAccountListRetrievePublicSerializer
        elif self.action == "partial_update":
            return UserAccountPatchSerializer
        return UserAccountListRetrieveAdminSerializer

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


class MeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MeRetrieveSerializer
        elif self.request.method == "PATCH":
            return MePatchSerializer
        return MeRetrieveSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class MeCommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user, deleted_at__isnull=True
        ).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return MeCommentPatchSerializer
        return MeCommentListRetrieveSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class MeCommentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeCommentListRetrieveSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user, deleted_at__isnull=True
        ).order_by("-created_at")
