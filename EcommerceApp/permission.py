from rest_framework import permissions

from EcommerceApp.models import Order


class ProductPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.seller.account == request.user

class EvaluatePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.customer.account == request.user

class PayMomoPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == 'CUSTOMER'

class CheckPaymentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return Order.objects.filter(customer__account = request.user).first()
        else:
            return False