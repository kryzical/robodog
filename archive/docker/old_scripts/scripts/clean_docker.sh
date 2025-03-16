#!/bin/bash

# Print disk usage before cleanup
echo "Disk usage before cleanup:"
df -h

# Print Docker disk usage
echo "Docker disk usage:"
docker system df

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

# Remove all containers
echo "Removing all containers..."
docker rm $(docker ps -aq) 2>/dev/null || true

# Remove unused images
echo "Removing unused images..."
docker image prune -af

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove build cache
echo "Removing build cache..."
docker builder prune -af

# Remove dangling images
echo "Removing dangling images..."
docker rmi $(docker images -f "dangling=true" -q) 2>/dev/null || true

# Prune networks
echo "Pruning networks..."
docker network prune -f

# Complete system prune
echo "Performing complete system prune..."
docker system prune -af

# Print disk usage after cleanup
echo "Disk usage after cleanup:"
df -h 