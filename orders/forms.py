from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'category', 'days_to_complete', 'budget', 'is_budget_negotiable']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'days_to_complete': forms.NumberInput(attrs={'min': 1, 'max': 365}),
            'budget': forms.NumberInput(attrs={'min': 0, 'step': 100}),
        }