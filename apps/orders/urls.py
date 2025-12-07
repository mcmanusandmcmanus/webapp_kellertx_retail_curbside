from django.urls import path

from .views import (
    CartAddView,
    CartDetailView,
    CartIndicatorView,
    CartRemoveView,
    CheckoutView,
    OrderStatusUpdateView,
    OrderDetailView,
    OrderListView,
)

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
    path("cart/indicator/", CartIndicatorView.as_view(), name="cart_indicator"),
    path("cart/add/<int:pk>/", CartAddView.as_view(), name="cart_add"),
    path("cart/remove/<int:pk>/", CartRemoveView.as_view(), name="cart_remove"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<uuid:pk>/status/", OrderStatusUpdateView.as_view(), name="order_status_update"),
]
