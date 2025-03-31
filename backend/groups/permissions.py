from rest_framework.permissions import BasePermission

class IsGroupAdmin(BasePermission):
    """
    Custom permission to only allow group creators (admins) to edit or delete.
    """
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
