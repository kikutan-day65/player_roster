from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import MeAPIView, MeCommentAPIView, UserAccountViewSet

router = SimpleRouter()
router.register(r"user-accounts", UserAccountViewSet, basename="user_account")

# fmt: off
urlpatterns = [
    path("user-accounts/me/", MeAPIView.as_view(), name="me"),
    path("user-accounts/me/comments/", MeCommentAPIView.as_view(), name="me_comments"),
    path("", include(router.urls)),
]
# fmt: on
