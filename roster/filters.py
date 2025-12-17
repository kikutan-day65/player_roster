from django_filters import rest_framework as filters

from core.filters import BaseFilterSet

from .models import Comment, Player, Team


class TeamFilter(BaseFilterSet):
    sport = filters.ChoiceFilter(field_name="sport", choices=Team.SportChoice)
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Team
        fields = []


class PlayerFilter(BaseFilterSet):
    team_name = filters.CharFilter(field_name="team__name", lookup_expr="icontains")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")

    class Meta:
        model = Player
        fields = []


class CommentFilter(BaseFilterSet):
    user_username = filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
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
