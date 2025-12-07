from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "pickup_slot", "total_amount", "created_at")
    list_filter = ("status", "pickup_slot")
    search_fields = ("id", "user__username", "user__email")
    inlines = [OrderItemInline]
