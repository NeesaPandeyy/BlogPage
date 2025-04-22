from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (AccountView, HomeView, PostCreateView, PostDeleteView,
                    PostDetailView, PostUpdateView)

app_name = "dashboard"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/", AccountView.as_view(), name="account"),
    path("account/<str:username>/", AccountView.as_view(), name="user_account"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
