from django.db import models
from django.contrib.auth.models import User
from apps.books.models import Book


class Cart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum([item.quantity for item in self.items.all()])
    
    def get_total_price(self):
        """Get total price of all items"""
        return sum([item.get_item_total() for item in self.items.all()])
    
    def get_total_discount(self):
        """Get total discount amount"""
        discount = 0
        for item in self.items.all():
            discount += item.book.discount_percentage * item.quantity
        return discount
    
    def get_tax(self):
        """Get tax amount (5% of total)"""
        total = self.get_total_price()
        from decimal import Decimal
        return total * Decimal('0.05')
    
    def get_total_with_tax(self):
        """Get grand total including tax"""
        total = self.get_total_price()
        from decimal import Decimal
        return total * Decimal('1.05')


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'book']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
    def __str__(self):
        return f"{self.book.title} x {self.quantity}"
    
    def get_item_total(self):
        """Get total price for this item"""
        return self.book.get_discounted_price() * self.quantity
