from django.urls import path
from . import views

urlpatterns = [
    path('find-executor/', views.ai_find_executor, name='ai_find_executor'),
]