from django.urls import path

from .views import LoginView, RegisterView, UserView

urlpatterns = [
    path("", UserView.as_view(), name="userlist"),
    path("register/", RegisterView.as_view(), name="register-api"),
    path("login/", LoginView.as_view(), name="login-api"),
]
