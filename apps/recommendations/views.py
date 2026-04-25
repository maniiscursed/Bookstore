from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models import Q
from apps.books.models import Book
from .models import RecommendedBook, UserRating
from .engine import generate_recommendations


def _get_related_books_from_searches(search_terms, limit=8):
    """Build a related-books list from recent search terms."""
    related_ids = []

    for term in search_terms:
        normalized_term = term.strip()
        if not normalized_term:
            continue

        matches = Book.objects.filter(
            Q(title__icontains=normalized_term)
            | Q(author__icontains=normalized_term)
            | Q(description__icontains=normalized_term)
            | Q(category__name__icontains=normalized_term)
        ).order_by('-created_at')

        for book_id in matches.values_list('id', flat=True):
            if book_id not in related_ids:
                related_ids.append(book_id)
            if len(related_ids) >= limit:
                break

        if len(related_ids) >= limit:
            break

    if not related_ids:
        return []

    books_by_id = {book.id: book for book in Book.objects.filter(id__in=related_ids)}
    return [books_by_id[book_id] for book_id in related_ids if book_id in books_by_id]


@login_required(login_url='accounts:login')
def recommendations_view(request):
    """Display personalized book recommendations"""
    user = request.user
    search_count = request.session.get('book_search_count', 0)
    recent_searches = request.session.get('recent_book_searches', [])
    
    # Get or generate recommendations
    recommendation_records = RecommendedBook.objects.filter(user=user).select_related('book').order_by('-recommendation_score')[:10]
    
    if not recommendation_records.exists():
        # Generate new recommendations
        generate_recommendations(user.id, n_recommendations=10)
        recommendation_records = RecommendedBook.objects.filter(user=user).select_related('book').order_by('-recommendation_score')[:10]

    if recommendation_records.exists():
        recommended_books = [record.book for record in recommendation_records]
    else:
        recommended_books = list(
            Book.objects.annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            ).filter(review_count__gt=0).order_by('-avg_rating')[:10]
        )
    
    # Get trending books
    trending = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:5]
    
    # Get newly added books
    new_releases = Book.objects.all().order_by('-created_at')[:5]

    related_books = []
    show_related_books = search_count >= 5
    if show_related_books:
        related_books = _get_related_books_from_searches(recent_searches)
    
    context = {
        'recommended_books': recommended_books,
        'related_books': related_books,
        'trending_books': trending,
        'new_releases': new_releases,
        'search_count': search_count,
        'recent_searches': recent_searches[:5],
        'show_related_books': show_related_books,
    }
    return render(request, 'recommendations/recommendations.html', context)


@login_required(login_url='accounts:login')
def track_interaction(request, book_id, interaction_type):
    """Track user interactions for recommendations"""
    from apps.books.models import Book
    
    book = Book.objects.get(id=book_id)
    
    # Record interaction
    UserRating.objects.get_or_create(
        user=request.user,
        book=book,
        interaction_type=interaction_type,
        defaults={'interaction_weight': 1.0}
    )
    
    # Mark recommendation as clicked
    RecommendedBook.objects.filter(
        user=request.user,
        book=book
    ).update(is_clicked=True)
    
    return render(request, 'recommendations/interaction_tracked.html')
