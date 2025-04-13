from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from users.admin import CustomUserAdmin

from recipes.models import (Ingredient, RecipeIngredient, Recipe,
                            Favorite, ShoppingCart)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)



class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    verbose_name = _('Ингредиент рецепта')
    verbose_name_plural = _('Ингредиенты рецепта')
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


class UserRecipeAdminMixin:
    """Base User-Recipe relation admin-panel."""
    list_display = ('user', 'recipe')
    list_display_links = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')

@admin.register(Favorite)
class FavoriteAdmin(UserRecipeAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(UserRecipeAdminMixin, admin.ModelAdmin):
    pass

# Expand the user admin-panel.
admin.site.unregister(CustomUser)

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    verbose_name = _('Избранный рецепт')
    verbose_name_plural = _('Избранное')

class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0
    verbose_name = _('Рецепт в корзине')
    verbose_name_plural = _('Корзина покупок')

@admin.register(CustomUser)
class CustomUserAdmin(CustomUserAdmin):
    inlines = CustomUserAdmin.inlines + [FavoriteInline, ShoppingCartInline]
