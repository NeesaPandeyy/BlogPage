from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """A form to post blogs.

    Attributes:
        title (CharField): A required text area for user to write title of content.
        content (TextAreaField): A required text area for user to write content.
    """

    class Meta:
        model = Post
        fields = ["title", "content"]
