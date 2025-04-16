from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """An extended djoser serializer to get users data.

    This serializer is used when receiving information about user(s),
    i.e. `/api/users/` and `/api/users/me/`.
    """

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'avatar',
        )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request and request.user.is_authenticated:
            return request.user.followers.filter(author=obj).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """An extended djoser serializer to post users data

    Used when registering new user or on password change.
    """

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
