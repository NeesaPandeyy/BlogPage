from rest_framework import serializers

from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    date_posted = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "date_posted"]
