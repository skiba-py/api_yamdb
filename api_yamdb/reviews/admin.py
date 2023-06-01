from django.contrib import admin
from django.db.models import Avg

from .models import Category, Genre, GenreTitle, Title

LIST_PER_PAGE = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'year', 'category')

    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""
        return '\n'.join((genre.name for genre in object.genre.all()))

    get_genre.short_description = 'Жанр/ы произведения'

    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), 1)

    get_rating.short_description = 'Рейтинг'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Класс настройки соответствия жанров и произведений."""

    list_display = (
        'pk',
        'genre',
        'title'
    )
    empty_value_display = '-пусто-'
    list_filter = ('genre',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('title',)
