from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/review/', views.add_review, name='add_review'),
    path('<int:book_id>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlists/', views.wishlist_view, name='wishlist'),
    path('category/<int:category_id>/', views.category_books, name='category_books'),
]
