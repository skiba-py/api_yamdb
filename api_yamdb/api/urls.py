from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, UserCreateViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router.urls))
]
