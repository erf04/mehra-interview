from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .models import Product

class IsProductOwner(BasePermission):
    """
    Custom permission to check if the authenticated user is the owner of the product.
    """

    def has_object_permission(self, request:Request, view, obj:Product) -> bool:
        # Check if the `created_by` field matches the authenticated user
        return obj.created_by == request.user
