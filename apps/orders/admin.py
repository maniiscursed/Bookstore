from django.contrib import admin
from .models import Order, OrderItem, Payment, Receipt


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'payment_status', 'final_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'payment_method')
    search_fields = ('order_id', 'user__username', 'user__email')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Order Info', {'fields': ('order_id', 'user', 'status', 'created_at', 'updated_at')}),
        ('Pricing', {'fields': ('total_amount', 'discount_amount', 'tax_amount', 'final_amount')}),
        ('Shipping', {'fields': ('shipping_address', 'delivered_at')}),
        ('Payment', {'fields': ('payment_method', 'payment_status')}),
        ('Notes', {'fields': ('notes',), 'classes': ('collapse',)}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price_at_purchase')
    search_fields = ('order__order_id', 'book__title')
    list_filter = ('order__created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status', 'payment_date')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('order__order_id', 'transaction_id')
    readonly_fields = ('payment_date',)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'order', 'total', 'generated_at')
    search_fields = ('receipt_number', 'order__order_id')
    readonly_fields = ('generated_at',)
