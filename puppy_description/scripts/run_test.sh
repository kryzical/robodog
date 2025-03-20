#!/bin/bash

# Exit on any error
set -e

# Generate unique container name
CONTAINER_NAME="puppy_ros_test_${USER}_$(date +%Y%m%d_%H%M%S)"

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    exit 0
}

# Setup trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Start container
echo "Starting container: $CONTAINER_NAME"
docker-compose -f docker-compose.test.yml up -d

# Wait for container to be healthy (max 30 seconds)
echo "Waiting for container to be healthy..."
for i in {1..30}; do
    if docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null | grep -q "healthy"; then
        echo "Container is healthy"
        break
    fi
    echo "Waiting for container health... ($i/30)"
    sleep 1
done

# Copy test script into container
echo "Copying test script into container..."
docker cp scripts/container_test.sh "$CONTAINER_NAME:/tmp/container_test.sh"
docker exec "$CONTAINER_NAME" chmod +x /tmp/container_test.sh

# Run test script inside container
echo "Running tests inside container..."
docker exec "$CONTAINER_NAME" /tmp/container_test.sh

echo "Tests completed successfully!"
exit 0 