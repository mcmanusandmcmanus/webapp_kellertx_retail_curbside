from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, View

from apps.orders.models import Order
from apps.users.mixins import StaffRequiredMixin

from .forms import ArrivalAlertForm


class StaffDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "curbside/staff_dashboard.html"


class StaffOrderStreamView(StaffRequiredMixin, TemplateView):
    template_name = "curbside/partials/staff_order_table.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["orders"] = (
            Order.objects.filter(
                status__in=[
                    Order.Status.PENDING,
                    Order.Status.PROCESSING,
                    Order.Status.READY_FOR_PICKUP,
                    Order.Status.CUSTOMER_ARRIVED,
                ]
            )
            .select_related("user", "pickup_slot")
            .prefetch_related("arrival_alert")
        )
        return ctx


class ArrivalAlertView(LoginRequiredMixin, View):
    form_class = ArrivalAlertForm

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"], user=request.user)
        form = self.form_class(request.POST, instance=getattr(order, "arrival_alert", None))
        if not form.is_valid():
            messages.error(request, "Unable to check in, please fix the errors.")
            return redirect("order_detail", pk=order.pk)
        alert = form.save(commit=False)
        alert.order = order
        alert.save()
        messages.success(request, "Thanks! The team has been notified that you're curbside.")
        if request.htmx:
            return render(request, "orders/partials/arrival_status.html", {"order": order})
        return redirect(reverse("order_detail", kwargs={"pk": order.pk}))
