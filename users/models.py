from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Заказчик'),
        ('executor', 'Исполнитель'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    rating = models.FloatField(default=5.0)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

class Order(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Программирование'),
        ('copywriting', 'Копирайтинг'),
        ('design', 'Дизайн'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    deadline = models.PositiveIntegerField()
    budget = models.PositiveIntegerField(null=True, blank=True)
    is_negotiable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author_rating = models.FloatField()

    def __str__(self):
        return self.title