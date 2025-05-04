from django.urls import path
from .views import profile_view, edit_profile_view, change_password_view

app_name = 'profiles'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('<int:user_id>/', profile_view, name='user_profile'),
    path('<int:user_id>/edit/', edit_profile_view, name='edit_profile'),
    path('<int:user_id>/change-password/', change_password_view, name='change_password'),
]