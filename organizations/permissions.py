from rest_framework.permissions import BasePermission, IsAuthenticated

class VerifiedEmailPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_email_verified