from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Book, Category, BookReview, WishList
from .forms import BookSearchForm, BookReviewForm


def _record_book_search(request, query):
    """Track recent search terms in the session for recommendations."""
    normalized_query = query.strip()
    if not normalized_query:
        return

    search_count = request.session.get('book_search_count', 0) + 1
    recent_searches = request.session.get('recent_book_searches', [])
    recent_searches = [item for item in recent_searches if item.lower() != normalized_query.lower()]
    recent_searches.insert(0, normalized_query)

    request.session['book_search_count'] = search_count
    request.session['recent_book_searches'] = recent_searches[:10]
    request.session.modified = True


def home(request):
    """Display home page with featured books, bestsellers, and discounted books"""
    # Get featured books (latest books with cover images)
    featured_books = Book.objects.filter(cover_image__isnull=False).order_by('-created_at')[:6]
    
    # Get bestsellers
    bestsellers = Book.objects.filter(is_bestseller=True, cover_image__isnull=False)[:6]
    
    # Get books with special discounts (discount_percentage > 0)
    special_discounts = Book.objects.filter(discount_percentage__gt=0, cover_image__isnull=False).order_by('-discount_percentage')[:6]
    
    context = {
        'featured_books': featured_books,
        'bestsellers': bestsellers,
        'special_discounts': special_discounts,
    }
    return render(request, 'home.html', context)


def book_list(request):
    """Display list of books with filters and search"""
    books = Book.objects.all()
    categories = Category.objects.all()
    
    # Search and filters
    form = BookSearchForm(request.GET)
    
    if request.GET:
        query = request.GET.get('query', '')
        category = request.GET.get('category', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        sort_by = request.GET.get('sort_by', '')
        
        if query:
            _record_book_search(request, query)
            books = books.filter(Q(title__icontains=query) | Q(author__icontains=query) |
                               Q(description__icontains=query))
        
        if category:
            books = books.filter(category__name__icontains=category)
        
        if min_price:
            books = books.filter(price__gte=min_price)
        
        if max_price:
            books = books.filter(price__lte=max_price)
        
        # Sorting
        if sort_by == 'newest':
            books = books.order_by('-created_at')
        elif sort_by == 'price_low':
            books = books.order_by('price')
        elif sort_by == 'price_high':
            books = books.order_by('-price')
        elif sort_by == 'rating':
            books = books.order_by('-average_rating')
        elif sort_by == 'bestseller':
            books = books.filter(is_bestseller=True)
    
    context = {
        'books': books,
        'categories': categories,
        'form': form,
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, book_id):
    """Display detailed view of a single book"""
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    related_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:5]
    
    user_review = None
    if request.user.is_authenticated:
        user_review = book.reviews.filter(user=request.user).first()
    
    context = {
        'book': book,
        'reviews': reviews,
        'related_books': related_books,
        'user_review': user_review,
        'in_wishlist': False,
    }
    
    if request.user.is_authenticated:
        try:
            wishlist = request.user.wishlist
            context['in_wishlist'] = book in wishlist.books.all()
        except WishList.DoesNotExist:
            pass
    
    return render(request, 'books/book_detail.html', context)


@login_required(login_url='accounts:login')
def add_review(request, book_id):
    """Add or update book review"""
    book = get_object_or_404(Book, id=book_id)
    user_review = book.reviews.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = BookReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookReviewForm(instance=user_review)
    
    context = {
        'form': form,
        'book': book,
        'is_edit': user_review is not None,
    }
    return render(request, 'books/review_form.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def add_to_wishlist(request, book_id):
    """Add book to wishlist"""
    book = get_object_or_404(Book, id=book_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    
    if book in wishlist.books.all():
        wishlist.books.remove(book)
        messages.success(request, f'Removed "{book.title}" from wishlist.')
    else:
        wishlist.books.add(book)
        messages.success(request, f'Added "{book.title}" to wishlist.')
    
    return redirect('books:book_detail', book_id=book.id)


@login_required(login_url='accounts:login')
def wishlist_view(request):
    """Display user's wishlist"""
    try:
        wishlist = request.user.wishlist
        books = wishlist.books.all()
    except WishList.DoesNotExist:
        wishlist = None
        books = []
    
    context = {
        'wishlist': wishlist,
        'books': books,
    }
    return render(request, 'books/wishlist.html', context)


def category_books(request, category_id):
    """Display books by category"""
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all()
    all_categories = Category.objects.all()
    
    context = {
        'category': category,
        'books': books,
        'categories': all_categories,
    }
    return render(request, 'books/category_books.html', context)
