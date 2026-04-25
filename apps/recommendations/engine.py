"""
Collaborative Filtering Recommendation Engine
Uses Matrix Factorization with SVD to predict user preferences
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.models import User
from apps.books.models import Book
from .models import UserRating, UserSimilarity, RecommendedBook


class CollaborativeFilteringEngine:
    """Matrix Factorization based collaborative filtering"""
    
    def __init__(self, n_factors=10, n_epochs=100, learning_rate=0.01, regularization=0.01):
        """
        Initialize the recommendation engine
        
        Args:
            n_factors: Number of latent factors
            n_epochs: Number of training epochs
            learning_rate: Learning rate for gradient descent
            regularization: Regularization parameter (lambda)
        """
        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.user_factors = None
        self.book_factors = None
        self.user_map = None
        self.book_map = None
    
    def build_rating_matrix(self):
        """
        Build user-item rating matrix from interactions in database
        
        Returns:
            DataFrame with users as rows and books as columns
        """
        ratings = UserRating.objects.all().values('user_id', 'book_id', 'rating', 'interaction_weight')
        
        if not ratings.exists():
            return None
        
        df = pd.DataFrame(ratings)
        
        # Weight ratings by interaction type
        # Purchases are more valuable than views
        weight_map = {
            'view': 0.5,
            'wishlist': 1.5,
            'purchase': 3.0,
            'review': 2.5,
        }
        
        # Create weighted ratings
        df['weighted_rating'] = df.apply(
            lambda row: row['rating'] * weight_map.get(row.get('interaction_type'), 1.0),
            axis=1
        )
        
        # Create rating matrix
        rating_matrix = df.pivot_table(
            index='user_id',
            columns='book_id',
            values='weighted_rating',
            fill_value=0
        )
        
        return rating_matrix
    
    def train(self):
        """Train the recommendation model using NMF"""
        rating_matrix = self.build_rating_matrix()
        
        if rating_matrix is None or rating_matrix.size == 0:
            return False
        
        try:
            # Use NMF for matrix factorization
            nmf = NMF(
                n_components=self.n_factors,
                init='random',
                max_iter=self.n_epochs,
                random_state=42,
                alpha_W=self.regularization,
                alpha_H=self.regularization
            )
            
            # Fit model
            self.user_factors = nmf.fit_transform(rating_matrix)
            self.book_factors = nmf.components_.T
            
            # Store mappings
            self.user_map = {user_id: idx for idx, user_id in enumerate(rating_matrix.index)}
            self.book_map = {book_id: idx for idx, book_id in enumerate(rating_matrix.columns)}
            
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict_rating(self, user_id, book_id):
        """
        Predict rating for a user-book pair
        
        Args:
            user_id: User ID
            book_id: Book ID
            
        Returns:
            Predicted rating (0-5)
        """
        if self.user_factors is None or self.book_factors is None:
            return 0.0
        
        if user_id not in self.user_map or book_id not in self.book_map:
            return 0.0
        
        user_idx = self.user_map[user_id]
        book_idx = self.book_map[book_id]
        
        # Calculate dot product
        predicted_rating = np.dot(self.user_factors[user_idx], self.book_factors[book_idx])
        
        # Clamp to [0, 5]
        return max(0, min(5, predicted_rating))
    
    def get_recommendations(self, user_id, n_recommendations=5, exclude_purchased=True):
        """
        Get recommendations for a user
        
        Args:
            user_id: User ID
            n_recommendations: Number of recommendations
            exclude_purchased: Whether to exclude already purchased books
            
        Returns:
            List of (book_id, predicted_rating) tuples
        """
        if self.user_factors is None:
            return []
        
        if user_id not in self.user_map:
            # User hasn't rated any books yet
            # Return popular books
            return self.get_popular_books(n_recommendations)
        
        predictions = []
        
        # Get all books
        all_books = set(self.book_map.keys())
        
        # Exclude already rated books
        user_rated = set(
            UserRating.objects.filter(user_id=user_id).values_list('book_id', flat=True)
        )
        
        candidate_books = all_books - user_rated
        
        # Predict ratings
        for book_id in candidate_books:
            predicted_rating = self.predict_rating(user_id, book_id)
            predictions.append((book_id, predicted_rating))
        
        # Sort by predicted rating
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions[:n_recommendations]
    
    def get_popular_books(self, n=5):
        """Get most popular books"""
        popular = Book.objects.annotate(
            avg_rating=models.Avg('reviews__rating'),
            review_count=models.Count('reviews')
        ).order_by('-avg_rating')[:n]
        
        return [(book.id, book.average_rating) for book in popular]
    
    def get_similar_users(self, user_id, n_similar=5):
        """
        Get similar users using cosine similarity
        
        Args:
            user_id: User ID
            n_similar: Number of similar users
            
        Returns:
            List of similar user IDs
        """
        if self.user_factors is None or user_id not in self.user_map:
            return []
        
        user_idx = self.user_map[user_id]
        user_vector = self.user_factors[user_idx].reshape(1, -1)
        
        # Calculate similarity with all users
        similarities = cosine_similarity(user_vector, self.user_factors)[0]
        
        # Get top similar users (exclude the user itself)
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]
        
        # Map back to user IDs
        reverse_map = {v: k for k, v in self.user_map.items()}
        similar_users = [reverse_map[idx] for idx in similar_indices]
        
        return similar_users


def generate_recommendations(user_id, n_recommendations=5):
    """
    Generate and store recommendations for a user
    
    Args:
        user_id: User ID
        n_recommendations: Number of recommendations to generate
    """
    from .models import RecommendationModel
    
    # Get active model
    model_config = RecommendationModel.objects.filter(is_active=True).first()
    if not model_config:
        return
    
    # Initialize and train engine
    engine = CollaborativeFilteringEngine(
        n_factors=model_config.n_factors,
        n_epochs=model_config.n_epochs,
        learning_rate=model_config.learning_rate,
        regularization=model_config.regularization
    )
    
    if not engine.train():
        return
    
    # Get recommendations
    recommendations = engine.get_recommendations(user_id, n_recommendations)
    
    # Store in database
    for book_id, score in recommendations:
        try:
            book = Book.objects.get(id=book_id)
            RecommendedBook.objects.update_or_create(
                user_id=user_id,
                book=book,
                defaults={
                    'recommendation_score': score,
                    'recommendation_type': 'collaborative_filtering',
                }
            )
        except Book.DoesNotExist:
            continue


def train_all_models():
    """Train all active recommendation models"""
    from .models import RecommendationModel
    
    models = RecommendationModel.objects.filter(is_active=True)
    
    for model_config in models:
        engine = CollaborativeFilteringEngine(
            n_factors=model_config.n_factors,
            n_epochs=model_config.n_epochs,
            learning_rate=model_config.learning_rate,
            regularization=model_config.regularization
        )
        
        if engine.train():
            # Generate recommendations for all users
            users = User.objects.filter(userrating__isnull=False).distinct()
            for user in users:
                generate_recommendations(user.id, n_recommendations=10)
