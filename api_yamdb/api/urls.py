from django.urls import include, path
from rest_framework import routers

from .views import UserCreateViewSet, UserGetTokenViewSet, UserViewSet

router = routers.DefaultRouter()
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
