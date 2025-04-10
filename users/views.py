from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import RegistrationForm, LoginForm


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!!!")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the errors.")
        return render(request, "users/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect("dashboard:home")
            else:
                messages.error(
                    request, "Login Unsuccessful. Please check your email and password."
                )
        return render(request, "users/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
