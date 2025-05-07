from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import (User, Subscription, Ingredient, Recipe,
                     RecipeIngredient, Favorite, ShoppingCart)


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


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [FollowerInline, SubscriptionInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')
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


# Recipes.
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    verbose_name = 'Ингредиент рецепта'
    verbose_name_plural = 'Ингредиенты рецепта'
    fields = ('ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline,]
    list_display = ('name', 'author', 'cooking_time', 'created_at')
    list_display_links = ('name',)
    list_filter = ('name', 'author', 'cooking_time')
    search_fields = ('name', 'ingredients__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Favorite, ShoppingCart)
class UserRecipeAdmin(admin.ModelAdmin):
    """Favorite and ShoppingCart admin-panel."""
    list_display = ('user', 'recipe')
    list_display_links = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


# Expand the user admin-panel.
admin.site.unregister(User)


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
class UserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [FavoriteInline, ShoppingCartInline]
