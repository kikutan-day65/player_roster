from django_filters import rest_framework as filters


class BaseFilterSet(filters.FilterSet):
    created_at_date = filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_year = filters.NumberFilter(field_name="created_at", lookup_expr="year")
    created_at_year_gte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__gte"
    )
    created_at_year_lte = filters.NumberFilter(
        field_name="created_at", lookup_expr="year__lte"
    )
