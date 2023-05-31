from rest_framework.serializers import ModelSerializer, ValidationError
from reviews.models import Comment, Review

from users.models import User


class UserCreateSerializer(ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Валидация создания пользователя"""
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'Пользователь с таким логином уже существует'
            )
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует'
            )
        if data.get('username') == 'me':
            raise ValidationError('Используйте другое имя!')
        return data


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )

    @staticmethod
    def validate_username(username):
        if username in 'me':
            raise ValidationError(
                'Используйте другое имя!'
            )
        return username

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
