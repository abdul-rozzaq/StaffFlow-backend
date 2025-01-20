from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CompanyIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.company)


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)


class CompanyOrRequestUser(BasePermission):

    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser) or request.company
