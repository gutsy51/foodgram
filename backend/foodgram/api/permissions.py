from rest_framework import permissions


class IsObjAuthorOrReadOnly(permissions.BasePermission):
    """Grant access if user is object author OR method is safe."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user and obj.author == request.user))
