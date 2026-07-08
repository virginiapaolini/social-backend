import os
import django

# inizializza l'ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialAPI.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()


def popola_database():
    print("Inizio popolamento database...")

    # Pulizia dati demo precedenti
    Comment.objects.all().delete()
    Post.objects.all().delete()

    # Creazione utenti demo
    admin_user, created = User.objects.get_or_create(
        username='admin_demo',
        defaults={
            'email': 'admin@example.com',
            'role': 'MODERATOR',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('admin12345')
    admin_user.email = 'admin@example.com'
    admin_user.role = 'MODERATOR'
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.save()
    print("Utente pronto: admin_demo / admin12345")

    moderator_user, created = User.objects.get_or_create(
        username='mod_demo',
        defaults={
            'email': 'mod@example.com',
            'role': 'MODERATOR',
            'bio': 'Moderatore ufficiale della piattaforma.',
        }
    )
    moderator_user.set_password('moderator12345')
    moderator_user.email = 'mod@example.com'
    moderator_user.role = 'MODERATOR'
    moderator_user.bio = 'Moderatore ufficiale della piattaforma.'
    moderator_user.is_active = True
    moderator_user.save()
    print("Utente pronto: mod_demo / moderator12345")

    standard_user, created = User.objects.get_or_create(
        username='user_demo',
        defaults={
            'email': 'user@example.com',
            'role': 'STANDARD',
            'bio': 'Ciao! Sono un utente standard del social network.',
        }
    )
    standard_user.set_password('user12345')
    standard_user.email = 'user@example.com'
    standard_user.role = 'STANDARD'
    standard_user.bio = 'Ciao! Sono un utente standard del social network.'
    standard_user.is_active = True
    standard_user.save()
    print("Utente pronto: user_demo / user12345")

    user_maria, created = User.objects.get_or_create(
        username='maria_demo',
        defaults={
            'email': 'maria@example.com',
            'role': 'STANDARD',
            'bio': 'Appassionata di tecnologia, viaggi e cucina.',
        }
    )
    user_maria.set_password('maria12345')
    user_maria.email = 'maria@example.com'
    user_maria.role = 'STANDARD'
    user_maria.bio = 'Appassionata di tecnologia, viaggi e cucina.'
    user_maria.is_active = True
    user_maria.save()
    print("Utente pronto: maria_demo / maria12345")

    user_luca, created = User.objects.get_or_create(
        username='luca_demo',
        defaults={
            'email': 'luca@example.com',
            'role': 'STANDARD',
            'bio': 'Studente e tester della piattaforma social.',
        }
    )
    user_luca.set_password('luca12345')
    user_luca.email = 'luca@example.com'
    user_luca.role = 'STANDARD'
    user_luca.bio = 'Studente e tester della piattaforma social.'
    user_luca.is_active = True
    user_luca.save()
    print("Utente pronto: luca_demo / luca12345")

    # Pulizia relazioni follow precedenti
    admin_user.following.clear()
    moderator_user.following.clear()
    standard_user.following.clear()
    user_maria.following.clear()
    user_luca.following.clear()

    # Relazioni follow tra utenti
    standard_user.following.add(moderator_user, user_maria)
    user_maria.following.add(standard_user, user_luca)
    user_luca.following.add(standard_user, moderator_user)
    moderator_user.following.add(standard_user)
    print("Relazioni follow create.")

    # Creazione post demo
    post1 = Post.objects.create(
        author=standard_user,
        content="Sto preparando il progetto finale di Back-end per il corso PPM 2026. Django REST Framework è fantastico!"
    )

    post2 = Post.objects.create(
        author=standard_user,
        content="Oggi ho testato autenticazione JWT, permessi personalizzati e creazione dei post tramite API."
    )

    post3 = Post.objects.create(
        author=moderator_user,
        content="Avviso di servizio: mantenete toni rispettosi e costruttivi all'interno della piattaforma."
    )

    post4 = Post.objects.create(
        author=user_maria,
        content="Ho appena pubblicato il mio primo post sulla piattaforma social REST API!"
    )

    post5 = Post.objects.create(
        author=user_luca,
        content="Sto provando feed personalizzato, like e commenti. Tutto funziona correttamente."
    )

    post6 = Post.objects.create(
        author=admin_user,
        content="Account amministratore pronto per la valutazione del progetto e per il pannello Django Admin."
    )

    print("Post demo creati.")

    # Like ai post
    post1.likes.add(admin_user, moderator_user, user_maria)
    post2.likes.add(moderator_user, user_luca)
    post3.likes.add(standard_user, user_maria, user_luca)
    post4.likes.add(standard_user, moderator_user)
    post5.likes.add(standard_user, user_maria, admin_user)
    post6.likes.add(moderator_user, standard_user)

    print("Like demo creati.")

    # Commenti demo
    Comment.objects.create(
        post=post1,
        author=moderator_user,
        content="Ottimo lavoro, continua così!"
    )

    Comment.objects.create(
        post=post1,
        author=user_maria,
        content="Anche io sto studiando DRF, molto interessante!"
    )

    Comment.objects.create(
        post=post2,
        author=user_luca,
        content="JWT configurato bene, utile per proteggere gli endpoint."
    )

    Comment.objects.create(
        post=post3,
        author=standard_user,
        content="Messaggio ricevuto, grazie per l'avviso."
    )

    Comment.objects.create(
        post=post4,
        author=admin_user,
        content="Benvenuta sulla piattaforma demo!"
    )

    Comment.objects.create(
        post=post5,
        author=user_maria,
        content="Il feed personalizzato è una feature molto utile."
    )

    Comment.objects.create(
        post=post6,
        author=moderator_user,
        content="Account admin verificato correttamente."
    )

    print("Commenti demo creati.")

    print("")
    print("Database popolato correttamente!")
    print("")
    print("Account demo disponibili:")
    print("- admin_demo / admin12345 / MODERATOR + SUPERUSER")
    print("- mod_demo / moderator12345 / MODERATOR")
    print("- user_demo / user12345 / STANDARD")
    print("- maria_demo / maria12345 / STANDARD")
    print("- luca_demo / luca12345 / STANDARD")


if __name__ == '__main__':
    popola_database()