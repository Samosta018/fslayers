from django.db import models
from accounts.models import Customer

class Order(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Программирование'),
        ('design', 'Дизайн'),
        ('copywriting', 'Копирайтинг'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=255, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание заказа')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    days_to_complete = models.PositiveIntegerField(verbose_name='Срок выполнения (дней)')
    budget = models.PositiveIntegerField(verbose_name='Бюджет', null=True, blank=True)
    is_budget_negotiable = models.BooleanField(default=False, verbose_name='Бюджет обсуждается')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.customer.user.name}"
