from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsSuperUser

from .models import UserAccount
from .serializers import (
    UserAccountCreateSerializer,
    UserAccountListSerializer,
    UserAccountRetrieveSerializer,
    UserAccountSerializer,
)


class UserAccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = UserAccount.objects.filter(deleted_at__isnull=True).order_by(
        "-created_at"
    )

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated]
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
        elif self.action == "retrieve":
            return UserAccountRetrieveSerializer
        elif self.action == "list":
            return UserAccountListSerializer
        elif self.action == "partial_update":
            return UserAccountSerializer
        return UserAccountRetrieveSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class UserAccountMeViewSet(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
