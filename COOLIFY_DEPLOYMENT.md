# Coolify Deployment Guide for Doogarey Agent Zero

## Option 1: Build and Push from Local Machine

### 1. Build locally and push to a registry

```bash
# Build the image
cd D:\Development\agent-zero-0.8.4.2\agent-zero-0.8.4.2
.\build_doogarey.bat

# Tag for your registry (replace with your registry details)
docker tag agent-zero-doogarey:latest your-registry.com/agent-zero-doogarey:latest

# Push to registry
docker push your-registry.com/agent-zero-doogarey:latest
```

### 2. Deploy in Coolify
1. Create new application in Coolify
2. Choose "Docker Image" deployment
3. Use image: `your-registry.com/agent-zero-doogarey:latest`
4. Set port mapping: `80` (container) → `your-desired-port` (host)
5. Add environment variables as needed

## Option 2: Git Repository Deployment

### 1. Create a Git Repository
```bash
# In your agent-zero directory
git init
git add .
git commit -m "Initial commit with Doogarey tools"

# Push to your Git service (GitHub, GitLab, etc.)
git remote add origin https://your-git-service.com/your-repo.git
git push -u origin main
```

### 2. Deploy in Coolify
1. Create new application in Coolify
2. Choose "Git Repository" deployment
3. Connect your repository
4. Set Dockerfile path: `Dockerfile.doogarey`
5. Configure build arguments:
   - `BRANCH=local`
   - `CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S)`

## Option 3: Direct File Upload (if Coolify supports it)

1. Create a zip file of your agent-zero directory
2. Upload to Coolify if it supports direct file deployment
3. Use the Dockerfile.doogarey for building

## Environment Configuration

### Required Environment Variables
```
# Doogarey API Configuration
DOOGAREY_API_URL=https://your-doogarey-instance.com
# Add other environment variables as needed
```

### Port Configuration
- Container Port: `80`
- Expose Port: `50001` (or your preferred port)

### Volume Mounts (Optional)
```
# For persistent data
/path/on/host:/a0/memory
/path/on/host:/a0/logs
```

## Docker Compose Alternative

If Coolify supports docker-compose, you can use this:

```yaml
version: '3.8'
services:
  agent-zero-doogarey:
    build:
      context: .
      dockerfile: Dockerfile.doogarey
      args:
        BRANCH: local
        CACHE_DATE: "2024-01-01:00:00:00"
    ports:
      - "50001:80"
    environment:
      - DOOGAREY_API_URL=https://your-doogarey-instance.com
    volumes:
      - ./memory:/a0/memory
      - ./logs:/a0/logs
    restart: unless-stopped
```

## Testing the Deployment

After deployment, test the integration:

1. Access the web interface at `http://your-server:50001`
2. Test basic Agent Zero functionality
3. Test Doogarey tools:
   ```json
   {
     "thoughts": ["Testing Doogarey workspace creation"],
     "tool_name": "doog_workspace",
     "tool_args": {
       "action": "list",
       "api_url": "https://your-doogarey-instance.com"
     }
   }
   ```

## Troubleshooting

### Build Issues
- Check Docker is running
- Verify all files are present
- Check for permission issues

### Runtime Issues
- Verify Doogarey API is accessible
- Check environment variables
- Review container logs: `docker logs container-name`