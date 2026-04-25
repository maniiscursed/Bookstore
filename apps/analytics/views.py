from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.db.models import Sum, Count, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods
from apps.orders.models import Order
from apps.books.models import Book, Category
from apps.books.utils import download_cover_from_url
from .forms import AdminBookForm
from .models import DailySalesMetric, CategoryAnalytics, UserEngagementMetric


def is_admin(user):
    """Check if user is admin"""
    profile = getattr(user, 'profile', None)
    return user.is_superuser or user.is_staff or (profile and profile.role == 'admin')


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with analytics"""

    # Total statistics
    total_orders = Order.objects.filter(status='delivered').count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('final_amount'))['final_amount__sum'] or 0
    total_customers = Order.objects.values('user').distinct().count()
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    recent_books = Book.objects.all().order_by('-created_at')[:12]
    recent_users = []
    for user in User.objects.all().order_by('-date_joined')[:12]:
        profile = getattr(user, 'profile', None)
        recent_users.append({
            'user': user,
            'role': profile.role if profile else 'customer',
        })
    
    # Top selling books
    top_books = Book.objects.annotate(
        sales_count=Count('orderitem')
    ).order_by('-sales_count')[:5]
    
    # Category performance
    category_analytics = CategoryAnalytics.objects.all().order_by('-total_revenue')[:5]
    
    # Top customers
    top_customers = Order.objects.values('user__username', 'user__email').annotate(
        total_orders=Count('id'),
        total_spent=Sum('final_amount')
    ).order_by('-total_spent')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_books': total_books,
        'total_users': total_users,
        'total_categories': total_categories,
        'recent_orders': recent_orders,
        'recent_books': recent_books,
        'recent_users': recent_users,
        'top_books': top_books,
        'category_analytics': category_analytics,
        'top_customers': top_customers,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def add_book(request):
    """Add a new book from the admin area."""
    if request.method == 'POST':
        form = AdminBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            cover_source_url = form.cleaned_data.get('cover_image_url') or book.source_url

            if not form.cleaned_data.get('cover_image') and cover_source_url:
                cover_bytes = download_cover_from_url(cover_source_url)
                if cover_bytes:
                    filename = f"{slugify(book.title) or 'book'}-cover.jpg"
                    book.cover_image.save(filename, ContentFile(cover_bytes), save=False)
                else:
                    messages.warning(
                        request,
                        'The book was saved, but no cover could be downloaded from the provided URL.',
                    )

            book.save()
            messages.success(request, f'Book "{book.title}" added successfully.')
            return redirect('analytics:manage_books')
    else:
        form = AdminBookForm()

    return render(request, 'admin_dashboard/add_book.html', {'form': form})


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def manage_books(request):
    """Show books and allow deletions."""
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/manage_books.html', {'books': books})


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def manage_users(request):
    """Show users and allow deletions."""
    users = []
    for user in User.objects.all().order_by('-date_joined'):
        profile = getattr(user, 'profile', None)
        users.append({
            'user': user,
            'role': profile.role if profile else 'customer',
        })

    return render(request, 'admin_dashboard/manage_users.html', {'users': users})


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.cover_image:
        book.cover_image.delete(save=False)
    title = book.title
    book.delete()
    messages.success(request, f'Book "{title}" deleted successfully.')
    return redirect('analytics:manage_books')


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account from the dashboard.')
        return redirect('analytics:manage_users')

    username = target_user.username
    target_user.delete()
    messages.success(request, f'User "{username}" deleted successfully.')
    return redirect('analytics:manage_users')


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def sales_analytics(request):
    """Detailed sales analytics"""
    
    daily_metrics = DailySalesMetric.objects.all().order_by('-date')[:30]
    
    # Revenue trend
    total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('final_amount'))['final_amount__sum'] or 0
    total_orders = Order.objects.filter(status='delivered').count()
    
    # Payment methods
    payment_methods = Order.objects.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('final_amount')
    ).order_by('-count')
    
    context = {
        'daily_metrics': daily_metrics,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'admin_dashboard/sales_analytics.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def user_analytics(request):
    """User analytics"""
    
    total_users = UserEngagementMetric.objects.count()
    avg_purchases = UserEngagementMetric.objects.aggregate(Avg('total_purchases'))['total_purchases__avg'] or 0
    avg_spent = UserEngagementMetric.objects.aggregate(Avg('total_spent'))['total_spent__avg'] or 0
    
    # Top users
    top_users = UserEngagementMetric.objects.all().order_by('-total_spent')[:10]
    
    context = {
        'total_users': total_users,
        'avg_purchases': avg_purchases,
        'avg_spent': avg_spent,
        'top_users': top_users,
    }
    
    return render(request, 'admin_dashboard/user_analytics.html', context)
