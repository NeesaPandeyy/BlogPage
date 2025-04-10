from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince


User = get_user_model()


class Post(models.Model):
    """
    Represents a post created by a user.

    Attributes:
        title (str): Title of the post.
        content (str): Content of the post.
        date_posted (datetime): The time when the post was created.
        author: Foreign key referencing the user who created the post.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def time_ago(self):
        return timesince(self.date_posted) + " ago"
