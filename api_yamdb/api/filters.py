import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
