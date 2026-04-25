from django import forms
from django.contrib import admin, messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
import re
import requests
from .models import Category, Book, BookReview, WishList


def _download_image_bytes(url):
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if response.status_code != 200:
            return None

        content = response.content
        content_type = (response.headers.get('content-type') or '').lower()

        if len(content) < 1000:
            return None

        if 'image' not in content_type and not content.startswith((b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a')):
            return None

        return content
    except requests.RequestException:
        return None


def _extract_og_image(page_url):
    try:
        response = requests.get(
            page_url,
            timeout=20,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if response.status_code != 200:
            return None

        html = response.text
        patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)
        return None
    except requests.RequestException:
        return None


def _download_cover_from_url(url):
    if not url:
        return None

    image_bytes = _download_image_bytes(url)
    if image_bytes:
        return image_bytes

    og_image_url = _extract_og_image(url)
    if og_image_url:
        return _download_image_bytes(og_image_url)

    return None


class BookAdminForm(forms.ModelForm):
    cover_image_url = forms.URLField(
        required=False,
        label='Cover image URL',
        help_text='Paste a direct image URL or a book page URL. The admin will try to download the cover automatically.',
    )

    class Meta:
        model = Book
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'category', 'price', 'stock', 'average_rating', 'is_bestseller', 'source_url')
    list_filter = ('category', 'is_bestseller', 'created_at', 'publication_date')
    search_fields = ('title', 'author', 'isbn', 'source_url')
    readonly_fields = ('average_rating', 'total_reviews', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'author', 'description', 'category', 'source_url')}),
        ('Publication', {'fields': ('isbn', 'publisher', 'publication_date', 'pages', 'language')}),
        ('Commercial', {'fields': ('price', 'stock', 'discount_percentage', 'is_bestseller')}),
        ('Media', {'fields': ('cover_image', 'cover_image_url')}),
        ('Ratings', {'fields': ('average_rating', 'total_reviews')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def save_model(self, request, obj, form, change):
        cover_source_url = form.cleaned_data.get('cover_image_url') or obj.source_url
        manual_cover = form.cleaned_data.get('cover_image')

        if not manual_cover and cover_source_url:
            cover_bytes = _download_cover_from_url(cover_source_url)
            if cover_bytes:
                if obj.pk and obj.cover_image:
                    default_storage.delete(obj.cover_image.name)

                filename = f"{slugify(obj.title) or 'book'}-cover.jpg"
                obj.cover_image.save(filename, ContentFile(cover_bytes), save=False)
            else:
                messages.warning(
                    request,
                    f'No cover could be downloaded from {cover_source_url}. The book was saved without changing its cover.',
                )

        super().save_model(request, obj, form, change)


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'book')
    search_fields = ('book__title', 'user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    filter_horizontal = ('books',)
