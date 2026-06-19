from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Endpoint pubblico per registrare un nuovo utente"""
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):
    """Endpoint per listare tutti gli utenti (richiede login)"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowUserView(APIView):
    """Endpoint per seguire/smettere di seguire un utente"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Utente non trovato."}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({"error": "Non puoi seguire te stesso."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=user_id).exists():
            # Se lo segue già, fa un-follow
            request.user.following.remove(user_to_follow)
            return Response({"message": f"Hai smesso di seguire {user_to_follow.username}."}, status=status.HTTP_200_OK)
        else:
            # Altrimenti fa follow
            request.user.following.add(user_to_follow)
            return Response({"message": f"Ora segui {user_to_follow.username}."}, status=status.HTTP_200_OK)
