from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    # mostriamo i dettagli dell'autore
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'post', 'author', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # mostriamo i commenti associati al post 
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']