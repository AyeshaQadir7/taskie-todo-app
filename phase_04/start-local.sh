#!/bin/bash

# Taskie Local Deployment Startup Script
# Starts containers and services for local development

set -e

echo "🚀 Starting Taskie Application (Local Deployment)"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${BLUE}[1/4]${NC} Checking Docker daemon..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"

# Load environment variables
echo -e "${BLUE}[2/4]${NC} Loading environment variables..."
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  backend/.env not found. Please create it first.${NC}"
    exit 1
fi
export $(cat backend/.env | grep -v '^#' | xargs)
echo -e "${GREEN}✓ Environment variables loaded${NC}"

# Check if images exist
echo -e "${BLUE}[3/4]${NC} Verifying Docker images..."
if ! docker image inspect taskie-backend:latest > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Image taskie-backend:latest not found. Please build it first:${NC}"
    echo "   cd backend && docker build -t taskie-backend:latest ."
    exit 1
fi

if ! docker image inspect taskie-frontend:latest > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Image taskie-frontend:latest not found. Please build it first:${NC}"
    echo "   cd frontend && docker build -t taskie-frontend:latest ."
    exit 1
fi
echo -e "${GREEN}✓ Both Docker images found${NC}"

# Stop existing containers if running
echo -e "${BLUE}[4/4]${NC} Starting containers..."
docker stop taskie-backend taskie-frontend 2>/dev/null || true
docker rm taskie-backend taskie-frontend 2>/dev/null || true

# Start backend
echo -e "${BLUE}Starting backend service...${NC}"
docker run -d \
  --name taskie-backend \
  -p 8000:8000 \
  -e DATABASE_URL="${DATABASE_URL}" \
  -e BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET}" \
  -e CORS_ORIGINS="http://localhost:3000,http://localhost:3001" \
  --health-cmd='curl -f http://localhost:8000/health || exit 1' \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  --health-start-period=10s \
  taskie-backend:latest

# Wait for backend to be healthy
echo "Waiting for backend to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if docker exec taskie-backend curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
        break
    fi
    attempt=$((attempt + 1))
    if [ $attempt -eq $max_attempts ]; then
        echo -e "${YELLOW}⚠️  Backend health check timed out. Continuing anyway...${NC}"
    fi
    sleep 1
done

# Start frontend
echo -e "${BLUE}Starting frontend service...${NC}"
docker run -d \
  --name taskie-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" \
  -e NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000" \
  -e BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET}" \
  -e NODE_ENV="production" \
  taskie-frontend:latest

# Wait for frontend to start
sleep 3
if docker ps | grep taskie-frontend > /dev/null; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Taskie Application Started Successfully!${NC}"
echo "=================================================="
echo ""
echo "📍 Access Points:"
echo -e "  ${BLUE}Frontend:${NC}        http://localhost:3000"
echo -e "  ${BLUE}Backend API:${NC}     http://localhost:8000"
echo -e "  ${BLUE}API Docs:${NC}        http://localhost:8000/docs"
echo ""
echo "📊 Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep taskie
echo ""
echo "📝 Useful Commands:"
echo "  View logs:     ./logs.sh [backend|frontend]"
echo "  Stop services: ./stop-local.sh"
echo "  Restart:       ./restart-local.sh"
echo ""
