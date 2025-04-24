from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from djoser.views import UserViewSet

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser as User
from api.v1.serializers.recipes import UserRecipesSerializer


class CustomUserViewSet(UserViewSet):
    """An extended UserViewSet.

    Added:
    - Limit offset pagination;
    - `/me/` endpoint;
    - `/me/avatar/` endpoint;
    - `/subscriptions/` endpoint;
    - `{id}/subscribe/` endpoint.
    """

    # Rename `id` to `pk` as id is a python reserved keyword.
    lookup_url_kwarg = 'pk'

    def get_object(self):
        """Just translate a 404 error."""
        try:
            return super().get_object()
        except Http404:
            raise NotFound(_('Пользователь не найден.'))

    @action(
        methods=('get',),
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),  # The only updated part.
    )
    def me(self, request):
        """Redefine permissions of `/me/`."""
        serializer = self.get_serializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data)

    @action(
        methods=('put', 'delete'),
        detail=False,
        url_path='me/avatar',
        url_name='me/avatar',
        permission_classes=(IsAuthenticated,),
    )
    def avatar(self, request):
        """Update and delete user`s avatar."""
        if request.method == 'PUT':
            if 'avatar' not in request.data:
                raise ValidationError({'avatar': _('Обязательное поле.')})
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'avatar': serializer.data['avatar']}
            return Response(data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            request.user.avatar.delete()
            request.user.avatar = None
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get',),
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Return user`s subscriptions."""
        queryset = User.objects.filter(followers__subscriber=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = UserRecipesSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=('post', 'delete'),
        detail=True,
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        """(Un)subscribe to another user."""
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            if user == author:
                raise ValidationError(_('Нельзя подписаться на самого себя.'))
            obj, is_created = user.subscriptions.get_or_create(author=author)
            if not is_created:
                raise ValidationError(_('Вы уже подписаны.'))
            serializer = UserRecipesSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            obj = user.subscriptions.filter(author=author)
            if not obj.exists():
                raise ValidationError(_('Вы не подписаны.'))
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
