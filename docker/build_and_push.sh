#!/bin/bash

# Check if GitHub username is set
if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GITHUB_USERNAME environment variable is not set"
    echo "Please set it with: export GITHUB_USERNAME=yourusername"
    exit 1
fi

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    echo "Please set it with: export GITHUB_TOKEN=your_personal_access_token"
    exit 1
fi

# Set version tag (default to latest if not specified)
TAG=${TAG:-latest}

# Login to GitHub Container Registry
echo "Logging in to GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin

# Build and push terminal image
echo "Building and pushing terminal image..."
docker compose build terminal
docker tag docker-terminal ghcr.io/$GITHUB_USERNAME/puppy_terminal:$TAG
docker push ghcr.io/$GITHUB_USERNAME/puppy_terminal:$TAG

# Build and push simulation image
echo "Building and pushing simulation image..."
docker compose build simulation
docker tag docker-simulation ghcr.io/$GITHUB_USERNAME/puppy_simulation:$TAG
docker push ghcr.io/$GITHUB_USERNAME/puppy_simulation:$TAG

echo "Done! Images have been pushed to GitHub Packages."
echo "You can now use them with:"
echo "  export GITHUB_USERNAME=yourusername"
echo "  docker compose pull"
echo "  docker compose up simulation" 