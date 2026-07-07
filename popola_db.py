import os
import django

# inizializza l'ambiente djangp
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialAPI.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


def popola_database():
    print("Inizio popolamento database...")

    # crea  utenti con i ruoli richiesti dalle specifiche
    # admin / Superuser
    if not User.objects.filter(username='admin_demo').exists():
        admin_user = User.objects.create_superuser(
            username='admin_demo',
            email='admin@example.com',
            password='admin12345'
        )
        print("Creato utente: admin_demo (Administrator)")

    # moderatore (gestisce blocco/rimozione)
    if not User.objects.filter(username='manager_demo').exists():
        moderator_user = User.objects.create_user(
            username='manager_demo',
            email='moderator@example.com',
            password='manager12345'
        )
        if hasattr(moderator_user, 'role'):
            moderator_user.role = 'MODERATOR'  # o il valore stringa che uso per i moderatori
            moderator_user.save()
        print("Creato utente: manager_demo (Moderator)")
    else:
        moderator_user = User.objects.get(username='manager_demo')

    # Utente Standard
    if not User.objects.filter(username='user_demo').exists():
        standard_user = User.objects.create_user(
            username='user_demo',
            email='user@example.com',
            password='user12345'
        )
        if hasattr(standard_user, 'role'):
            standard_user.role = 'STANDARD'
            standard_user.save()
        print("Creato utente: user_demo (Standard User)")
    else:
        standard_user = User.objects.get(username='user_demo')

    # creazione di post e interazioni per il testing immediato
    Post.objects.all().delete()  # Resetta i post vecchi per pulizia

    post1 = Post.objects.create(
        author=standard_user,
        content="Sto preparando il progetto finale di Back-end per il corso PPM 2026. Django REST Framework è fantastico!"
    )

    post2 = Post.objects.create(
        author=standard_user,
        content="Ricordatevi di impostare DEBUG=False e configurare WhiteNoise prima della consegna finale del codice."
    )

    post3 = Post.objects.create(
        author=moderator_user,
        content="Avviso di servizio: si prega di mantenere i toni costruttivi all'interno della piattaforma."
    )

    #  qualche interazione (Like)
    if hasattr(post1, 'likes'):
        post1.likes.add(moderator_user)
    if hasattr(post2, 'likes'):
        post2.likes.add(standard_user)

    print("Post e interazioni demo creati con successo!")
    print("Database pronto!")


if __name__ == '__main__':
    popola_database()