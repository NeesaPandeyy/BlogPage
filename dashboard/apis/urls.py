from django.urls import path

from .views import PostDetailView, PostView

urlpatterns = [
    path("", PostView.as_view(), name="postlist"),
    path("<int:pk>", PostDetailView.as_view(), name="postdetail"),
]
