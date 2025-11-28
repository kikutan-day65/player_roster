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
    UserAccountCommentListAdminSerializer,
    UserAccountCommentListPublicSerializer,
    UserAccountCreateSerializer,
    UserAccountListRetrieveAdminSerializer,
    UserAccountListRetrievePublicSerializer,
    UserAccountPatchSerializer,
)


class UserAccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

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
