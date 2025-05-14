from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram.constants import (
    USER_AVATAR_UPLOAD_TO, RECIPE_MIN_COOKING_TIME,
    RECIPE_IMAGE_UPLOAD_TO, RECIPE_INGREDIENT_MIN_AMOUNT
)


# Users.
class User(AbstractUser):
    """A custom user model.

    User model with custom required fields (in AbstractUser, them are
    username and password). In this model, all fields are required
    except profile_picture.
    """

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(
        verbose_name='E-Mail',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to=USER_AVATAR_UPLOAD_TO,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username} ({self.email})'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class Subscription(models.Model):
    """A user-to-author subscription model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор',
        help_text='Автор, на которого подписан пользователь.',
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
        help_text='Пользователь, подписанный на автора.',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='uq_subscription_subscriber_author'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='check_subscription_prevent_self_subscription'
            )
        ]
        ordering = ('author__username',)

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'



# Recipes.
class Ingredient(models.Model):
    """A model of the recipe ingredient."""

    name = models.CharField(
        verbose_name='Название',
        max_length=128,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='uq_ingredient_name_measurement_unit',
            ),
        ]
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """A model of the recipe.

    Recipe must have name, author, ingredients, text, cooking time.
    It may have image. Creation date is added automatically.
    """

    name = models.CharField(verbose_name='Название', max_length=256)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes',
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(RECIPE_MIN_COOKING_TIME),],
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=RECIPE_IMAGE_UPLOAD_TO,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """An ingredient used in the recipe model.

    The intermediate table indicates the amount of the ingredient in the recipe.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients_amounts',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='used_in_recipes',
        on_delete=models.PROTECT,  # Prevent deleting the ingredient if used.
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(RECIPE_INGREDIENT_MIN_AMOUNT),],
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        # There can be only one unique ingredient in recipe.
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='uq_recipe_ingredient_recipe_ingredient',
            ),
        ]
        ordering = ('recipe__created_at', 'ingredient__name',)


class AbstractUserRecipe(models.Model):
    """An abstract model for lists of the chosen and purchases.

    When using, it is necessary to specify `MyClass.Meta.default_related_name`.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'


class ShoppingCart(AbstractUserRecipe):
    """A user's shopping cart."""
    class Meta(AbstractUserRecipe.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_carts'
