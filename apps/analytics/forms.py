from django import forms

from apps.books.models import Book


class AdminBookForm(forms.ModelForm):
    cover_image_url = forms.URLField(
        required=False,
        label='Cover image URL',
        help_text='Paste a direct image URL or a book page URL. The dashboard will try to download the cover automatically.',
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'category',
            'price',
            'stock',
            'isbn',
            'publication_date',
            'publisher',
            'pages',
            'language',
            'source_url',
            'cover_image',
            'is_bestseller',
            'discount_percentage',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'source_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional source or wiki URL'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_bestseller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }