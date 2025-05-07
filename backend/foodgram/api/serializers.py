from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreateSerializer as DjoserUserCreateSerializer
)
from django.contrib.auth import get_user_model
from rest_framework import serializers as ser
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredient, RecipeIngredient, Recipe


User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """An extended djoser serializer to get users data.

    This serializer is used when receiving information about user(s),
    i.e. `/api/users/` and `/api/users/me/`.
    """

    is_subscribed = ser.SerializerMethodField()
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
            return request.user.authors.filter(author=obj).exists()
        return False


class UserCreateSerializer(DjoserUserCreateSerializer):
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



class IngredientSerializer(ser.ModelSerializer):
    """An ingredient serializer."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(ser.ModelSerializer):
    """An ingredient in a recipe serializer."""

    id = ser.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(),
    )
    name = ser.CharField(
        source='ingredient.name', read_only=True,
    )
    measurement_unit = ser.CharField(
        source='ingredient.measurement_unit', read_only=True,
    )
    amount = ser.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ser.ModelSerializer):
    """A recipe serializer.

    Example:
    {
        'id': 1,
        'author': {
            'id': 1,
            'email': 'first_user@example.com',
            'username': 'first_user',
            'first_name': 'Joe',
            'last_name': 'Mama',
            'is_subscribed': False,
            'avatar': 'https://example.com/avatar.jpg',
        },
        'ingredients': [{'id': 1, 'amount': 5}, ...],
        'is_favorited': True,
        'is_in_shopping_cart': False,
        'name': 'My recipe!!!',
        'image': 'https://example.com/image.jpg',
        'text': 'Recipe text',
        'cooking_time': 60
    }
    """

    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_amounts', many=True,
    )
    is_favorited = ser.SerializerMethodField()
    is_in_shopping_cart = ser.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    # Getters.
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.shopping_carts.filter(user=request.user).exists()
        return False

    # Validators and setters.
    @staticmethod
    def validate_image(image):
        """Prevent empty image fields from being saved (i.e. {'image': ''})."""
        if not image:
            raise ser.ValidationError({'image': 'Обязательное поле.'})
        return image

    @staticmethod
    def validate_ingredients(ingredients):
        """Ingredients must: be non-empty, exist, be unique.

        Will be called in Serializer.validate() method.
        """
        if not ingredients:
            raise ser.ValidationError({'ingredients': 'Обязательное поле.'})
        ids = [x['ingredient'].id for x in ingredients]
        duplicate_ids = [x for x in ids if ids.count(x) > 1]
        if duplicate_ids:
            raise ser.ValidationError(
                {'ingredients': f'Ингредиенты {duplicate_ids} повторяются.'}
            )
        not_exist_ids = [x for x in ids
                         if not Ingredient.objects.filter(id=x).exists()]
        if not_exist_ids:
            raise ser.ValidationError(
                {'ingredients': f'Не найден(ы) ингредиенты {not_exist_ids}.'}
            )
        return ingredients

    @staticmethod
    def set_recipe_ingredients(recipe, ingredients):
        """Set recipe's ingredients."""
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=x['ingredient'].id,
                amount=x['amount'],
            )
            for x in ingredients
        )

    # Core methods.
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_amounts')
        recipe = super().create(validated_data)
        self.set_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_amounts', None)
        ingredients_data = self.validate_ingredients(ingredients_data)
        instance = super().update(instance, validated_data)
        instance.ingredients_amounts.all().delete()
        self.set_recipe_ingredients(instance, ingredients_data)
        return instance


class ShortRecipeSerializer(ser.ModelSerializer):
    """A shortened serializer for working with subscriptions and baskets."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipesSerializer(DjoserUserSerializer):
    """A user with his recipes serializer.

    Example:
    {
        'email': 'second_user@example.com',
        'id': 2,
        'username': 'second_user',
        'first_name': 'Yuri',
        'last_name': 'Tarded',
        'is_subscribed': true,
        'recipes': [{
            'id': 1,
            'name': 'Are you reading?',
            'image': 'https://example.com/image.jpg',
            'cooking_time': 66
        }, ...],
        'recipes_count': 1,
        'avatar': 'https://example.com/image.jpg'
    }
    """
    recipes = ser.SerializerMethodField()
    recipes_count = ser.IntegerField(source='recipes.count', read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', 'avatar'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = int(request.query_params.get('recipes_limit', '10000'))
        return ShortRecipeSerializer(
            obj.recipes.all()[:recipes_limit], many=True, context=self.context
        ).data
