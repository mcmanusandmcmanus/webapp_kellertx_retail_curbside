from datetime import datetime, time, timedelta

from django.utils import timezone

from .models import PickupSlot


def ensure_default_pickup_slots(days_ahead: int = 2, interval_minutes: int = 60, capacity: int = 5) -> int:
    """
    Create pickup slots for the next `days_ahead` days if none exist.

    Returns number of slots created.
    """
    tz = timezone.get_current_timezone()
    now = timezone.now()
    created = 0
    for day in range(days_ahead):
        date = (now + timedelta(days=day)).date()
        start_dt = timezone.make_aware(datetime.combine(date, time(hour=10)), tz)
        end_dt = timezone.make_aware(datetime.combine(date, time(hour=18)), tz)
        slot_start = start_dt
        while slot_start < end_dt:
            slot_end = slot_start + timedelta(minutes=interval_minutes)
            exists = PickupSlot.objects.filter(start_time=slot_start, end_time=slot_end).exists()
            if not exists:
                PickupSlot.objects.create(
                    start_time=slot_start,
                    end_time=slot_end,
                    max_orders=capacity,
                )
                created += 1
            slot_start = slot_end
    return created
