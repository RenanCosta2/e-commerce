from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins have full access to the object
        if request.user.is_staff:
            return True
        # Regular users can only access their own profile
        return obj.id == request.user.id
