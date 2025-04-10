from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Post
from .forms import PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/home.html"
    context_object_name = "posts"
    paginate_by = 3
    login_url = "login"

    def get_queryset(self):
        return Post.objects.order_by("-date_posted")


class AccountView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "users/profile.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        username = self.kwargs.get("username", None)
        if username:
            user = get_object_or_404(User, username=username)
            return Post.objects.filter(author=user).order_by("-date_posted")
        return Post.objects.filter(author=self.request.user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username", None)
        if username:
            user = get_object_or_404(User, username=username)
            context["user"] = user
            context["profile"] = (
                user.profile_picture.url if user.profile_picture else None
            )
            context["has_posts"] = bool(context["posts"])
        else:
            context["user"] = self.request.user
            context["profile"] = (
                self.request.user.profile_picture.url
                if self.request.user.profile_picture
                else None
            )
            context["has_posts"] = bool(context["posts"])
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/createpost.html"
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post Created Successfully")
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "dashboard/post.html"
    context_object_name = "post"


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/createpost.html"

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            raise PermissionDenied
        return post

    def form_valid(self, form):
        messages.success(self.request, "Successfully updated!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard:home")

    def get_object(self):
        post = super().get_object()
        messages.success(self.request, "Your post has been deleted successfully.")
        if post.author != self.request.user:
            raise PermissionDenied
        return post
