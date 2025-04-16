import logging

from django.http import Http404
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound
from rest_framework.status import *
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser as User


class CustomUserViewSet(UserViewSet):
    """An extended UserViewSet.

    Added:
    - Limit offset pagination;
    - `/me/` endpoint;
    - `/me/avatar/` endpoint;
    - `/subscriptions/` endpoint;
    - `{id}/subscribe/` endpoint.
    """
    pagination_class = LimitOffsetPagination

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
                return Response({'avatar': ['Обязательное поле.']},
                                status=HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'avatar': serializer.data['avatar']}
            return Response(data, status=HTTP_200_OK)
        elif request.method == 'DELETE':
            request.user.avatar.delete()
            request.user.avatar = None
            request.user.save()
            return Response(status=HTTP_204_NO_CONTENT)

    # TODO: Will be implemented after Recipes.
    # @action(
    #     detail=False,
    #     methods=('get',),
    #     url_path='subscriptions',
    #     url_name='subscriptions',
    #     permission_classes=(IsAuthenticated,),
    # )
    # def subscriptions(self, request):
    #     """Return user`s subscriptions."""
    #     queryset = User.objects.filter(
    #         followers__subscriber=request.user
    #     )
    #     pages = self.paginate_queryset(queryset)
    #     serializer = self.get_serializer(
    #         pages, many=True, context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)

    # TODO: Will be implemented after Recipes.
    # @action(
    #     detail=True,
    #     methods=('post', 'delete'),
    #     url_path='subscribe',
    #     url_name='subscribe',
    #     permission_classes=(IsAuthenticated,),
    # )
    # def subscribe(self, request, pk):
    #     """Subscribe or unsubscribe to another user."""
    #     if request.method == 'POST':
    #         pass
    #     elif request.method == 'DELETE':
    #         pass
