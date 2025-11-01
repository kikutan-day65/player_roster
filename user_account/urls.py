from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    MeCommentListView,
    MeCommentRetrieveUpdateDestroyView,
    MeRetrieveUpdateDestroyView,
    UserAccountCommentViewSet,
    UserAccountViewSet,
)

router = SimpleRouter()
router.register(r"user-accounts", UserAccountViewSet, basename="user_account")

user_comment_router = NestedSimpleRouter(router, r"user-accounts", lookup="user")
user_comment_router.register(
    r"comments", UserAccountCommentViewSet, basename="user_account_comment"
)

# fmt: off
urlpatterns = [
    path("user-accounts/me/", MeRetrieveUpdateDestroyView.as_view(), name="me"),
    path("user-accounts/me/comments/", MeCommentListView.as_view(), name="me_comment_list"),
    path("user-accounts/me/comments/<uuid:pk>/", MeCommentRetrieveUpdateDestroyView.as_view(), name="me_comment_detail"),
    path("", include(router.urls)),
    path("", include(user_comment_router.urls)),
]
# fmt: on
