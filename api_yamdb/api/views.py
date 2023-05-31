from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Title
from api.serializer import CategorySerializer, GenreSerializer, TitleSerializer



class TitleViewSet(viewsets.ModelViewSet):
    '''Произведения.'''
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    '''Категории.'''
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    '''Жанры'''
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'