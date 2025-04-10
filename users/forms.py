from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None,
        }

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="",
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
        help_text="",
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.Please choose another one")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already taken.Please choose another one")
        return email


class LoginForm(AuthenticationForm):
    pass
