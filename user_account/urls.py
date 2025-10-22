from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserAccountMeViewSet, UserAccountViewSet

router = SimpleRouter()
router.register(r"user-accounts", UserAccountViewSet, basename="user_account")

urlpatterns = [
    path("user-accounts/me/", UserAccountMeViewSet.as_view(), name="user_account_me"),
    path("", include(router.urls)),
]
