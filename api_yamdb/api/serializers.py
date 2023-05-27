from rest_framework.serializers import ModelSerializer, ValidationError

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
