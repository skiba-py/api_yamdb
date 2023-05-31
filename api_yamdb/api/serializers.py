from rest_framework import serializers
from reviews.models import Category, Genre, Title
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Валидация создания пользователя"""
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким логином уже существует'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError('Используйте другое имя!')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )

    @staticmethod
    def validate_username(username):
        if username in 'me':
            raise serializers.ValidationError(
                'Используйте другое имя!'
            )
        return username

    def validate_role(self, role):
        """Запрещает пользователям изменять себе роль."""
        try:
            if self.instance.role != 'admin':
                return self.instance.role
            return role
        except AttributeError:
            return role


class UserGetTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class TitleSerializer(serializers.ModelSerializer):
    '''Сериалайзер произведений.'''
    genre = serializers.SlugRelatedField(
        slug_field='genre',
        queryset=Genre.objects.all(),
        many=True,
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
