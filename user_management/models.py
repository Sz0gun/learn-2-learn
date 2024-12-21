from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    tg_id = models.BigIntegerField(blank=True, null=True, unique=True, help_text="Telegram User ID")
    tg_username = models.CharField(max_length=150, blank=True, null=True, help_text="Telegram username")
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Conflict resolution
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permission_set',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name='user_permissions',
    )
    def __str__(self):
        return self.username