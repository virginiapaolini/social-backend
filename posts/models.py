from django.db import models
from django.conf import settings


class Post(models.Model):
    """Modello per i Post del Social Network"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # relazione molti-a-molti per i "like" ai post
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )

    def __str__(self):
        return f"Post di {self.author.username} ({self.created_at.strftime('%d/%m/%Y')})"


class Comment(models.Model):
    """Modello per i Commenti sotto i Post"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commento di {self.author.username} su Post {self.post.id}"
