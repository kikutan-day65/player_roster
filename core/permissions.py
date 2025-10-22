from rest_framework import permissions


class IsAuthenticatedOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser
