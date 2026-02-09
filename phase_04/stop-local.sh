#!/bin/bash

# Taskie Local Deployment Stop Script
# Stops all running containers

set -e

echo "🛑 Stopping Taskie Application"
echo "=============================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to stop container
stop_container() {
    local container=$1
    if docker ps | grep -q "$container"; then
        echo -e "${BLUE}Stopping ${container}...${NC}"
        docker stop "$container"
        docker rm "$container"
        echo -e "${GREEN}✓ ${container} stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  ${container} is not running${NC}"
    fi
}

# Stop both containers
stop_container "taskie-backend"
stop_container "taskie-frontend"

echo ""
echo "=============================="
echo -e "${GREEN}✅ All services stopped${NC}"
echo ""
echo "To restart: ./start-local.sh"
echo ""
