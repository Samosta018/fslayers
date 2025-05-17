from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='assistant'),
    path('api/', views.chat_api, name='assistant-api'),
]