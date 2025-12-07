from django.db import models
from django.db.models import Count, F, Q
from django.utils import timezone


class PickupSlotQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(start_time__gte=timezone.now()).order_by("start_time")

    def with_capacity(self):
        from apps.orders.models import Order

        return self.annotate(
            order_total=Count(
                "orders",
                filter=~Q(orders__status=Order.Status.CANCELLED),
            )
        ).filter(order_total__lt=F("max_orders"))


class PickupSlotManager(models.Manager):
    def get_queryset(self):
        return PickupSlotQuerySet(self.model, using=self._db)

    def upcoming(self):
        return self.get_queryset().upcoming().with_capacity()


class PickupSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_orders = models.PositiveIntegerField(default=5)

    objects = PickupSlotManager()

    class Meta:
        ordering = ("start_time",)

    def __str__(self):
        return f"{self.start_time:%b %d %I:%M %p} - {self.end_time:%I:%M %p}"

    @property
    def remaining_capacity(self) -> int:
        from apps.orders.models import Order

        placed = self.orders.exclude(status=Order.Status.CANCELLED).count()
        return max(self.max_orders - placed, 0)

    @property
    def is_full(self) -> bool:
        return self.remaining_capacity <= 0

    def reserve_order(self) -> None:
        if self.is_full:
            raise ValueError("Pickup slot is full.")


class ArrivalAlert(models.Model):
    order = models.OneToOneField("orders.Order", related_name="arrival_alert", on_delete=models.CASCADE)
    vehicle_desc = models.CharField(max_length=120)
    parking_spot = models.CharField(max_length=30, blank=True)
    arrived_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-arrived_at",)

    def __str__(self) -> str:
        return f"Arrival alert for {self.order_id}"

    def save(self, *args, **kwargs):
        creating = self.pk is None
        result = super().save(*args, **kwargs)
        if creating:
            order = self.order
            order.status = order.Status.CUSTOMER_ARRIVED
            order.save(update_fields=["status", "updated_at"])
        return result
