from django.urls import path
from .views import PostListCreateView, PostDetailView, FeedView, LikePostView, CommentCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post_like'),
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment_create'),
    path('feed/', FeedView.as_view(), name='user_feed'),
]