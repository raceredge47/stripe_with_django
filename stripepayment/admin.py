from django.contrib import admin
from .models import Product, OrderDetail
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'stripe_payment_intent', 'has_paid']


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
