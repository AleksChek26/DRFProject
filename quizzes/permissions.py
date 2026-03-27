from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта или администратору.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        # Для теста проверяем владельца материала или самого теста (они должны совпадать)
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        # Для материала проверяем владельца материала
        if hasattr(obj, 'material'):
            return obj.material.owner == request.user


class CanTakeTest(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Студенты могут проходить тест только если они не владельцы (не преподаватели)
        return request.user.role == 'student'