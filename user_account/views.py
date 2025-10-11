from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsSuperUser

from .models import UserAccount
from .serializers import (
    UserAccountAdminSerializer,
    UserAccountCreateSerializer,
    UserAccountMeSerializer,
    UserAccountPublicSerializer,
)


class UserAccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = UserAccount.objects.filter(deleted_at__isnull=True).order_by(
        "-created_at"
    )

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action in ["list", "partial_update"]:
            permission_classes = [IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return UserAccountCreateSerializer
        elif self.action in ["list", "partial_update"]:
            return UserAccountAdminSerializer
        elif self.action == "retrieve":
            if self.request.user.is_staff:
                return UserAccountAdminSerializer
            return UserAccountPublicSerializer
        return UserAccountPublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


class UserAccountMeViewSet(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    serializer_class = UserAccountMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
