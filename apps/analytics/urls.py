from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/manage/', views.manage_books, name='manage_books'),
    path('users/manage/', views.manage_users, name='manage_users'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('sales/', views.sales_analytics, name='sales_analytics'),
    path('users/', views.user_analytics, name='user_analytics'),
]
