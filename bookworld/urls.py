"""
URL configuration for bookworld project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.books.views import home

admin.site.site_header = 'SuperControls'
admin.site.site_title = 'SuperControls'
admin.site.index_title = 'SuperControls'

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('books/', include('apps.books.urls', namespace='books')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('recommendations/', include('apps.recommendations.urls', namespace='recommendations')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
