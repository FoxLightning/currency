import django_filters

from rate.models import Rate


class RateFilter(django_filters.FilterSet):
    crated_day = django_filters.NumberFilter(field_name='created', lookup_expr='day')

    class Meta:
        model = Rate
        fields = [
            'source',
            'currency',
            'sale',
            'crated_day',
        ]
