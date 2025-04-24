from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """A model of the recipe ingredient."""

    name = models.CharField(
        verbose_name=_('Название'),
        max_length=128,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Единица измерения'),
        max_length=64,
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        # Use unique_together instead of unique name as
        # it's possible to have multiple measurements to one ingredient.
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='uq_ingredient_name_measurement_unit',
            ),
        ]
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class RecipeIngredient(models.Model):
    """An ingredient used in the recipe model.

    The intermediate table indicates the amount of the ingredient in the recipe.
    """

    recipe = models.ForeignKey(
        'Recipe',
        verbose_name=_('Рецепт'),
        related_name='ingredients_amounts',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name=_('Ингредиент'),
        related_name='used_in_recipes',
        on_delete=models.PROTECT,  # Prevent deleting the ingredient if used.
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('Количество'),
        validators=[MinValueValidator(1),],
    )

    class Meta:
        verbose_name = _('Ингредиент рецепта')
        verbose_name_plural = _('Ингредиенты рецепта')
        # There can be only one unique ingredient in recipe.
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='uq_recipe_ingredient_recipe_ingredient',
            ),
        ]
        ordering = ('recipe__created_at', 'ingredient__name',)


class Recipe(models.Model):
    """A model of the recipe.

    Recipe must have name, author, ingredients, text, cooking time.
    It may have image. Creation date is added automatically.
    """

    name = models.CharField(verbose_name=_('Название'), max_length=256)
    author = models.ForeignKey(
        'users.CustomUser',
        verbose_name=_('Автор'),
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name=_('Ингредиенты'),
        through='RecipeIngredient',
    )
    text = models.TextField(verbose_name=_('Описание'))
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Время приготовления'),
        validators=[MinValueValidator(1),],
    )
    image = models.ImageField(
        verbose_name=_('Изображение'),
        upload_to='recipes/images',
    )
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class AbstractUserRecipe(models.Model):
    """An abstract model for lists of the chosen and purchases.

    When using, it is necessary to specify `MyClass.Meta.default_related_name`.
    """

    user = models.ForeignKey(
        'users.CustomUser',
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name=_('Рецепт'),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uq_%(class)s_user_recipe',
            ),
        ]
        ordering = ('user__username', 'recipe__name',)

    def __str__(self):
        return f'{self.user.id} - {self.recipe.id}'


class Favorite(AbstractUserRecipe):
    """A user's favorite recipe(s)."""
    class Meta(AbstractUserRecipe.Meta):
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранное')
        default_related_name = 'favorites'


class ShoppingCart(AbstractUserRecipe):
    """A user's shopping cart."""
    class Meta(AbstractUserRecipe.Meta):
        verbose_name = _('Список покупок')
        verbose_name_plural = _('Списки покупок')
        default_related_name = 'shopping_carts'
