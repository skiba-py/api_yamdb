from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
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


class CategorySerializer(serializers.ModelSerializer):
    '''Сериалайзер категорий.'''

    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    '''Сериалайзер жанров.'''

    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = 'slug'


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'rating',
            'category',
            'genre',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre')

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleGETSerializer(title)
        return serializer.data


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate_score(self, score):
        if not (0 < score <= 10):
            raise serializers.ValidationError(
                'Рейтинг должен быть в интервале от 1 до 10.'
            )
        return score

    def validate(self, data):
        request = self.context.get('request')
        title = self.context.get('view').kwargs.get('title_id')
        review_exists = Review.objects.filter(title=title,
                                              author=request.user).exists()
        is_post_request = request.method == 'POST'
        if review_exists and is_post_request:
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв!'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
