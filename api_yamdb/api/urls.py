from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserCreateViewSet, UserGetTokenViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('title', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genre', GenreViewSet, basename='genre')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path(
        'v1/auth/signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        UserGetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
    path('v1/', include(router.urls))
]
