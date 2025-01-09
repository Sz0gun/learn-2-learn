#!/bin/bash
# Initialize and unseal Vault, then configure basic secrets.

# Start Vault in dev mode (or production mode setup if required)
echo "Starting Vault server..."
vault server -dev &

sleep 5

# Export Vault environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable the KV secrets engine
echo "Enabling KV secrets engine..."
vault secrets enable -path=secret kv

# Add initial secrets
echo "Adding initial secrets to Vault..."
vault kv put secret/django DATABASE_URL="..."
vault kv put secret/telegram API_ID="..." API_HASH="..." BOT_TOKEN="..."

# Verify secrets
echo "Verifying secrets in Vault..."
vault kv get secret/django
vault kv get secret/telegram

# Output success message
echo "Vault initialization complete!"