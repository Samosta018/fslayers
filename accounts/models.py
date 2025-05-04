from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=150)
    is_customer = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']  
    
    def __str__(self):
        return self.email

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.user.name}"

class Executor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.FloatField(default=0.0)
    completed_orders = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.name}"