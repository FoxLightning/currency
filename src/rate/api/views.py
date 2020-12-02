from rest_framework import viewsets

from rate.api.serializers import RateSerializer
from rate.models import Rate


class RateAPIViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().order_by('-id')
    serializer_class = RateSerializer
