from django.urls import include, path
from rest_framework.routers import SimpleRouter

# from api.views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet


router = SimpleRouter()
# router.register('', SomeViewSet)
# router.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
