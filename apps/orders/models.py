import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PROCESSING = "processing", _("Processing")
        READY_FOR_PICKUP = "ready_for_pickup", _("Ready For Pickup")
        CUSTOMER_ARRIVED = "customer_arrived", _("Customer Arrived")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING)
    pickup_slot = models.ForeignKey(
        "curbside.PickupSlot",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Order {self.id}"

    @property
    def display_status(self) -> str:
        return self.get_status_display()

    def recalculate_total(self) -> None:
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
