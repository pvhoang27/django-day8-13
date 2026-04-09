from django.conf import settings
from rest_framework import permissions


class HasInternalApiKey(permissions.BasePermission):
    message = "Invalid internal API key."

    def has_permission(self, request, view):
        api_key = request.headers.get("X-INTERNAL-API-KEY", "")
        return api_key and api_key == settings.INVENTORY_INTERNAL_API_KEY
