from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Ingredient, Recipe
from api.v1.serializers.recipes import IngredientSerializer, RecipeSerializer
from api.v1.permissions import IsObjAuthorOrReadOnly
from api.v1.filters import NameFilterSet, RecipeFilterSet


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
    permission_classes = (IsObjAuthorOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
