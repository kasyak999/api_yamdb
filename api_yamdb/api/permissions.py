from rest_framework import permissions


class IsOwnerOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Ограничение на изменение и удаление только автором и персоналом API.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Ограничение на изменение и удаление только администратором и суперюзером.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin or request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    """Проверка прав админа в списке всех пользователей"""

    def has_permission(self, request, view):
        """Проверяем имеет ли он роль администратора"""
        return request.user.is_admin or request.user.is_superuser
