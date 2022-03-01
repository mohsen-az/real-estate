from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.user == request.user)
