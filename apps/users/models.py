from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with role-aware behaviour."""

    class Types(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        STAFF = "staff", _("Staff")
        MANAGER = "manager", _("Manager")

    type = models.CharField(
        max_length=20,
        choices=Types.choices,
        default=Types.CUSTOMER,
    )
    phone_number = models.CharField(max_length=20, blank=True)

    @property
    def is_staff_portal_user(self) -> bool:
        return self.type in {self.Types.STAFF, self.Types.MANAGER}

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username}"
