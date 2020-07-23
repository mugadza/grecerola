from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

def signup(request):
    form = CustomUserCreationForm(request.POST)

    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        messages.success(request, f'Account created with email {email}!')

        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(request, user)

        return redirect('campaign-home')

    return render(request, 'account/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard/dashboard.html', {'bank': request.user.bank})

@login_required
def investor_wallet(request):
    return render(request, 'account/dashboard/investor_wallet.html', {'bank': request.user.bank})

@login_required
def deposit(request):
    return render(request, 'account/dashboard/deposit.html', {'bank': request.user.bank})
