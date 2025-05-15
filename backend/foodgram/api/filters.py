from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class NameFilterSet(filters.FilterSet):
    """Filterset for ingredients. Filter by ingredient name."""

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(filters.FilterSet):
    """Filterset for recipes.

    Filter recipes by:
    - `is_favorited`: 0/1 - whether the recipe is favorited by the user;
    - `is_in_shopping_cart`: 0/1 - whether the recipe is in the shopping cart;
    - `author`: integer - ID of the author.
    """

    BOOL_CHOICES = ((0, 'Нет'), (1, 'Да'))

    is_favorited = filters.TypedChoiceFilter(
        choices=BOOL_CHOICES, coerce=int, method='filter_boolean',
        label='Избранное',
    )
    is_in_shopping_cart = filters.TypedChoiceFilter(
        choices=BOOL_CHOICES, coerce=int, method='filter_boolean',
        label='Корзина',
    )
    author = filters.NumberFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    # Relation between filter name and model related field.
    related_fields = {
        'is_favorited': 'favorites',
        'is_in_shopping_cart': 'shopping_carts',
    }

    def filter_boolean(self, queryset, name, value):
        """Filter whether the recipe is in the user's lists.

        Filters the `queryset` based on the `value` of the related field
        given by `name`.
        Example: `is_favorited=1` - get favorite recipes of the user.
        """
        field = self.related_fields.get(name)
        if not field:
            return queryset
        if not self.request.user or not self.request.user.is_authenticated:
            return queryset.none()
        lookup = {f'{field}__user': self.request.user}
        return (queryset.filter(**lookup) if value == 1
                else queryset.exclude(**lookup))
