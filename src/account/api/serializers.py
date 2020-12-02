from rest_framework import serializers

from account.models import Avatar, User


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = (
            'user',
            'file_path',
            'active_avatar',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            # main info
            'id',
            'username',
            'email',
            # 'get_password',
            # 'set_password',
            # additional info
            'first_name',
            'last_name',
            # permisions
            'is_superuser',
            'is_staff',
        )
