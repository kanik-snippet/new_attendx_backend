from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Custom permission to allow only Super Admins to access certain APIs.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'

class IsSuperAdminOrSubAdmin(BasePermission):
    """
    Custom permission to allow only Super Admin or Sub Admin to access the API.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["super_admin", "sub_admin"]