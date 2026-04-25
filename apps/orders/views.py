from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from apps.cart.views import get_or_create_cart
from apps.accounts.models import Address
from .models import Order, OrderItem, Payment, Receipt
from .forms import CheckoutForm
import uuid


@login_required(login_url='accounts:login')
def checkout(request):
    """Order checkout view"""
    cart = get_or_create_cart(request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('books:book_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return process_order(request, form, cart)
    else:
        form = CheckoutForm()
    
    # Get user addresses for selection
    user_addresses = request.user.addresses.all()
    
    context = {
        'form': form,
        'cart': cart,
        'user_addresses': user_addresses,
    }
    return render(request, 'orders/checkout.html', context)


@transaction.atomic
def process_order(request, form, cart):
    """Process the order"""
    user = request.user
    
    # Create order
    total_amount = cart.get_total_price()
    discount_amount = Decimal('0')
    tax_amount = total_amount * Decimal('0.05')  # 5% tax
    final_amount = total_amount + tax_amount - discount_amount
    
    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        final_amount=final_amount,
        payment_method=form.cleaned_data['payment_method'],
        notes=form.cleaned_data.get('notes', '')
    )
    
    # Add order items from cart
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            book=cart_item.book,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.book.price,
            discount_percentage=cart_item.book.discount_percentage
        )
        # Reduce book stock
        cart_item.book.stock -= cart_item.quantity
        cart_item.book.save()
    
    # Create payment record
    Payment.objects.create(
        order=order,
        payment_method=form.cleaned_data['payment_method'],
        amount=final_amount,
        transaction_id=f"TXN-{order.order_id}-{timezone.now().timestamp()}",
        status='completed'
    )
    
    # Create receipt
    Receipt.objects.create(
        order=order,
        receipt_number=f"RCP-{order.order_id}",
        subtotal=total_amount,
        discount=discount_amount,
        tax=tax_amount,
        total=final_amount
    )
    
    # Clear cart
    cart.items.all().delete()
    
    messages.success(request, 'Order placed successfully!')
    return redirect('orders:order_confirmation', order_id=order.id)


@login_required(login_url='accounts:login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/confirmation.html', context)


@login_required(login_url='accounts:login')
def order_list(request):
    """List user orders"""
    orders = request.user.orders.all()
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required(login_url='accounts:login')
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='accounts:login')
def receipt_view(request, order_id):
    """View order receipt"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    receipt = get_object_or_404(Receipt, order=order)
    
    context = {
        'order': order,
        'receipt': receipt,
    }
    return render(request, 'orders/receipt.html', context)
