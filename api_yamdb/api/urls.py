from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = DefaultRouter()
router.register('title', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genre', GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(router.urls)),
]