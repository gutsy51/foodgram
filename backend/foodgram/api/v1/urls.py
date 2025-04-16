from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.v1.views.users import CustomUserViewSet


router = SimpleRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # Part of this is redefined by `users`.
    path('auth/', include('djoser.urls.authtoken')),
]
