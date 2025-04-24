from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm, OrderForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          
            login(request, user)        
            return redirect('home')     
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) 
            if user is not None:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form}) 


@require_POST  
def custom_logout(request):
    logout(request)
    return redirect('home') 


@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'page_title': 'Личный кабинет'
    }
    return render(request, 'pages/profile.html', context)


@login_required
def order_view(request):
    if request.user.role != 'customer':
        logger.warning(f"Попытка создания заказа не заказчиком: {request.user}")
        return redirect('home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.author = request.user
                order.author_rating = request.user.rating
                order.save()
                logger.info(f"Создан новый заказ: {order}")
                return redirect('home')
            except Exception as e:
                logger.error(f"Ошибка при создании заказа: {str(e)}")
        else:
            logger.warning(f"Невалидная форма: {form.errors}")
    else:
        form = OrderForm()

    return render(request, 'pages/order.html', {'form': form})