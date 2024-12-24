from django.db import models

class VaultKey(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='A unique name for the Vault key.'
    )
    value = models.TextField(
        help_text='Vault key value.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'value')
        verbose_name = "Vault Key"
        verbose_name_plural = "Vault Keys"
        permissions = [
            ("can_add_to_vault", "Can add keys to Vault"),
            ("can_read_from_vault", "Can read keys from Vault"),
            ("can_delete_from_vault", "Can delete keys from Vault"),
        ]

    def __str__(self):
        return self.name

