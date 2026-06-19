from rest_framework import permissions
from users.models import CustomUser

class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato:
    - chiunque (autenticato) può leggere (GET).
    - solo l'autore può modificare (PUT/PATCH).
    - l'autore OPPURE un moderatore possono cancellare (DELETE).
    """
    def has_object_permission(self, request, view, obj):
        # i metodi di lettura (GET, HEAD, OPTIONS) sono sempre consentiti!
        if request.method in permissions.SAFE_METHODS:
            return True

        # se l'operazione è una cancellazione (DELETE), permettiamola anche al moderatore
        if request.method == 'DELETE' and request.user.role == CustomUser.Role.MODERATOR:
            return True

        # in tutti gli altri casi (modifiche), solo l'autore originario ha i permessi
        return obj.author == request.user