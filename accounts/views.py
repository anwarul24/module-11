from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterForm, ProfileUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:redirect")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("dashboard:redirect")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class RoleAwareLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"profile_user": request.user})


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})
