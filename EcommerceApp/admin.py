from django.contrib import admin
from django.template.response import TemplateResponse
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from .models import *
from django.contrib.auth.admin import UserAdmin as UserSite
from django.contrib.auth.models import Permission, Group
from django.urls import path

class EcommerceAdminSite(admin.AdminSite):

    site_header = 'Trang quản trị hệ thống bán hàng trực tuyến'

    def get_urls(self):
        return [
            path('statistic/', self.statistic_view)
        ] + super().get_urls()

    def statistic_view(self, request):
        return TemplateResponse(request, 'admin/statistic.html',)

class OrderDetailInline(NestedStackedInline):
    model = OrderDetail

class PaymentInlineAdmin(NestedStackedInline):
    model = Payment

class OrderAdmin(NestedModelAdmin):

    list_filter =  ['created_date', 'shipped_date', 'status']
    search_fields = ['customer', 'seller']
    inlines = [OrderDetailInline, PaymentInlineAdmin]

    add_fieldsets = (
        ("User Login", {'fields': ('username', 'password1', 'password2')}),
        ("Permission", {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ("Information", {'fields': ('email', 'avatar', 'first_name', 'last_name')})
    )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Order.objects.all()

        if request.user.role == 'SELLER':
            return Order.objects.filter(seller__account = request.user)
        return Order.objects.none()

class AccountAdmin(UserSite):

    fieldsets = (
        ("User Login", {'fields': ('username',)}),
        ("Permission", {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ("Information", {'fields': ('email', 'avatar', 'first_name', 'last_name')}),
    )

    add_fieldsets = (
        ("User Login", {'fields': ('username', 'password1', 'password2')}),
        ("Permission", {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ("Information", {'fields': ('email', 'avatar', 'first_name', 'last_name')})
    )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Account.objects.all()

        if request.user.role == 'SELLER':
            return Account.objects.filter(id = request.user.id)
        return Account.objects.none()


class ProductDetailInline(NestedStackedInline):
    model = ProductDetail

class ProductAdmin(NestedModelAdmin):
    inlines = [ProductDetailInline]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()

        if request.user.role == 'SELLER':
            return Product.objects.filter(seller__account = request.user)
        return Product.objects.none()

class EvaluateAdmin(admin.ModelAdmin):

    list_filter = ['rate', 'product']

class RevenueAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Revenue.objects.all()

        if request.user.role == 'SELLER':
            return Revenue.objects.filter(order__seller = request.user)
        return Revenue.objects.none()

class SellerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Seller.objects.all()

        if request.user.role == 'SELLER':
            return Seller.objects.filter(account = request.user)
        return Seller.objects.none()

admin_site = EcommerceAdminSite(name= "myadmin")

admin_site.register(Account,AccountAdmin)
admin_site.register(Customer)
admin_site.register(Seller, SellerAdmin)
admin_site.register(Order,OrderAdmin)
admin_site.register(Evaluate,EvaluateAdmin)
admin_site.register(Product,ProductAdmin)
admin_site.register(Category)
admin_site.register(Brand)
admin_site.register(Group)
admin_site.register(Permission)
admin_site.register(Classification)