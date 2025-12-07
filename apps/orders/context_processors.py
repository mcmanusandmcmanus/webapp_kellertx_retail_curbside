from .cart import Cart


def cart_summary(request):
    if not hasattr(request, "session"):
        return {}
    cart = Cart(request)
    return {"cart_item_count": cart.count}
