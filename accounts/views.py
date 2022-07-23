from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
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


