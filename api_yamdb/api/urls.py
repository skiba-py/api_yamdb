from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet, 
                       CommentsViewSet, ReviewsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('title', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genre', GenreViewSet, basename='genre')
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentsViewSet,
    basename="comments",
)


urlpatterns = [
    path('v1/', include(router.urls)),
]