from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, PortfolioImage
from accounts.models import User
from .forms import ProfileForm, UserForm, PasswordChangeForm, PortfolioImageForm
from .models import Review
from .forms import ReviewForm

@login_required
def add_review_view(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)
    
    if request.user == recipient:
        messages.error(request, 'Вы не можете оставить отзыв самому себе')
        return redirect('profiles:user_profile', user_id=user_id)
    
    try:
        review = Review.objects.get(author=request.user, recipient=recipient)
        is_edit = True
    except Review.DoesNotExist:
        review = None
        is_edit = False
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.recipient = recipient
            review.save()
            messages.success(request, 'Отзыв успешно сохранен!')
            return redirect('profiles:user_profile', user_id=user_id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'profiles/add_review.html', {
        'form': form,
        'recipient': recipient,
        'is_edit': is_edit
    })

@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.user != review.author:
        messages.error(request, 'Вы можете удалять только свои отзывы')
        return redirect('profiles:profile')
    
    user_id = review.recipient.id
    review.delete()
    messages.success(request, 'Отзыв успешно удален')
    return redirect('profiles:user_profile', user_id=user_id)
User = get_user_model()

def profile_view(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    
    profile = user.profile
    is_owner = (request.user == user)
    portfolio_images = PortfolioImage.objects.filter(profile=profile)
    reviews = Review.objects.filter(recipient=user).order_by('-created_at')
    
    # Проверяем, оставлял ли текущий пользователь отзыв этому пользователю
    has_review = False
    if request.user.is_authenticated and not is_owner:
        has_review = Review.objects.filter(author=request.user, recipient=user).exists()
    
    return render(request, 'profiles/profile.html', {
        'profile_user': user,
        'profile': profile,
        'is_owner': is_owner,
        'portfolio_images': portfolio_images,
        'reviews': reviews,
        'has_review': has_review
    })

@login_required
def edit_profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        return redirect('profiles:user_profile', user_id=user_id)
    
    portfolio_images = PortfolioImage.objects.filter(profile=user.profile)
    
    if request.method == 'POST':
        # Обработка основной формы профиля
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profiles:user_profile', user_id=user_id)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'portfolio_images': portfolio_images
    })

@login_required
def portfolio_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        return redirect('profiles:user_profile', user_id=user_id)
    
    if request.method == 'POST':
        form = PortfolioImageForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_item = form.save(commit=False)
            portfolio_item.profile = user.profile
            portfolio_item.save()
            messages.success(request, 'Изображение добавлено в портфолио!')
            return redirect('profiles:portfolio', user_id=user_id)
    else:
        form = PortfolioImageForm()
    
    portfolio_images = PortfolioImage.objects.filter(profile=user.profile)
    
    return render(request, 'profiles/portfolio.html', {
        'form': form,
        'portfolio_images': portfolio_images
    })

@login_required
def delete_portfolio_image(request, image_id):
    image = get_object_or_404(PortfolioImage, pk=image_id)
    if request.user != image.profile.user:
        return redirect('profiles:profile')
    
    user_id = request.user.id
    image.delete()
    messages.success(request, 'Изображение удалено из портфолио')
    return redirect('profiles:portfolio', user_id=user_id)  

@login_required
def change_password_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        return redirect('profiles:user_profile', user_id=user_id)
        
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            
            if not user.check_password(old_password):
                messages.error(request, 'Текущий пароль введен неверно')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен!')
                return redirect('profiles:profile')
    else:
        form = PasswordChangeForm()
    
    return render(request, 'profiles/change_password.html', {'form': form})