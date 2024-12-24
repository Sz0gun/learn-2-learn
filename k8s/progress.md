# Instalacja Docker
sudo apt update
sudo apt install docker.io -y

# Adding the user to a Docker group to avoid sudo
sudo usermod -aG docker $USER
newgrp docker

# Kind installation
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

```bash
sudo apt update
sudo apt install -y curl gnupg lsb-release
```

# Dodanie oficjalnego klucza GPG Dockera
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

# Dodanie repozytorium Dockera
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
# Instalacja Dockera
```bash
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
```
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
```bash
sudo usermod -aG docker $USER
newgrp docker
```

# Instalacja Kind
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

# Create a cluster
```bash
kind create cluster --name learn2learn
```
info about cluster
```bash
kubectl cluster-info --context kind-learn2learn
kubectl config view
kubectl get nodes
# check a current context
kubectl config current-context
# context switch
kubectl config use-context kind-learn2learn
kubectl get namespaces
```
## Creating certificates (Let's Encrypt)
# Installing Cert-Manager (for automating certificates in Kubernetes):
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```
# CRDs dla Cert-Managera
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.crds.yaml
```
# Check if cert-manager worked correctly
```bash
kubectl create namespace cert-manager
kubectl get all --namespace cert-manager
#checking resources in the cert manager space
kubectl get all --namespace cert-manager
# deploy status logs
kubectl describe deployment cert-manager --namespace cert-manager
# controller logs
kubectl logs deployment/cert-manager --namespace cert-manager
# webhook logs
kubectl logs deployment/cert-manager-webhook --namespace cert-manager
# Verify server API options
kubectl get apiservices
# Verify CRDs (Custom Resource Definitions)
kubectl get crd
# detailed information about webhook resources
kubectl get mutatingwebhookconfigurations
kubectl get validatingwebhookconfigurations
# Check that all Cert-Manager related pods have been started correctly
kubectl get pods --namespace cert-manager
kubectl cluster-info
```

```bash
kubectl apply -f k8s/cert-manager/letsencrypt-clusterissuer.yaml
kubectl get clusterissuer
```

# certificate generation
```bash
kubectl apply -f k8s/cert-manager/l2l-cert.yaml
# Check certificate status
kubectl describe certificate l2l-cert
# Check if the secret has been generated
kubectl get secrets
```
## Configure Nginx as Ingress Controller
# Install Nginx Ingress Controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```
# Update k8s/manifests/ingress.yaml file with certificate support
```bash
kubectl apply -f k8s/manifests/ingress.yaml
# status
kubectl describe ingress learn2learn-ingress
kubectl get ingress

```
```bash
# Check the status of Nginx Ingress Controller:
kubectl get pods -n ingress-nginx
kubectl get ingress -n default
kubectl describe ingress cm-acme-http-solver-vlslg
kubectl get svc -n default
```

#  MetalLB

MetalLB allows you to assign an external IP address to LoadBalancer services in local clusters. After applying MetalLB, the ingress-nginx-controller service will receive an external IP address, allowing it to handle traffic from outside the cluster.
```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml
kubectl apply -f metallb-config.yaml
kubectl get svc -n ingress-nginx # external IP available now

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```
```bash

```