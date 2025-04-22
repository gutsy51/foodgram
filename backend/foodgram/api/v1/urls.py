from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.v1.views.users import CustomUserViewSet
from api.v1.views.recipes import IngredientViewSet, RecipeViewSet


router = SimpleRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # Part of this is redefined by `users`.
    path('auth/', include('djoser.urls.authtoken')),
]
