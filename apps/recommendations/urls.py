from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendations_view, name='recommendations'),
    path('track/<int:book_id>/<str:interaction_type>/', views.track_interaction, name='track_interaction'),
]
