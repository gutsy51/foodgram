from rest_framework import permissions


class IsObjAuthorOrReadOnly(permissions.BasePermission):
    """Grant access if user is object author OR method is safe.

    Rules:
    1. Any safe method (GET, HEAD, OPTIONS) can be accessed by any user;
    2. Only authenticated user can POST objects;
    3. Only object author can PUT, PATCH, DELETE objects.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and obj.author == request.user
