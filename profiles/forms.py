from django import forms
from .models import Profile, User, PortfolioImage
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Оценка'
    )
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Напишите ваш отзыв здесь...'
        }),
        label='Текст отзыва'
    )

    class Meta:
        model = Review
        fields = ['rating', 'text']
        
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget = forms.FileInput(attrs={
            'class': 'hidden-file-input',
            'id': 'avatar-upload',
            'style': 'display: none;',
            'onchange': 'previewAvatar(this);'
        })
        self.fields['avatar'].label = ""
        self.fields['avatar'].required = False
        self.fields['bio'].label = "О себе"
        self.fields['skills'].label = "Навыки"
        self.fields['phone'].label = "Телефон"

    class Meta:
        model = Profile
        fields = ['bio', 'skills', 'avatar', 'phone']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Расскажите о себе...'
            }),
            'skills': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Например: Python, Django, JavaScript'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
        }
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Текущий пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите новый пароль")

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")
        
        return cleaned_data
    

class PortfolioImageForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = ['image', 'title', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название работы'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Описание работы...'
            }),
        }