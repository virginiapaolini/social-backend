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

    # evita commenti vuoti
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Il contenuto del commento non può essere vuoto o contenere solo spazi.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # mostriamo i commenti associati al post 
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

   # lunghezza minima dei post
    def validate_content(self, value):
        clean_value = value.strip()
        if len(clean_value) < 5:
            raise serializers.ValidationError("Il contenuto del post deve essere lungo almeno 5 caratteri.")
        return clean_value