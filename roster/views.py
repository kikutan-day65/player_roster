from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions import IsSuperUser
from roster.serializers.player import PlayerAdminSerializer, PlayerPublicSerializer
from roster.serializers.team import TeamAdminSerializer, TeamPublicSerializer

from .models import Player, Team


class PlayerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = Player.objects.filter(deleted_at__isnull=True).order_by("-created_at")

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
        if self.action in ["create", "partial_update"]:
            return PlayerAdminSerializer
        elif self.action in ["list", "retrieve"]:
            if self.request.user.is_staff:
                return PlayerAdminSerializer
            return PlayerPublicSerializer
        elif self.action == "destroy":
            return PlayerAdminSerializer
        return PlayerPublicSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])
