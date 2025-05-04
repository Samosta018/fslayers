from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='orders'),
    path('create_order/', views.create_order_view, name='create_order'),
]