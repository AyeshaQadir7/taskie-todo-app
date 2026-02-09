# Taskie Helm Chart - Local Minikube Deployment Guide

This guide explains how to deploy the Taskie application on Minikube using Helm.

## Prerequisites

1. **Docker** - For building images
   ```bash
   docker --version
   ```

2. **Minikube** - For local Kubernetes cluster
   ```bash
   minikube version
   minikube status
   ```

3. **Kubectl** - For Kubernetes CLI
   ```bash
   kubectl version --client
   ```

4. **Helm** - For package management
   ```bash
   helm version
   ```

## Quick Start - Local Docker Deployment (Recommended for Development)

For quick local development, use the provided startup scripts instead of Helm:

```bash
# Start services
./start-local.sh

# View logs
./logs.sh backend     # View backend logs
./logs.sh frontend    # View frontend logs
./logs.sh all         # View all logs

# Stop services
./stop-local.sh

# Restart services
./restart-local.sh
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Helm Deployment on Minikube

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start \
  --cpus=4 \
  --memory=4096 \
  --driver=docker

# Verify Minikube is running
minikube status
kubectl cluster-info
```

### Step 2: Build Docker Images (Local)

```bash
# Build backend image
cd backend
docker build -t taskie-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t taskie-frontend:latest .
cd ..

# Verify images exist
docker images | grep taskie
```

### Step 3: Load Images into Minikube

```bash
# Load backend image
minikube image load taskie-backend:latest

# Load frontend image
minikube image load taskie-frontend:latest

# Verify images are loaded
minikube image list | grep taskie
```

### Step 4: Create Kubernetes Secrets

```bash
# Create namespace (optional)
kubectl create namespace taskie --dry-run=client -o yaml | kubectl apply -f -

# Set environment variables for secrets
export DATABASE_URL="postgresql+psycopg://user:password@ep-xxx.neon.tech/dbname?sslmode=require"
export BETTER_AUTH_SECRET="your-secret-key-minimum-32-characters-long"

# Create backend secrets
kubectl create secret generic taskie-backend-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=better-auth-secret="$BETTER_AUTH_SECRET" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

# Create frontend secrets
kubectl create secret generic taskie-frontend-secrets \
  --from-literal=better-auth-secret="$BETTER_AUTH_SECRET" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

# Verify secrets
kubectl get secrets
```

### Step 5: Enable Ingress (Optional)

```bash
# Enable Ingress addon
minikube addons enable ingress

# Wait for ingress controller to start
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"

# Add to /etc/hosts
echo "$MINIKUBE_IP taskie.local" | sudo tee -a /etc/hosts
```

### Step 6: Deploy with Helm

```bash
# Option A: Deploy with Minikube values
helm install taskie ./todo-chatbot \
  --values ./todo-chatbot/values-minikube.yaml \
  --namespace=default

# Option B: Deploy with default values
helm install taskie ./todo-chatbot \
  --namespace=default

# Verify deployment
helm list
kubectl get all
kubectl get pods
```

### Step 7: Verify Deployment

```bash
# Check pods are running
kubectl get pods
kubectl describe pod taskie-backend-xxxxx
kubectl describe pod taskie-frontend-xxxxx

# Check services
kubectl get svc
kubectl describe svc taskie-backend

# Check deployments
kubectl get deployments

# View logs
kubectl logs -l app.kubernetes.io/name=taskie,component=backend -f
kubectl logs -l app.kubernetes.io/name=taskie,component=frontend -f
```

### Step 8: Access the Application

#### Option A: Port Forwarding

```bash
# Terminal 1: Forward backend
kubectl port-forward svc/taskie-backend 8000:8000

# Terminal 2: Forward frontend
kubectl port-forward svc/taskie-frontend 3000:3000

# Access:
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# Docs:     http://localhost:8000/docs
```

#### Option B: Ingress (if enabled)

```bash
# Access via hostname
# Frontend: http://taskie.local
# Backend:  http://taskie.local/api

# If using port forwarding for ingress:
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80
```

---

## Helm Chart Structure

```
todo-chatbot/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default values
├── values-minikube.yaml       # Minikube-optimized values
├── templates/
│   ├── _helpers.tpl           # Template helpers
│   ├── backend-deployment.yaml # Backend deployment
│   ├── backend-service.yaml    # Backend service
│   ├── backend-secrets.yaml    # Backend secrets
│   ├── frontend-deployment.yaml # Frontend deployment
│   ├── frontend-service.yaml    # Frontend service
│   ├── frontend-secrets.yaml    # Frontend secrets
│   ├── serviceaccount.yaml      # Service account
│   ├── ingress.yaml             # Ingress (if enabled)
│   ├── NOTES.txt                # Post-install notes
│   └── tests/
│       └── test-connection.yaml # Connection test
└── .helmignore
```

---

## Configuration

### Backend Environment Variables

Edit `backend-secrets.yaml` to configure:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT signing secret (min 32 chars)

### Frontend Environment Variables

Edit `frontend-secrets.yaml` to configure:
- `BETTER_AUTH_SECRET` - Must match backend secret

### Customize Deployment

Edit `values-minikube.yaml`:
- `replicaCount` - Number of replicas
- `image.tag` - Image version
- `service.port` - Service port
- `resources` - CPU/memory limits
- `ingress` - Ingress configuration

---

## Common Helm Commands

```bash
# Install
helm install taskie ./todo-chatbot

# Upgrade
helm upgrade taskie ./todo-chatbot

# Rollback
helm rollback taskie 1

# Uninstall
helm uninstall taskie

# Get values
helm get values taskie

# Get manifest
helm get manifest taskie

# Template (dry-run)
helm template taskie ./todo-chatbot

# Lint chart
helm lint ./todo-chatbot

# Debug template
helm template taskie ./todo-chatbot --debug
```

---

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
```

### Images not found

```bash
# Verify images are loaded
minikube image list

# Load image again
minikube image load taskie-backend:latest
minikube image load taskie-frontend:latest
```

### Secrets not found

```bash
# Verify secrets exist
kubectl get secrets

# Check secret values (base64 encoded)
kubectl get secret taskie-backend-secrets -o yaml

# Delete and recreate secrets
kubectl delete secret taskie-backend-secrets
kubectl delete secret taskie-frontend-secrets
# Then run Step 4 again
```

### Ingress not working

```bash
# Verify ingress is enabled
minikube addons list | grep ingress

# Check ingress controller
kubectl get pods -n ingress-nginx

# Test ingress
kubectl get ingress
kubectl describe ingress taskie
```

### Connection issues

```bash
# Test backend health
kubectl exec -it <backend-pod> -- curl http://localhost:8000/health

# Test network connectivity
kubectl exec -it <frontend-pod> -- curl http://taskie-backend:8000/health

# Check DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup taskie-backend
```

---

## Minikube Tips

```bash
# Dashboard
minikube dashboard

# SSH into Minikube
minikube ssh

# View logs
minikube logs
minikube logs -f

# Delete cluster
minikube delete

# Clean up Docker images
docker system prune
```

---

## Production Deployment

For production, use:
1. **Managed Kubernetes** (EKS, GKE, AKS)
2. **Production values** - Adjust `values.yaml`:
   - Higher `replicaCount` for HA
   - Proper `resources` limits
   - Enable `autoscaling`
   - Configure persistent storage
   - Use proper domain names in ingress
   - Enable TLS/SSL

```bash
helm install taskie ./todo-chatbot \
  --values ./todo-chatbot/values.yaml \
  --namespace production
```

---

## Additional Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
- [Taskie Project](https://github.com/your-org/taskie)

---

Happy deploying! 🚀
