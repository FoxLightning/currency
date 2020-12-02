from rest_framework import viewsets

from account.api.serializers import AvatarSerializer, UserSerializer
from account.models import Avatar, User


class AvatarAPIViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all().order_by('-id')
    serializer_class = AvatarSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
