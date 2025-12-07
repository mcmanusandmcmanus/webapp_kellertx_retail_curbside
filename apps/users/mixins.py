from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest


class StaffRequiredMixin(UserPassesTestMixin):
    """Restrict access to staff or manager accounts."""

    def test_func(self) -> bool:
        request: HttpRequest = self.request
        user = request.user
        return bool(user.is_authenticated and getattr(user, "is_staff_portal_user", False))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied("You do not have access to the staff portal.")
