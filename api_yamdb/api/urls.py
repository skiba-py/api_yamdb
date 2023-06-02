from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

from .views import (CommentsViewSet, ReviewsViewSet, UserCreateViewSet,
                    UserGetTokenViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentsViewSet,
    basename="comments",
)


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
