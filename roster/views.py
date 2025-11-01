from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsAuthenticatedOwner, IsSuperUser

from .models import Comment, Player, Team
from .serializers.comment import (
    CommentCreateSerializer,
    CommentListRetrieveAdminSerializer,
    CommentListRetrievePublicSerializer,
    CommentPatchSerializer,
)
from .serializers.player import (
    PlayerCommentCreateSerializer,
    PlayerCommentListRetrieveAdminSerializer,
    PlayerCommentListRetrievePublicSerializer,
    PlayerCommentPatchSerializer,
    PlayerCreateSerializer,
    PlayerListRetrieveAdminSerializer,
    PlayerListRetrievePublicSerializer,
    PlayerPatchSerializer,
)
from .serializers.team import (
    TeamCreateSerializer,
    TeamListRetrieveAdminSerializer,
    TeamListRetrievePublicSerializer,
    TeamPatchSerializer,
    TeamPlayerCreateSerializer,
    TeamPlayerListRetrieveAdminSerializer,
    TeamPlayerListRetrievePublicSerializer,
    TeamPlayerPatchSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Team.objects.all().order_by("-created_at")
        return Team.objects.filter(deleted_at__isnull=True).order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return TeamCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return TeamListRetrieveAdminSerializer
            return TeamListRetrievePublicSerializer
        elif self.action == "partial_update":
            return TeamPatchSerializer
        return TeamListRetrievePublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class PlayerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Player.objects.all().order_by("-created_at")
        return Player.objects.filter(deleted_at__isnull=True).order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return PlayerCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return PlayerListRetrieveAdminSerializer
            return PlayerListRetrievePublicSerializer
        elif self.action == "partial_update":
            return PlayerPatchSerializer
        return PlayerListRetrievePublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all().order_by("-created_at")
        return Comment.objects.filter(deleted_at__isnull=True).order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "partial_update":
            permission_classes = [IsAdminUser | IsAuthenticatedOwner]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser | IsAuthenticatedOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return CommentListRetrieveAdminSerializer
            return CommentListRetrievePublicSerializer
        elif self.action == "partial_update":
            return CommentPatchSerializer
        return CommentListRetrievePublicSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class TeamPlayerViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Player.objects.filter(team=self.kwargs["team_pk"]).order_by(
                "-created_at"
            )
        return Player.objects.filter(
            team=self.kwargs["team_pk"], deleted_at__isnull=True
        ).order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return TeamPlayerCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return TeamPlayerListRetrieveAdminSerializer
            return TeamPlayerListRetrievePublicSerializer
        elif self.action == "partial_update":
            return TeamPlayerPatchSerializer
        return TeamPlayerListRetrievePublicSerializer

    def perform_create(self, serializer):
        serializer.save(team=self.kwargs["team_pk"])

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class PlayerCommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.filter(player=self.kwargs["player_pk"]).order_by(
                "-created_at"
            )
        return Comment.objects.filter(
            player=self.kwargs["player_pk"], deleted_at__isnull=True
        ).order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "partial_update":
            permission_classes = [IsAdminUser | IsAuthenticatedOwner]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser | IsAuthenticatedOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return PlayerCommentCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return PlayerCommentListRetrieveAdminSerializer
            return PlayerCommentListRetrievePublicSerializer
        elif self.action == "partial_update":
            return PlayerCommentPatchSerializer
        return PlayerCommentListRetrievePublicSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, player=self.kwargs["player_pk"])

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
