from django import forms
from .models import Order, Payment


class CheckoutForm(forms.Form):
    """Checkout form"""
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Delivery address'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Postal code'
    }))
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('cod', 'Cash on Delivery'),
    ], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Order notes (optional)'
    }), required=False)
