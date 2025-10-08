from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlayerViewSet, TeamViewSet

router = DefaultRouter()
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"teams", TeamViewSet, basename="team")

urlpatterns = [
    path("", include(router.urls)),
]
