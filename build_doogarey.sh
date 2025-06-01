#!/bin/bash

# Build script for Doogarey Agent Zero
echo "🚀 Building Doogarey Agent Zero Docker Image"
echo "============================================="

# Set variables
IMAGE_NAME="agent-zero-doogarey"
TAG="${1:-latest}"
CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S)

echo "📦 Building image: $IMAGE_NAME:$TAG"
echo "🕒 Cache date: $CACHE_DATE"

# Build the Docker image
docker build \
  -f Dockerfile.doogarey \
  -t "$IMAGE_NAME:$TAG" \
  --build-arg BRANCH=local \
  --build-arg CACHE_DATE="$CACHE_DATE" \
  .

if [ $? -eq 0 ]; then
  echo "✅ Build completed successfully!"
  echo "🏷️  Image: $IMAGE_NAME:$TAG"
  echo ""
  echo "To run the container:"
  echo "docker run -d -p 50001:80 --name agent-zero-doogarey $IMAGE_NAME:$TAG"
  echo ""
  echo "To push to a registry:"
  echo "docker tag $IMAGE_NAME:$TAG your-registry.com/$IMAGE_NAME:$TAG"
  echo "docker push your-registry.com/$IMAGE_NAME:$TAG"
else
  echo "❌ Build failed!"
  exit 1
fi