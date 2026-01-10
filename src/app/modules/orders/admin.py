from django.contrib import admin
from modules.orders.models import Order, OrderLine


class OrderItemInline(admin.TabularInline):
    model = OrderLine
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # TODO: добавить юзкейсы
    inlines = [OrderItemInline]

    readonly_fields = ("created_at",)
    list_display = ("id", "status", "created_at")
