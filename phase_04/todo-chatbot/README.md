# Taskie Helm Chart

A comprehensive Helm chart for deploying the **Taskie** full-stack todo application on Kubernetes/Minikube.

## Overview

This Helm chart deploys:
- **Backend**: FastAPI REST API (port 8000)
- **Frontend**: Next.js web application (port 3000)

Both services are configured for local development with Minikube or production deployment.

## Quick Start

### For Local Development (Docker Compose)

Use the convenience scripts in the project root:

```bash
# Start all services
./start-local.sh

# View logs
./logs.sh backend|frontend|all

# Stop services
./stop-local.sh

# Restart
./restart-local.sh
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### For Minikube Deployment

See [HELM_DEPLOYMENT_GUIDE.md](../HELM_DEPLOYMENT_GUIDE.md) for detailed instructions.

```bash
# Quick setup
minikube start --cpus=4 --memory=4096

# Build and load images
docker build -t taskie-backend:latest ../backend
docker build -t taskie-frontend:latest ../frontend
minikube image load taskie-backend:latest
minikube image load taskie-frontend:latest

# Deploy
helm install taskie . --values values-minikube.yaml

# Access via port forwarding
kubectl port-forward svc/taskie-backend 8000:8000
kubectl port-forward svc/taskie-frontend 3000:3000
```

## Chart Contents

```
├── Chart.yaml                    # Chart metadata
├── values.yaml                   # Default configuration
├── values-minikube.yaml          # Minikube-optimized values
├── README.md                     # This file
├── templates/
│   ├── _helpers.tpl              # Template helpers
│   ├── backend-deployment.yaml    # Backend deployment
│   ├── backend-service.yaml       # Backend Kubernetes service
│   ├── backend-secrets.yaml       # Backend secrets
│   ├── frontend-deployment.yaml   # Frontend deployment
│   ├── frontend-service.yaml      # Frontend Kubernetes service
│   ├── frontend-secrets.yaml      # Frontend secrets
│   ├── serviceaccount.yaml        # Service account
│   ├── ingress.yaml               # Ingress configuration
│   ├── hpa.yaml                   # Horizontal Pod Autoscaler
│   ├── httproute.yaml             # Gateway API HTTPRoute
│   ├── NOTES.txt                  # Post-install instructions
│   └── tests/
│       └── test-connection.yaml   # Connectivity tests
└── .helmignore                   # Files to ignore
```

## Configuration

### Backend Service

| Setting | Default | Description |
|---------|---------|-------------|
| `backend.replicaCount` | 1 | Number of backend replicas |
| `backend.image.repository` | `taskie-backend` | Container image |
| `backend.image.tag` | `latest` | Image tag |
| `backend.service.port` | 8000 | Service port |
| `backend.env.*` | See values.yaml | Environment variables |

**Required Secrets:**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT signing secret (min 32 chars)

### Frontend Service

| Setting | Default | Description |
|---------|---------|-------------|
| `frontend.replicaCount` | 1 | Number of frontend replicas |
| `frontend.image.repository` | `taskie-frontend` | Container image |
| `frontend.image.tag` | `latest` | Image tag |
| `frontend.service.port` | 3000 | Service port |
| `frontend.env.*` | See values.yaml | Environment variables |

**Required Secrets:**
- `BETTER_AUTH_SECRET` - JWT signing secret (must match backend)

## Installation

### Prerequisites

- Kubernetes 1.19+ or Minikube 1.20+
- Helm 3.0+
- Docker (for local image builds)

### Install

```bash
# Install with default values
helm install taskie ./todo-chatbot

# Install with Minikube values
helm install taskie ./todo-chatbot --values ./todo-chatbot/values-minikube.yaml

# Install in specific namespace
helm install taskie ./todo-chatbot -n taskie --create-namespace

# Install with custom values
helm install taskie ./todo-chatbot \
  --set backend.replicaCount=2 \
  --set frontend.replicaCount=2
```

### Upgrade

```bash
# Upgrade release
helm upgrade taskie ./todo-chatbot

# Rollback to previous version
helm rollback taskie 1
```

### Uninstall

```bash
helm uninstall taskie
```

## Values

### Backend Configuration Example

```yaml
backend:
  replicaCount: 1
  image:
    repository: taskie-backend
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  env:
    DEBUG: "false"
    CORS_ORIGINS: "http://localhost:3000"
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

