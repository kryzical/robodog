#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to display usage
usage() {
    echo "Usage: $0 [up|down|build]"
    echo "  up    - Start the simulation"
    echo "  down  - Stop the simulation"
    echo "  build - Rebuild the Docker image"
    exit 1
}

# Check if a command was provided
if [ $# -ne 1 ]; then
    usage
fi

case "$1" in
    up)
        docker compose -f "$SCRIPT_DIR/docker/docker-compose.yml" up
        ;;
    down)
        docker compose -f "$SCRIPT_DIR/docker/docker-compose.yml" down
        ;;
    build)
        docker compose -f "$SCRIPT_DIR/docker/docker-compose.yml" build
        ;;
    *)
        usage
        ;;
esac 