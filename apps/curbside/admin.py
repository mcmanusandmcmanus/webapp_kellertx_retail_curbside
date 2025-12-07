from django.contrib import admin

from .models import ArrivalAlert, PickupSlot


@admin.register(PickupSlot)
class PickupSlotAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "max_orders")
    ordering = ("start_time",)


@admin.register(ArrivalAlert)
class ArrivalAlertAdmin(admin.ModelAdmin):
    list_display = ("order", "vehicle_desc", "parking_spot", "arrived_at")
