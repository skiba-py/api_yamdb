from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    '''Сериалайзер пользователей.'''

    class Meta:
        model = User
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    '''Сериалайзер произведений.'''
    genre = serializers.SlugRelatedField(
        slug_field='genre',
        queryset=Genre.objects.all(),
        meny=True,
    )

    category = serializers.SlugRelatedField(
        slug_field='category',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''Сериалайзер категорий.'''

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    '''Сериалайзер жанров.'''

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'