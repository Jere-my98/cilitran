from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow the owner of the review or an admin to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin users or the user who wrote the review to edit or delete
        return obj.user == request.user or request.user.is_staff

class IsSelfOrAdmin(BasePermission):
    """
    Custom permission to allow users to edit their own profile or admins to edit any profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
