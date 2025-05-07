from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, IngredientViewSet, RecipeViewSet


router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
