#!/bin/bash

source .env

# Vault Settings
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='${VAULT_TOKEN}'
VAULT_PORT=8200

# Elasticsearch Settings
export ELASTICSEARCH_HOST='http://localhost:9200'
export ELASTICSEARCH_INDEX='django-logs'
ELASTICSEARCH_PORT=9200

# Add the project directory to PYTHONPATH using pwd
PROJECT_DIR="$(pwd)"

if [[ ":$PYTHONPATH:" != *":$PROJECT_DIR:"* ]]; then
    export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
    echo "Added $PROJECT_DIR to PYTHONPATH."
else
    echo "$PROJECT_DIR is already in PYTHONPATH."
fi

# Function to check port occupancy
check_port_usage() {
    local port=$1
    local name=$2

    echo "Checking if port $port ($name) is busy..."
    PID=$(lsof -ti tcp:$port)
    if [ -n "$PID" ]; then
        echo "Port $port ($name) is busy (used by process $PID). Killing process..."
        if ! kill -9 $PID; then
            echo "Failed to kill process $PID on port $port ($name)."
            exit 1
        fi
        echo "Process $PID killed. Port $port ($name) is now free."
    else
        echo "Port $port ($name) is free."
    fi
}

# Check ports for Vault and Elasticsearch
check_port_usage $VAULT_PORT "Vault"
check_port_usage $ELASTICSEARCH_PORT "Elasticsearch"

# Start Vault
echo "Starting Vault Server in Development Mode..."
vault server -dev > vault.log 2>&1 &
sleep 5  # Wait for Vault to start

# Vault availability check
if curl -s "$VAULT_ADDR/v1/sys/health" | grep '"sealed":false' > /dev/null; then
    echo "Vault is running on $VAULT_ADDR."
else
    echo "Vault is not available on $VAULT_ADDR. Please check your configuration."
    cat vault.log
    exit 1
fi

# View key Django configuration information
echo "===================================="
echo "Environment Variables:"
echo "Project Directory:       $PROJECT_DIR"
echo "PYTHONPATH:              $PYTHONPATH"
echo "Elasticsearch Host:      $ELASTICSEARCH_HOST"
echo "Elasticsearch Index:     $ELASTICSEARCH_INDEX"
echo "===================================="

# Start the Django server
echo "Starting Django server..."
python dj_rest/manage.py runserver
