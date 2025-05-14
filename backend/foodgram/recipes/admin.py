from django.db.models import Count
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.safestring import mark_safe

from .models import (
    User, Subscription, Ingredient, Recipe, RecipeIngredient,
    Favorite, ShoppingCart
)
from .admin_filters import (
    RecipeCountFilter, SubscriberCountFilter, SubscriptionCountFilter,
    UsedInRecipesCountFilter, CookingTimeFilter
)


# Users.
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'subscriber')
    list_filter = ('author', 'subscriber')
    search_fields = ('author__username', 'subscriber__username')
    ordering = ('author',)


class FollowerInline(admin.TabularInline):
    """View subscribers of author."""
    model = Subscription
    fk_name = 'author'
    extra = 0
    verbose_name = 'Подписчик'
    verbose_name_plural = 'Подписчики'
    fields = ('subscriber',)
    raw_id_fields = ('subscriber',)


class SubscriptionInline(admin.TabularInline):
    """View subscriptions of user."""
    model = Subscription
    fk_name = 'subscriber'
    extra = 0
    verbose_name = 'Подписка'
    verbose_name_plural = 'Подписки'
    fields = ('author',)
    raw_id_fields = ('author',)


class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 0
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    verbose_name = 'Избранный рецепт'
    verbose_name_plural = 'Избранное'


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0
    verbose_name = 'Рецепт в корзине'
    verbose_name_plural = 'Корзина покупок'


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [FollowerInline,
               SubscriptionInline,
               RecipeInline,
               FavoriteInline,
               ShoppingCartInline,]
    list_display = ('id',
                    'username',
                    'full_name',
                    'email',
                    'avatar_preview',
                    'recipe_count',
                    'subscriptions_count',
                    'subscribers_count',
                    'is_staff',)
    list_display_links = ('username', 'email')
    list_filter = ('date_joined',
                   RecipeCountFilter,
                   SubscriptionCountFilter,
                   SubscriberCountFilter,
                   'is_staff',
                   'is_active',)
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    # Update the default form.
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')}
         ),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name', 'avatar',
                       'last_login', 'date_joined'),
        }),
        ('Права', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
    )

    # Add first and last name fields in the Add form.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            recipe_count=Count('recipes', distinct=True),
            subscriptions_count=Count('subscriptions', distinct=True),
            subscribers_count=Count('authors', distinct=True),
        )

    @admin.display(description='Имя и фамилия')
    def full_name(self, user):
        return user.get_full_name()

    @mark_safe
    @admin.display(description='Аватар')
    def avatar_preview(self, user):
        if user.avatar:
            return (f'<img src="{user.avatar.url}"'
                    f'style="height: 30px; width: 30px; border-radius: 50%;">')
        return '-'

    @admin.display(description='Рецептов')
    def recipe_count(self, user):
        return user.recipe_count

    @admin.display(description='Подписок')
    def subscriptions_count(self, user):
        return user.subscriptions_count

    @admin.display(description='Подписчиков')
    def subscribers_count(self, user):
        return user.subscribers_count


# Recipes.
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'used_in_recipes_count')
    list_display_links = ('name',)
    list_filter = ('measurement_unit', UsedInRecipesCountFilter)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            used_in_recipes_count=Count('recipes', distinct=True),
        )

    @admin.display(description='Использован в рецептах')
    def used_in_recipes_count(self, ingredient):
        return ingredient.used_in_recipes_count


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    verbose_name = 'Ингредиент рецепта'
    verbose_name_plural = 'Ингредиенты рецепта'
    fields = ('ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline,]
    list_display = ('id',
                    'name',
                    'cooking_time',
                    'author',
                    'favorited_count',
                    'get_ingredients',
                    'image_preview')
    list_display_links = ('name',)
    list_filter = (CookingTimeFilter,)
    search_fields = ('name', 'ingredients__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    @admin.display(description='В избранном')
    def favorited_count(self, recipe):
        return recipe.favorites.count()

    @mark_safe
    @admin.display(description='Ингредиенты')
    def get_ingredients(self, recipe):
        return '<br>'.join(
            f'- {item.ingredient.name} {item.amount} '
            f'{item.ingredient.measurement_unit}'
            for item in recipe.ingredients_amounts.all()
        )

    @mark_safe
    @admin.display(description='Изображение')
    def image_preview(self, recipe):
        if recipe.image:
            return f'<img src="{recipe.image.url}" style="height: 100px">'
        return '-'


@admin.register(Favorite, ShoppingCart)
class UserRecipeAdmin(admin.ModelAdmin):
    """Favorite and ShoppingCart admin-panel."""
    list_display = ('user', 'recipe')
    list_display_links = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
