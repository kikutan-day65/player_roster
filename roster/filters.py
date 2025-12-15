import django_filters as filters

from .models import Comment, Player, Team


class TeamFilter(filters.FilterSet):
    sport = filters.ChoiceFilter(field_name="sport", choices=Team.SportChoice)
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    created_at_date = filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_year = filters.NumberFilter(field_name="created_at", lookup_expr="year")
    created_at_year_gte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__gte"
    )
    created_at_year_lte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__lte"
    )

    class Meta:
        model = Team
        fields = []


class PlayerFilter(filters.FilterSet):
    team_name = filters.CharFilter(field_name="team__name", lookup_expr="icontains")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    created_at_date = filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_year = filters.NumberFilter(field_name="created_at", lookup_expr="year")
    created_at_year_gte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__gte"
    )
    created_at_year_lte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__lte"
    )

    class Meta:
        model = Player
        fields = []


class CommentFilter(filters.FilterSet):
    user_username = filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    player_first_name = filters.CharFilter(
        field_name="player__first_name", lookup_expr="icontains"
    )
    player_last_name = filters.CharFilter(
        field_name="player__last_name", lookup_expr="icontains"
    )
    created_at_date = filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_year = filters.NumberFilter(field_name="created_at", lookup_expr="year")
    created_at_year_gte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__gte"
    )
    created_at_year_lte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__lte"
    )

    class Meta:
        model = Comment
        fields = []
