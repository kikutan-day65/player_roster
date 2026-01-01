from django_filters import rest_framework as django_filters
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.mixins.throttles import UserRoleBasedThrottleMixin
from core.permissions import IsSuperUser
from roster.models import Comment

from .filters import MeCommentFilter, UserAccountFilter
from .models import UserAccount
from .serializers import (
    MeCommentListSerializer,
    MePatchSerializer,
    MeRetrieveSerializer,
    UserAccountCommentListAdminSerializer,
    UserAccountCommentListPublicSerializer,
    UserAccountCreateSerializer,
    UserAccountListRetrieveAdminSerializer,
    UserAccountListRetrievePublicSerializer,
    UserAccountPatchSerializer,
)


class UserAccountViewSet(UserRoleBasedThrottleMixin, viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserAccountFilter
    search_fields = ["username"]

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = UserAccount.objects.all()
        else:
            qs = UserAccount.objects.filter(deleted_at__isnull=True)

        return qs.order_by("-created_at")

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve", "comments"]:
            permission_class = [AllowAny]
        elif self.action == "partial_update":
            permission_class = [IsAdminUser]
        elif self.action == "destroy":
            permission_class = [IsSuperUser]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action == "create":
            return UserAccountCreateSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return UserAccountListRetrieveAdminSerializer
            return UserAccountListRetrievePublicSerializer
        elif self.action == "partial_update":
            return UserAccountPatchSerializer
        return UserAccountListRetrievePublicSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=["get"], url_name="comments")
    def comments(self, request, pk=None):
        target_user = self.get_object()

        is_admin = request.user.is_staff

        if is_admin:
            serializer_class = UserAccountCommentListAdminSerializer
            comment_qs = Comment.objects.filter(user=target_user)
        else:
            serializer_class = UserAccountCommentListPublicSerializer
            comment_qs = Comment.objects.filter(
                user=target_user, deleted_at__isnull=True
            )

        comments = comment_qs.order_by("-created_at")

        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(comments, many=True)

        return Response(serializer.data)


class MeAPIView(UserRoleBasedThrottleMixin, generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MeRetrieveSerializer
        elif self.request.method == "PATCH":
            return MePatchSerializer
        return MeRetrieveSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.soft_delete()


class MeCommentAPIView(UserRoleBasedThrottleMixin, generics.ListAPIView):
    http_method_names = ["get"]
    serializer_class = MeCommentListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = MeCommentFilter
    search_fields = ["body", "player__first_name", "player__last_name"]

    def get_queryset(self):
        qs = Comment.objects.filter(user=self.request.user, deleted_at__isnull=True)
        return qs.order_by("-created_at")
