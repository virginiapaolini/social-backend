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

class BlockUserView(APIView):
    """Endpoint per permettere ai Moderatori di bloccare/disattivare un account"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # controllo se l'utente che fa la richiesta è un vero MODERATOR
        if request.user.role != CustomUser.Role.MODERATOR:
            return Response(
                {"detail": "Azione consentita solo ai moderatori."},
                status=status.HTTP_403_FORBIDDEN
            )

        # cerco l'utente da bloccare nel database
        try:
            user_to_block = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Utente da bloccare non trovato."},
                status=status.HTTP_404_NOT_FOUND
            )

        #  un moderatore non può bloccare se stesso neanche per errore
        if user_to_block == request.user:
            return Response(
                {"error": "Non puoi bloccare il tuo stesso account."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # logica di blocco/sblocco (Toggle)
        if user_to_block.is_active:
            user_to_block.is_active = False
            user_to_block.save()
            return Response(
                {"message": f"L'utente {user_to_block.username} è stato bloccato con successo."},
                status=status.HTTP_200_OK
            )
        else:
            # Se era già bloccato, lo sblocchiamo
            user_to_block.is_active = True
            user_to_block.save()
            return Response(
                {"message": f"L'utente {user_to_block.username} è stato riattivato."},
                status=status.HTTP_200_OK
            )
