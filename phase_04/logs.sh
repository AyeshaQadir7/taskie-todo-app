#!/bin/bash

# Taskie Logs Viewer
# View logs from running containers

# Colors for output
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SERVICE=${1:-"all"}
FOLLOW=${2:-"-f"}

case $SERVICE in
  backend)
    echo -e "${BLUE}📋 Backend Logs${NC}"
    docker logs $FOLLOW taskie-backend 2>/dev/null || echo -e "${YELLOW}⚠️  Backend container not running${NC}"
    ;;
  frontend)
    echo -e "${BLUE}📋 Frontend Logs${NC}"
    docker logs $FOLLOW taskie-frontend 2>/dev/null || echo -e "${YELLOW}⚠️  Frontend container not running${NC}"
    ;;
  all)
    echo -e "${BLUE}📋 Backend Logs${NC}"
    docker logs $FOLLOW taskie-backend 2>/dev/null || echo -e "${YELLOW}⚠️  Backend container not running${NC}"
    echo ""
    echo -e "${BLUE}📋 Frontend Logs${NC}"
    docker logs $FOLLOW taskie-frontend 2>/dev/null || echo -e "${YELLOW}⚠️  Frontend container not running${NC}"
    ;;
  *)
    echo "Usage: $0 [backend|frontend|all] [-f|--follow|--no-follow]"
    echo ""
    echo "Examples:"
    echo "  $0 backend              # View backend logs with follow"
    echo "  $0 frontend             # View frontend logs with follow"
    echo "  $0 all                  # View all logs with follow"
    echo "  $0 backend --no-follow  # View backend logs without follow"
    ;;
esac
