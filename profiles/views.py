from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile
from accounts.models import User
from .forms import ProfileForm, UserForm, PasswordChangeForm

User = get_user_model()

def profile_view(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    
    profile = user.profile
    is_owner = (request.user == user)
    
    return render(request, 'profiles/profile.html', {
        'profile_user': user,
        'profile': profile,
        'is_owner': is_owner
    })

@login_required
def edit_profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        return redirect('profiles:user_profile', user_id=user_id)
    
    if request.method == 'POST':
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
        'profile_form': profile_form
    })

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