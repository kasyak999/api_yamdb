from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from users.models import MAX_LENGT_EMAIL, MAX_LENGT_USERNAME
from .validators import validate_username


User = get_user_model()
PATTERN = r'^[\w.@+-]+\Z'


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        """Проверка валидности confirmation_code."""
        user = get_object_or_404(User, username=attrs.get("username"))
        if attrs.get("confirmation_code") == str(user.code):
            token = AccessToken.for_user(user)
            return {"token": str(token)}
        raise serializers.ValidationError(
            {"confirmation_code": "Неверный код подтверждения"})


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    email = serializers.EmailField(
        max_length=MAX_LENGT_EMAIL,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Этот email уже используется")]
    )
    username = serializers.CharField(
        max_length=MAX_LENGT_USERNAME,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Этот username уже используется"), validate_username]
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class UsersSerializer(UserRegistrationSerializer):
    """Сериализатор для /me"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UpdateUsersSerializer(UserRegistrationSerializer):
    """Сериализатор для обновляем пользователя"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio',
        )
