from django.db import models
from django.contrib.auth.models import User
from apps.books.models import Category


class DailySalesMetric(models.Model):
    """Track daily sales metrics"""
    date = models.DateField(auto_now_add=True, unique=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    total_items_sold = models.IntegerField(default=0)
    unique_customers = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Daily Sales Metric'
        verbose_name_plural = 'Daily Sales Metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Sales for {self.date}"


class CategoryAnalytics(models.Model):
    """Analytics by book category"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='analytics')
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category Analytics'
        verbose_name_plural = 'Category Analytics'
    
    def __str__(self):
        return f"Analytics for {self.category.name}"


class UserEngagementMetric(models.Model):
    """Track user engagement"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='engagement_metric')
    total_purchases = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    wishlist_items = models.IntegerField(default=0)
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    account_age_days = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'User Engagement Metric'
        verbose_name_plural = 'User Engagement Metrics'
    
    def __str__(self):
        return f"Metrics for {self.user.username}"
