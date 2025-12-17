from django_filters import rest_framework as filters

from core.filters import BaseFilterSet
from roster.models import Comment

from .models import UserAccount


class UserAccountFilter(BaseFilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = UserAccount
        fields = []


class MeCommentFilter(BaseFilterSet):
    team_name = filters.CharFilter(
        field_name="player__team__name", lookup_expr="icontains"
    )
    player_first_name = filters.CharFilter(
        field_name="player__first_name", lookup_expr="icontains"
    )
    player_last_name = filters.CharFilter(
        field_name="player__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = Comment
        fields = []
