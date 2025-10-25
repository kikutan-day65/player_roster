from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CommentViewSet, PlayerViewSet, TeamPlayerViewSet, TeamViewSet

router = SimpleRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"comments", CommentViewSet, basename="comment")

team_player_router = NestedSimpleRouter(router, r"teams", lookup="team")
team_player_router.register(r"players", TeamPlayerViewSet, basename="team_player")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(team_player_router.urls)),
]
