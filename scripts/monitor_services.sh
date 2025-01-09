#!/bin/bash
# Monitor services for health checks

set -e

echo "Monitoring services..."

function check_vault() {
    VAULT_STATUS=$(curl -s --header "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/sys/health | jq '.initialized')
    if [ "$VAULT_STATUS " == "true" ]; then
        echo "Vault is healthy."
    else
        echo "Vault is not healthy."
    fi
}

function check_redis() {
    REDIS_STATUS=$(redis-cli ping)
    if [ "$REDIS_STATUS" == "PONG" ]; then
        echo "Redis is healthy."
    else
        echo "Redis is not healthy."
    fi
}

function check_django() {
    DJANGO_STATUS=$(curl -s http://127.0.0.1:8000/health/ |jq '.status')
    if [ "$DJANGO_STATUS" == "\"ok"\"]; then
        echo "Django is healthy."
    else
        echo "Django is not healthy."
    fi
}

check_vault
check_redis
check_django