from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Publisher)
# admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(Order)
admin.site.register(OrderItem)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
@admin.register(Order)
class CartAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


# Register your models here.
