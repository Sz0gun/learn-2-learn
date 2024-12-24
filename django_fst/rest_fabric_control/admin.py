# dj_rest/rest_fabric_control/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import VaultKey
from rest_fabric_control.utils import FabricControlUtils

@admin.register(VaultKey)
class VaultKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return request.user.has_perm('rest_fabric_control.can_add_to_vault')
    
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('rest_fabric_control.can_delete_from_vault')
    
    # Support for adding keys to Vault
    def save_model(self, request, obj, form, change):
        """
        Saving the VaultKey model and adding keys to Vault.
        """
        utils = FabricControlUtils()
        if not change: # New key
            # Check if the key already exists in Vault
            if utils.validate_vault_key_existence(path='learn-2-learn', key=obj.name):
                raise ValidationError(f"Key '{obj.name}' already exists in Vault.")
        super().save_model(request, obj, form, change)

        # Adding a key to Vault
        try:
            utils.add_key_to_vault(path="learn-2-learn", key=obj.name, value=obj.value)
        except Exception as e:
            raise ValidationError(f"Failed to add key '{obj.name}' to Vault: {e}")