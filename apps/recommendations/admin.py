from django.contrib import admin
from .models import UserRating, RecommendationModel, UserSimilarity, RecommendedBook


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'interaction_type', 'created_at')
    list_filter = ('interaction_type', 'rating', 'created_at')
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RecommendationModel)
class RecommendationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'n_factors', 'accuracy', 'is_active', 'last_retrained')
    list_filter = ('model_type', 'is_active')
    readonly_fields = ('trained_at', 'last_retrained')


@admin.register(UserSimilarity)
class UserSimilarityAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'similarity_score', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    readonly_readonly_fields = ('created_at',)


@admin.register(RecommendedBook)
class RecommendedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'recommendation_score', 'recommendation_type', 'is_clicked')
    list_filter = ('recommendation_type', 'is_clicked', 'created_at')
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created_at',)
