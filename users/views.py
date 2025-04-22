from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm

from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

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