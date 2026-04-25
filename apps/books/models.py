from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from PIL import Image
from decimal import Decimal
import os


class Category(models.Model):
    """Book category model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    isbn = models.CharField(max_length=20, unique=True)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=255)
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, default='English')
    source_url = models.URLField(blank=True, null=True, max_length=500)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.IntegerField(default=0)
    is_bestseller = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_discounted_price(self):
        """Calculate discounted price"""
        if self.discount_percentage:
            discount = self.price * Decimal(self.discount_percentage) / Decimal(100)
            return self.price - discount
        return self.price
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize cover image
        if self.cover_image:
            img = Image.open(self.cover_image.path)
            if img.height > 400 or img.width > 300:
                output_size = (300, 400)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                img.save(self.cover_image.path)


class BookReview(models.Model):
    """Book review and rating model"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    review_text = models.TextField()
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['book', 'user']
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for '{self.book.title}' by {self.user.username}"


class WishList(models.Model):
    """User wishlist model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    books = models.ManyToManyField(Book, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist"
