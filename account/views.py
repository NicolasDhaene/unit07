from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, UserProfileForm, EditAccountForm, ChangePasswordForm
from .models import User, UserProfile


def sign_up(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )
            login(request, user)
            messages.success(
                request,
                "You're now registred and signed in."
            )
            return redirect("home")
    return render(request, 'account/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You're now signed out.")
    return redirect("home")


def sign_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            login(request, user)
            messages.success(
                request,
                "You're now signed in."
            )
            return redirect("home")
    return render(request, "account/sign_in.html", {"form": form})


@login_required
def view_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    return render(request, 'account/profile.html', {'user': user, "profile": profile})


@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    form1 = EditAccountForm(instance=user)
    form2 = UserProfileForm(instance=user.userprofile)
    if request.method == "POST":
        form1 = EditAccountForm(instance=user, data=request.POST)
        form2 = UserProfileForm(instance=user.userprofile, data=request.POST, files=request.FILES)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(
                request,
                "Account and Profile updated"
            )
            return redirect("view_profile", pk=user.pk)
    return render(request, "account/edit_profile.html", {"user": user,
                                                         "form1": form1,
                                                         "form2": form2,
                                                         "profile": profile})


@login_required
def change_password(request, pk):
    user = request.user
    form = ChangePasswordForm(user=request.user, request=request)
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST, request=request)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request,
                "Password changed"
            )
            return redirect("view_profile", pk=user.pk)
    return render(request, 'account/change_password.html', {"form": form})