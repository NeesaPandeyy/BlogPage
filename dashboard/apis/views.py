from rest_framework import generics
from ..models import Post
from .serializers import PostSerializer
from .permissions import IsAuthor
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields=('author',)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
