from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django_filters.rest_framework import DjangoFilterBackend

from djoser.views import UserViewSet as DjoserUserViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            Favorite, ShoppingCart)

from api.filters import NameFilterSet, RecipeFilterSet
from api.permissions import IsObjAuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             ShortRecipeSerializer, UserRecipesSerializer)


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
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
                raise ValidationError({'avatar': 'Обязательное поле.'})
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'avatar': serializer.data['avatar']}
            return Response(data, status=status.HTTP_200_OK)

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
        queryset = User.objects.filter(authors__subscriber=request.user)
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
                raise ValidationError('Нельзя подписаться на самого себя.')
            obj, is_created = user.subscriptions.get_or_create(author=author)
            if not is_created:
                raise ValidationError(f'Вы уже подписаны на {author}.')
            serializer = UserRecipesSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Specification awaits the return of the HTTP400, not HTTP404,
        # Therefore, don't use get_object_or_404().
        obj = user.subscriptions.filter(author=author)
        if not obj.exists():
            raise ValidationError('Вы не подписаны.')
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Get specific or all ingredients."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NameFilterSet


class RecipeViewSet(ModelViewSet):
    """CRUD operations with recipes."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    short_serializer_class = ShortRecipeSerializer
    permission_classes = (IsObjAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    # Core methods.
    def perform_create(self, serializer):
        """Create new recipe and assign author to it."""
        serializer.save(author=self.request.user)

    # Additional methods.
    def handle_user_recipe_relation(self, model, request, recipe_id):
        """POST or DEL user-recipe 'subscription' in Favorite or ShoppingCart.

        :param model: Favorite or ShoppingCart model class.
        :param request: request object.
        :param recipe_id: recipe id (pk).

        :return: POST -> 201 + (id, name, image, cooking_time)
                 DELETE -> 204
        :raises: 404 if recipe not found, 400 if relation already exists.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.method == 'POST':
            obj, is_created = model.objects.get_or_create(
                user_id=user.id, recipe_id=recipe.id
            )
            if not is_created:
                raise ValidationError(f'Рецепт "{recipe}" уже в списке.')
            return Response(self.short_serializer_class(recipe).data,
                            status=status.HTTP_201_CREATED)

        # Specification awaits the return of the HTTP400, not HTTP404,
        # Therefore, don't use get_object_or_404().
        obj = model.objects.filter(user=user, recipe=recipe)
        if not obj.exists():
            raise ValidationError(f'Рецепт "{recipe}" не существует.')
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def format_shopping_list_text(recipes, ingredients):
        """Return formatted string with recipes and ingredients amounts."""
        return '\n'.join([
            f'Список покупок от {datetime.now().strftime("%d.%m.%Y")}:',
            f'\nВы хотели приготовить:',
            *[f'{i}. {x.name}, автор: {x.author})'
              for i, x in enumerate(recipes, 1)],
            f'\nКупить:',
            *[f'{i}. {x["name"]} — {x["amount"]} {x["unit"]}'
              for i, x in enumerate(ingredients, 1)],
        ]) if ingredients else 'Список покупок пуст.'


    # Actions.
    @action(
        methods=('post', 'delete'),
        detail=True,
        url_path='favorite',
        url_name='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        """Add or remove recipe to/from user`s favorites."""
        return self.handle_user_recipe_relation(Favorite, request, pk)

    @action(
        methods=('post', 'delete'),
        detail=True,
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        """Add or remove recipe to/from user`s shopping cart."""
        return self.handle_user_recipe_relation(ShoppingCart, request, pk)

    @action(
        methods=('get',),
        detail=False,
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Return a file with a list of ingredients and their amounts."""
        recipes = Recipe.objects.filter(
            shopping_carts__user=request.user
        ).distinct()
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in=request.user.shopping_carts.values('recipe'))
            .values(name=F('ingredient__name'),
                    unit=F('ingredient__measurement_unit'))
            .annotate(amount=Sum('amount'))
            .order_by('name')
        )
        return FileResponse(
            self.format_shopping_list_text(recipes, ingredients),
            filename='shopping_list.txt',
            as_attachment=True,
            content_type='text/plain'
        )

    @action(
        methods=('get',),
        detail=True,
        url_path='get-link',
        url_name='get-link',
    )
    def get_link(self, request, pk):
        """Return a 'short'-link to the recipe."""
        get_object_or_404(Recipe, pk=pk)
        return Response({
            'short-link': request.build_absolute_uri(
                reverse('recipes:get_recipe', args=(pk,))
            )
        })
