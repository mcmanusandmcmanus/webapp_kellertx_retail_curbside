from __future__ import annotations

from decimal import Decimal

from django.http import HttpRequest

from apps.inventory.models import Product


class Cart:
    session_key = "cart"

    def __init__(self, request: HttpRequest):
        self.session = request.session
        self.data = self.session.get(self.session_key, {})

    def add(self, product_id: int, quantity: int = 1) -> None:
        product_id = str(product_id)
        current_qty = self.data.get(product_id, 0)
        self.data[product_id] = current_qty + quantity
        self._save()

    def set(self, product_id: int, quantity: int) -> None:
        product_id = str(product_id)
        if quantity <= 0:
            self.data.pop(product_id, None)
        else:
            self.data[product_id] = quantity
        self._save()

    def remove(self, product_id: int) -> None:
        product_id = str(product_id)
        if product_id in self.data:
            del self.data[product_id]
            self._save()

    def clear(self) -> None:
        self.session[self.session_key] = {}
        self.session.modified = True
        self.data = {}

    @property
    def count(self) -> int:
        return sum(self.data.values())

    def items(self):
        product_ids = [int(pk) for pk in self.data.keys()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}
        for product_id, qty in self.data.items():
            product = product_map.get(product_id)
            if not product:
                continue
            yield {
                "product": product,
                "quantity": qty,
                "line_total": product.price * qty,
            }

    def total(self) -> Decimal:
        return sum(item["line_total"] for item in self.items())

    def _save(self):
        self.session[self.session_key] = self.data
        self.session.modified = True
