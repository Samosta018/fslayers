from django.urls import path
from .views import signup_view, login_view
from .views import custom_logout

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
]