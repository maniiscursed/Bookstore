from django.db import models
from django.contrib.auth.models import User
from apps.books.models import Book
from datetime import datetime


class UserRating(models.Model):
    """User rating and interaction tracking for recommendations"""
    INTERACTION_CHOICES = [
        ('view', 'View'),
        ('wishlist', 'Wishlist'),
        ('purchase', 'Purchase'),
        ('review', 'Review'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(default=0, help_text='0-5 stars')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_CHOICES)
    interaction_weight = models.FloatField(default=1.0, help_text='Weight for collaborative filtering')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book', 'interaction_type']
        verbose_name = 'User Rating'
        verbose_name_plural = 'User Ratings'
        indexes = [
            models.Index(fields=['user', 'book']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.interaction_type})"


class RecommendationModel(models.Model):
    """Store trained recommendation models"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_type = models.CharField(max_length=50, default='matrix_factorization')
    n_factors = models.IntegerField(default=10)
    n_epochs = models.IntegerField(default=100)
    learning_rate = models.FloatField(default=0.01)
    regularization = models.FloatField(default=0.01)
    is_active = models.BooleanField(default=True)
    accuracy = models.FloatField(null=True, blank=True)
    trained_at = models.DateTimeField(auto_now_add=True)
    last_retrained = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Recommendation Model'
        verbose_name_plural = 'Recommendation Models'
    
    def __str__(self):
        return self.name


class UserSimilarity(models.Model):
    """Precomputed user similarity matrix"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similarities_from')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similarities_to')
    similarity_score = models.FloatField(help_text='Cosine similarity score (0-1)')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user1', 'user2']
        verbose_name = 'User Similarity'
        verbose_name_plural = 'User Similarities'
    
    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username}: {self.similarity_score:.2f}"


class RecommendedBook(models.Model):
    """Recommended books for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommended_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommendation_score = models.FloatField(help_text='Predicted rating 0-5')
    recommendation_type = models.CharField(max_length=50, default='collaborative_filtering')
    reason = models.CharField(max_length=255, blank=True)
    is_clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
        verbose_name = 'Recommended Book'
        verbose_name_plural = 'Recommended Books'
        ordering = ['-recommendation_score']
    
    def __str__(self):
        return f"Recommend {self.book.title} to {self.user.username} ({self.recommendation_score:.2f})"
