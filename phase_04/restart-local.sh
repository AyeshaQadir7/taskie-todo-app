#!/bin/bash

# Taskie Local Deployment Restart Script

set -e

echo "🔄 Restarting Taskie Application"
echo "================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Stop services
echo "Stopping services..."
bash "$SCRIPT_DIR/stop-local.sh"

# Wait a moment for cleanup
sleep 2

# Start services
echo ""
echo "Starting services..."
bash "$SCRIPT_DIR/start-local.sh"
