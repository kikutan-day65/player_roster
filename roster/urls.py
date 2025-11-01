from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    CommentViewSet,
    PlayerCommentViewSet,
    PlayerViewSet,
    TeamPlayerViewSet,
    TeamViewSet,
)

router = SimpleRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"comments", CommentViewSet, basename="comment")

team_player_router = NestedSimpleRouter(router, r"teams", lookup="team")
team_player_router.register(r"players", TeamPlayerViewSet, basename="team_player")

player_comment_router = NestedSimpleRouter(router, r"players", lookup="player")
player_comment_router.register(
    r"comments", PlayerCommentViewSet, basename="player_comment"
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(team_player_router.urls)),
    path("", include(player_comment_router.urls)),
]
