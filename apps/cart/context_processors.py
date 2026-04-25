from apps.cart.views import get_or_create_cart


def cart_context(request):
    """Add cart information to template context"""
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
        return {
            'cart': cart,
            'cart_items_count': cart.get_total_items(),
            'cart_total': float(cart.get_total_price()),
        }
    return {
        'cart': None,
        'cart_items_count': 0,
        'cart_total': 0.0,
    }
