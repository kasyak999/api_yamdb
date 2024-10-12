from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet, UserVerificationViewSet,
    UsersViewSet)

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'auth/token', UserVerificationViewSet, basename='token')
router.register(
    r'auth/signup', UserRegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
]
