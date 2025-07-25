from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from dashboard.models import Post
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="023015@"
        )
        self.user2 = User.objects.create_user(username="user2", password="pass1234")

        self.client.login(username="testuser", password="023015@")

    def create_post(
        self, author=None, title="Test Post", content="Test Conetent", days_ago=0
    ):
        if not author:
            author = self.user
        return Post.objects.create(
            title=title,
            content=content,
            author=author,
            date_posted=timezone.now() - timedelta(days=days_ago),
        )


class HomeViewTest(BaseTestCase):
    def test_home_view(self):
        for i in range(5):
            self.create_post(title=f"Post {i}", days_ago=i)

        url = reverse("dashboard:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post 2")


class PostUpdateViewTest(BaseTestCase):
    def test_only_author_can_update(self):
        post = self.create_post(author=self.user2)
        url = reverse("dashboard:post_update", kwargs={"pk": post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_update_successfully(self):
        post = self.create_post()
        url = reverse("dashboard:post_update", kwargs={"pk": post.pk})
        response = self.client.post(url, {"title": "Updated", "content": "Updated"})
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated")


class PostDeleteViewTest(BaseTestCase):
    def test_only_author_can_delete(self):
        post = self.create_post(author=self.user2)
        url = reverse("dashboard:post_delete", kwargs={"pk": post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_sucessfull_delete(self):
        post = self.create_post(author=self.user)
        url = reverse("dashboard:post_delete", kwargs={"pk": post.pk})
        response = self.client.post(url)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
