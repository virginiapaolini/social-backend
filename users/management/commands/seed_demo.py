from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Popola il database con gli utenti demo per la valutazione'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creazione account demo in corso...")

        # admin o superuser
        if not CustomUser.objects.filter(username='admin_demo').exists():
            CustomUser.objects.create_superuser(
                username='admin_demo',
                password='admin12345',
                email='admin@example.com',
                role=CustomUser.Role.MODERATOR # gli admin possono fare anche i moderatori
            )
            self.stdout.write(self.style.SUCCESS('Creato admin_demo / admin12345'))

        # utente standard
        if not CustomUser.objects.filter(username='user_demo').exists():
            user = CustomUser.objects.create_user(
                username='user_demo',
                password='user12345',
                email='user@example.com',
                role=CustomUser.Role.STANDARD
            )
            user.bio = "Ciao! Sono un utente standard del social network."
            user.save()
            self.stdout.write(self.style.SUCCESS('Creato user_demo / user12345'))

        # moderatore
        if not CustomUser.objects.filter(username='mod_demo').exists():
            mod = CustomUser.objects.create_user(
                username='mod_demo',
                password='moderator12345',
                email='mod@example.com',
                role=CustomUser.Role.MODERATOR
            )
            mod.bio = "Moderatore ufficiale della piattaforma."
            mod.save()
            self.stdout.write(self.style.SUCCESS('Creato mod_demo / moderator12345'))