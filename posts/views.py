from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrModeratorOrReadOnly
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404


class PostListCreateView(generics.ListCreateAPIView):
    """Endpoint per listare tutti i post e crearne uno nuovo (C_UD)"""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [SearchFilter]
    search_fields = ['content', 'author__username']

    def perform_create(self, serializer):
        # associa automaticamente l'utente loggato come autore del post
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint per leggere, aggiornare o eliminare un singolo post (CR_D)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # applico il  controllo permessi personalizzato!
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrModeratorOrReadOnly]


class FeedView(generics.ListAPIView):
    """Endpoint personalizzato per vedere solo i post degli utenti seguiti"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # filtra i post dove l'autore è presente nella lista 'following' dell'utente loggato
        return Post.objects.filter(author__in=self.request.user.following.all()).order_by('-created_at')


class LikePostView(APIView):
    """Endpoint per mettere o togliere il Like a un post"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post non trovato."}, status=status.HTTP_404_NOT_FOUND)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response({"message": "Like rimosso."}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({"message": "Like aggiunto."}, status=status.HTTP_200_OK)


class CommentCreateView(generics.CreateAPIView):
    """Endpoint per aggiungere un commento a un post specifico"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"error": "Post non trovato."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(author=self.request.user, post=post)

class ToggleLikeView(APIView):
    """Endpoint per mettere o togliere il like a un post (Toggle)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        # intanto prendo il post (se non esiste, Django lancia un 404 automatico)
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # controllo se l'utente ha già messo like a questo post
        if post.likes.filter(id=user.id).exists():
            # se esiste già, togliamo il like (Unlike)
            post.likes.remove(user)
            return Response(
                {"message": "Like rimosso con successo.", "liked": False},
                status=status.HTTP_200_OK
            )
        else:
            # se non esiste, aggiungiamo il like (Like)!!!
            post.likes.add(user)
            return Response(
                {"message": "Like aggiunto con successo.", "liked": True},
                status=status.HTTP_200_OK
            )
