from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.curbside.forms import ArrivalAlertForm
from apps.inventory.models import Product
from apps.curbside.services import ensure_default_pickup_slots
from apps.users.mixins import StaffRequiredMixin

from .cart import Cart
from .forms import CheckoutForm
from .models import Order
from .services import create_order_from_cart


def _cart_indicator_context(request):
    cart = Cart(request)
    return {"cart_item_count": cart.count}


class CartIndicatorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "orders/partials/cart_indicator.html", _cart_indicator_context(request))


class CartDetailView(TemplateView):
    template_name = "orders/cart_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        ctx["cart_items"] = list(cart.items())
        ctx["cart_total"] = sum(item["line_total"] for item in ctx["cart_items"])
        return ctx


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs["pk"], is_active=True)
        cart = Cart(request)
        try:
            quantity = max(1, int(request.POST.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1
        cart.add(product.id, quantity=quantity)
        messages.success(request, f"Added {product.name} to cart.")
        if request.htmx:
            return render(request, "orders/partials/cart_indicator.html", _cart_indicator_context(request))
        return redirect(request.META.get("HTTP_REFERER", reverse("catalog")))


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.remove(kwargs["pk"])
        messages.info(request, "Removed product from cart.")
        if request.htmx:
            return render(request, "orders/partials/cart_indicator.html", _cart_indicator_context(request))
        return redirect("cart_detail")


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm

    def get(self, request, *args, **kwargs):
        ensure_default_pickup_slots()
        form = self.form_class()
        cart = Cart(request)
        if cart.count == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect("catalog")
        cart_items = list(cart.items())
        cart_total = sum(item["line_total"] for item in cart_items)
        return render(
            request,
            self.template_name,
            {"form": form, "cart_items": cart_items, "cart_total": cart_total},
        )

    def post(self, request, *args, **kwargs):
        ensure_default_pickup_slots()
        cart = Cart(request)
        form = self.form_class(request.POST)
        cart_items = list(cart.items())
        cart_total = sum(item["line_total"] for item in cart_items)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "cart_items": cart_items, "cart_total": cart_total},
            )
        try:
            order = create_order_from_cart(
                cart=cart,
                user=request.user,
                pickup_slot=form.cleaned_data["pickup_slot"],
                notes=form.cleaned_data.get("notes", ""),
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                self.template_name,
                {"form": form, "cart_items": cart_items, "cart_total": cart_total},
            )
        messages.success(request, "Order placed successfully.")
        return redirect("order_detail", pk=order.pk)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.request.user.orders.select_related("pickup_slot")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return self.request.user.orders.select_related("pickup_slot").prefetch_related("items__product")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["arrival_form"] = ArrivalAlertForm(instance=getattr(self.object, "arrival_alert", None))
        return ctx


class OrderStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        new_status = request.POST.get("status")
        if new_status not in Order.Status.values:
            messages.error(request, "Invalid status.")
            return redirect("staff_dashboard")
        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Order updated.")
        if request.htmx:
            from apps.curbside.views import StaffOrderStreamView

            return StaffOrderStreamView.as_view()(request)
        return redirect("staff_dashboard")
