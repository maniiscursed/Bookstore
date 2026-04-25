from django import forms
from .models import Book, BookReview


class BookSearchForm(forms.Form):
    """Book search form"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author...'
        })
    )
    category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price'
        })
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Sort by...'),
            ('newest', 'Newest'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('rating', 'Rating'),
            ('bestseller', 'Bestsellers'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BookReviewForm(forms.ModelForm):
    """Book review form"""
    class Meta:
        model = BookReview
        fields = ['rating', 'title', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your review here...'
            }),
        }
