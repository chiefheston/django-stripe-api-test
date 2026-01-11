from django.contrib import admin
from modules.orders.models import (
    Discount,
    Order,
    OrderDiscount,
    OrderLine,
    OrderTax,
    Tax,
)

admin.site.register([Tax, Discount])


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0


class OrderTaxInline(admin.TabularInline):
    model = OrderTax
    extra = 0
    max_num = 1


class OrderDiscountInline(admin.TabularInline):
    model = OrderDiscount
    extra = 0
    max_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline, OrderTaxInline, OrderDiscountInline]

    readonly_fields = ("created_at",)
    list_display = ("id", "status", "created_at")
