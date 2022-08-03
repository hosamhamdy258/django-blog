from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.urls import reverse

from .form import SignupForm

# Create your views here.


def signUp(req):
    form = SignupForm()
    if req.method == "POST":
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            return redirect('home')

    return render(req, 'accounts/signup.html', {'form': form})


def block_unblock(req, user_id):
    users = User.objects.all()
    user = get_object_or_404(User, pk=user_id)
    if user.is_active:
        user.is_active=False
        user.save()
    else:
        user.is_active=True
        user.save()
    return render(req, 'accounts/block.html',{'user':user,'users':users})











