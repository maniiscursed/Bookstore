from django.contrib import admin
from .models import DailySalesMetric, CategoryAnalytics, UserEngagementMetric


@admin.register(DailySalesMetric)
class DailySalesMetricAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_revenue', 'total_orders', 'total_items_sold', 'average_order_value')
    list_filter = ('date',)
    readonly_fields = ('date',)


@admin.register(CategoryAnalytics)
class CategoryAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('category', 'total_sales', 'total_revenue', 'average_rating')
    list_filter = ('category',)
    search_fields = ('category__name',)


@admin.register(UserEngagementMetric)
class UserEngagementMetricAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_purchases', 'total_spent', 'total_reviews')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('account_age_days',)
