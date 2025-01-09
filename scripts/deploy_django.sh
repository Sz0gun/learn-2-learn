#!/bin/bash
# Deploy Django API.

set -e

RUN_MODE=${1:-local}

function deploy_local_django() {
    echo "Starting Django locally..."
    docker run --name django -p 8000:8000 -d \
        -e DJANGO_SETTINGS_MODULE=django_fst.core.settings \
        -e SECRET_KEY="$DJANGO_SECRET_KEY" \
        django_fst:latest
    echo "Django is running locally on port 8000."
}

if [ "$RUN_MODE" == "local" ]; then
    deploy_local_django
elif [ "$RUN_MODE" == "k8s" ]; then
    deploy_k8s_django
else
    echo "Invalid mode specified. Use 'local' or 'k8s'."
    exit 1
fi
