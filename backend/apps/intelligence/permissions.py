"""
Permissions for WorthIQ AI Intelligence Endpoints.
Ensures strict ownership isolation across user predictions and roadmaps.
"""

from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """Allows access only to the object owner or staff administrators."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return hasattr(obj, 'user') and obj.user == request.user
