from django.urls import include, path
from rest_framework.routers import SimpleRouter

from roster.views import CommentViewSet, PlayerViewSet, TeamViewSet

router = SimpleRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
]
