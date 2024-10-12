from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters, viewsets, mixins
from rest_framework.decorators import action
from api.permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer, UsersSerializer,
    UpdateUsersSerializer, TokenSerializer
)
from .utils import send_verification_email, generate_verification_code


User = get_user_model()


class UserRegistrationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Регистрация пользователя"""
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        result = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if not result:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            result.code = generate_verification_code()
            result.save()
        send_verification_email(result, result.code)
        return Response(
            {'username': result.username, 'email': result.email},
            status=status.HTTP_200_OK
        )


class UserVerificationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Верификация пользователя и получение токена."""
    serializer_class = TokenSerializer

    def perform_create(self, serializer):
        return Response(serializer.validated_data)


class UsersViewSet(viewsets.ModelViewSet):
    """Пользователи"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False, methods=['get'], url_path='me',
        permission_classes=[IsAuthenticated])
    def user_information(self, request):
        """users/me"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @user_information.mapping.patch
    def user_update(self, request):
        """Обработка patch запроса /me"""
        serializer = UpdateUsersSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
