from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from apps.books.models import Book
from .models import Cart, CartItem


def get_or_create_cart(user):
    """Get or create cart for user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required(login_url='accounts:login')
def cart_view(request):
    """Display shopping cart"""
    cart = get_or_create_cart(request.user)
    
    context = {
        'cart': cart,
        'items': cart.items.all(),
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def add_to_cart(request, book_id):
    """Add book to cart"""
    book = get_object_or_404(Book, id=book_id)
    cart = get_or_create_cart(request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check stock
    if quantity > book.stock:
        messages.error(request, f'Only {book.stock} copies available.')
        return redirect('books:book_detail', book_id=book.id)
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > book.stock:
            messages.error(request, f'Only {book.stock} copies available.')
            cart_item.quantity -= quantity
            cart_item.save()
            return redirect('books:book_detail', book_id=book.id)
        cart_item.save()
    
    messages.success(request, f'Added "{book.title}" to cart.')
    return redirect('cart:cart_view')


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update quantity of cart item"""
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        item.delete()
        messages.success(request, 'Item removed from cart.')
    else:
        if quantity > item.book.stock:
            messages.error(request, f'Only {item.book.stock} copies available.')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Cart updated.')
    
    return redirect('cart:cart_view')


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    book_title = item.book.title
    item.delete()
    messages.success(request, f'Removed "{book_title}" from cart.')
    return redirect('cart:cart_view')


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('cart:cart_view')


def context_processor(request):
    """Add cart data to context"""
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
        return {
            'cart': cart,
            'cart_total_items': cart.get_total_items(),
        }
    return {}


@login_required(login_url='accounts:login')
@require_http_methods(["GET"])
def cart_api_count(request):
    """API endpoint for cart item count"""
    cart = get_or_create_cart(request.user)
    return JsonResponse({
        'count': cart.get_total_items(),
        'total': float(cart.get_total_price())
    })