### Frontend Configuration Example

```yaml
frontend:
  replicaCount: 1
  image:
    repository: taskie-frontend
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000
  env:
    NODE_ENV: "production"
    NEXT_PUBLIC_API_BASE_URL: "http://backend:8000"
```

## Secrets

Update secrets after installation:

```bash
# Edit backend secrets
kubectl edit secret taskie-backend-secrets

# Edit frontend secrets
kubectl edit secret taskie-frontend-secrets
```

Required values:

**Backend Secrets:**
```yaml
database-url: "postgresql+psycopg://user:password@ep-xxx.neon.tech/dbname?sslmode=require"
better-auth-secret: "your-secret-key-minimum-32-characters-long"
```

**Frontend Secrets:**
```yaml
better-auth-secret: "your-secret-key-minimum-32-characters-long"  # Must match backend
```

## Accessing the Application

### Port Forwarding

```bash
# Forward backend (port 8000)
kubectl port-forward svc/taskie-backend 8000:8000

# Forward frontend (port 3000)
kubectl port-forward svc/taskie-frontend 3000:3000

# Access
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
```

### Ingress

If ingress is enabled in values.yaml:

```bash
# Check ingress
kubectl get ingress

# Access via hostname (requires DNS/hosts entry)
# Frontend: http://taskie.local
# Backend:  http://taskie.local/api
```

## Monitoring

### Check Deployment Status

```bash
# View deployments
kubectl get deployments

# View pods
kubectl get pods -l app.kubernetes.io/name=taskie

# View services
kubectl get services -l app.kubernetes.io/name=taskie
```

### View Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/name=taskie,component=backend -f

# Frontend logs
kubectl logs -l app.kubernetes.io/name=taskie,component=frontend -f

# Pod logs
kubectl logs <pod-name>

# Previous pod logs (if crashed)
kubectl logs <pod-name> --previous
```

### Describe Resources

```bash
# Describe pod
kubectl describe pod <pod-name>

# Describe deployment
kubectl describe deployment taskie-backend

# Describe service
kubectl describe svc taskie-backend
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name>
```

### Image pull errors

```bash
# For Minikube, load images
minikube image load taskie-backend:latest
minikube image load taskie-frontend:latest

# Verify images
minikube image list | grep taskie
```

### Secret errors

```bash
# Verify secrets exist
kubectl get secrets

# Check secret content
kubectl get secret taskie-backend-secrets -o jsonpath='{.data}'

# Recreate secrets
kubectl delete secret taskie-backend-secrets taskie-frontend-secrets
# Then update values.yaml and reinstall
```

### Connection issues

```bash
# Test backend from frontend pod
kubectl exec -it <frontend-pod> -- curl http://taskie-backend:8000/health

# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup taskie-backend

# Check service
kubectl get svc taskie-backend -o yaml
```

## Helm Commands

```bash
# List releases
helm list

# Get release values
helm get values taskie

# Get release manifest
helm get manifest taskie

# Template chart (dry-run)
helm template taskie ./todo-chatbot

# Lint chart
helm lint ./todo-chatbot

# Debug template
helm template taskie ./todo-chatbot --debug

# Rollback
helm rollback taskie <revision>
```

## Production Considerations

For production deployment:

1. **Replicas**: Set `replicaCount` >= 2 for HA
2. **Resources**: Adjust CPU/memory limits appropriately
3. **Scaling**: Enable `autoscaling` in values
4. **Persistence**: Add persistent volumes for data
5. **TLS**: Enable ingress TLS/SSL
6. **Monitoring**: Add Prometheus/Grafana
7. **Logging**: Configure centralized logging (ELK, Splunk)
8. **Backup**: Configure database backups
9. **Security**: Use RBAC, network policies, pod security policies

## Support

For issues or questions:
1. Check [HELM_DEPLOYMENT_GUIDE.md](../HELM_DEPLOYMENT_GUIDE.md)
2. Review logs: `kubectl logs <pod-name>`
3. Verify configuration: `helm get values <release>`
4. Check Kubernetes events: `kubectl get events`

## License

Same as Taskie project

## Contributing

Contributions welcome! Please follow project guidelines.
