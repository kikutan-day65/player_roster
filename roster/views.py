import django_filters.rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAuthenticatedOwner, IsSuperUser

from .filters import CommentFilter, PlayerFilter, TeamFilter
from .models import Comment, Player, Team
from .serializers.comment import (
    CommentCreateSerializer,
    CommentListRetrieveAdminSerializer,
    CommentListRetrievePublicSerializer,
    CommentPatchSerializer,
)
from .serializers.player import (
    PlayerCommentListAdminSerializer,
    PlayerCommentListPublicSerializer,
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
    TeamPlayerListAdminSerializer,
    TeamPlayerListPublicSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TeamFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Team.objects.all()
        else:
            qs = Team.objects.filter(deleted_at__isnull=True)
        return qs.order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            permission_class = [IsAdminUser]
        elif self.action in ["list", "retrieve", "players"]:
            permission_class = [AllowAny]
        elif self.action == "destroy":
            permission_class = [IsSuperUser]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]

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
        instance.soft_delete()

    @action(detail=True, methods=["get"], url_name="players")
    def players(self, request, pk=None):
        target_team = self.get_object()

        is_admin = request.user.is_staff

        if is_admin:
            serializer_class = TeamPlayerListAdminSerializer
            player_qs = Player.objects.filter(team=target_team)
        else:
            serializer_class = TeamPlayerListPublicSerializer
            player_qs = Player.objects.filter(team=target_team, deleted_at__isnull=True)

        players = player_qs.order_by("-created_at")

        page = self.paginate_queryset(players)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(players, many=True)

        return Response(serializer.data)


class PlayerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlayerFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Player.objects.all()
        else:
            qs = Player.objects.filter(deleted_at__isnull=True)
        return qs.order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            permission_class = [IsAdminUser]
        elif self.action in ["list", "retrieve", "comments"]:
            permission_class = [AllowAny]
        elif self.action == "destroy":
            permission_class = [IsSuperUser]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]

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
        instance.soft_delete()

    @action(detail=True, url_name="comments")
    def comments(self, request, pk=None):
        target_player = self.get_object()

        is_admin = request.user.is_staff

        if is_admin:
            serializer_class = PlayerCommentListAdminSerializer
            comment_qs = Comment.objects.filter(player=target_player)
        else:
            serializer_class = PlayerCommentListPublicSerializer
            comment_qs = Comment.objects.filter(
                player=target_player, deleted_at__isnull=True
            )

        comments = comment_qs.order_by("-created_at")

        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(comments, many=True)

        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Comment.objects.all()
        else:
            qs = Comment.objects.filter(deleted_at__isnull=True)
        return qs.order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            permission_class = [IsAuthenticated]
        elif self.action in ["list", "retrieve"]:
            permission_class = [AllowAny]
        elif self.action == "partial_update":
            permission_class = [IsAdminUser | IsAuthenticatedOwner]
        elif self.action == "destroy":
            permission_class = [IsSuperUser | IsAuthenticatedOwner]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]

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
        instance.soft_delete()
