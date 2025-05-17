from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('new/<int:user_id>/', views.chat_detail, name='new_chat'),
    path('api/messages/<int:chat_id>/', views.get_messages, name='get_messages'),
    path('api/chats/', views.get_chats, name='get_chats'),
]