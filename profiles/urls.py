from django.urls import path
from .views import profile_view, edit_profile_view, change_password_view, portfolio_view, delete_portfolio_image, delete_review_view, add_review_view

app_name = 'profiles'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('<int:user_id>/', profile_view, name='user_profile'),
    path('<int:user_id>/edit/', edit_profile_view, name='edit_profile'),
    path('<int:user_id>/change-password/', change_password_view, name='change_password'),
    path('portfolio/delete/<int:image_id>/', delete_portfolio_image, name='delete_portfolio_image'),
    path('<int:user_id>/portfolio/', portfolio_view, name='portfolio'),
    path('<int:user_id>/add-review/', add_review_view, name='add_review'),
    path('review/delete/<int:review_id>/', delete_review_view, name='delete_review'),
]