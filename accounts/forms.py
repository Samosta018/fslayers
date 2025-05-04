from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Executor

class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[('customer', 'Заказчик'), ('executor', 'Исполнитель')],
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        
        if commit:
            user.save()
            
            role = self.cleaned_data['role']
            if role == 'customer':
                user.is_customer = True
                Customer.objects.create(user=user)  
            else:
                user.is_executor = True
                Executor.objects.create(user=user) 
            user.save()
        
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)