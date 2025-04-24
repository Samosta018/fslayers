from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Order
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Роль'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    pass  


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'category', 'deadline', 'budget', 'is_negotiable']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'category': forms.Select(attrs={'class': 'order-form__select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_negotiable = cleaned_data.get('is_negotiable')
        budget = cleaned_data.get('budget')

        if not is_negotiable and not budget:
            raise forms.ValidationError("Укажите бюджет или отметьте 'Договорной'")
        return cleaned_data