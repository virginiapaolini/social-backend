from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # definizione dei ruoli
    class Role(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard User'
        MODERATOR = 'MODERATOR', 'Moderator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STANDARD
    )
    bio = models.TextField(max_length=500, blank=True)
    # relazione n:n per i follower (Simmetrica=False permette il "segui" non ricambiato)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"