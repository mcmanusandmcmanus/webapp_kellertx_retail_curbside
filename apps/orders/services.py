from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from apps.inventory.models import Product

from .cart import Cart
from .models import Order, OrderItem


def create_order_from_cart(*, cart: Cart, user, pickup_slot, notes: str = "") -> Order:
    if cart.count == 0:
        raise ValueError("Cart is empty.")

    pickup_slot.reserve_order()

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            pickup_slot=pickup_slot,
            notes=notes,
        )
        items = []
        for entry in cart.items():
            product: Product = entry["product"]
            quantity = entry["quantity"]
            if product.stock_quantity < quantity:
                raise ValueError(f"Not enough stock for {product.name}.")
            product.stock_quantity -= quantity
            product.save(update_fields=["stock_quantity"])
            items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                )
            )
        OrderItem.objects.bulk_create(items)
        total = sum(item.unit_price * item.quantity for item in items)
        order.total_amount = total.quantize(Decimal("0.01"))
        order.save(update_fields=["total_amount"])

    cart.clear()
    return order
