#!/bin/bash
# Deploy and configure Redis service.

set -e

# Check if running locally or on Kubernetes
RUN_MODE=${1:-local}

function deploy_local_redis() {
    echo "Starting Redis localy..."
    docker run --name redis -p 6379:6379 -d redis:latest
    echo "Redis is running locally" on port 6379."
}

function deploy_k8s_redis() {
    echo "Deploing Redis on Kubernetes..."
    kubectl apply -f ../infra/k8s/redis-deployment.yaml
    kubectl apply -f ../infra/k8s/redis-service.yaml
    echo "Redis deployed in Kubernetes cluster."
}

if [ "$RUN_MODE" == "local" ]; then
    deploy_local_redis
elif [ "$RUN_MODE" == "k8s" ]; then
    deploy_k8s_redis
else
    echo "Invalide mode specified. Use 'local' or 'k8s'."
    exit 1
fi