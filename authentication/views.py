from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm


def login(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Invalid login details')
    else:
        form = AuthenticationForm()
    return render(request, 'users/accounts/login.html', {'form': form})

def logout(request):
    return render(request,'users/accounts/login.html')