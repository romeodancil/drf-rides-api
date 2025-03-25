from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        print('request.user', request.user)
        return getattr(request.user, "role", "") == "admin"
