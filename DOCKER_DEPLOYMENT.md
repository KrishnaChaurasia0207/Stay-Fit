# 🐳 Docker Deployment Guide

## Quick Start

### Prerequisites
- **Docker Desktop** installed and running
- **Docker Compose** (included with Docker Desktop)

### One-Click Startup
**Windows:**
```bash
# Option 1: Batch file
docker-start.bat

# Option 2: PowerShell
docker-start.ps1
```

**Mac/Linux:**
```bash
# Make executable and run
chmod +x docker-start.sh
./docker-start.sh
```

### Manual Startup
```bash
# Build and start all services
docker compose --env-file .env.docker up --build -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Architecture

### Services
- **Backend**: Python FastAPI server (port 8000)
- **Frontend**: React app with Nginx (port 3000)
- **Nginx** (optional): Reverse proxy for production (port 80)

### Network
- All services communicate via `nutrition-network`
- Frontend proxies API requests to backend
- Health checks ensure services are ready

## Configuration

### Environment Variables (.env.docker)
```env
# API Keys
SPOONACULAR_API_KEY=your_key_here
USDA_API_KEY=your_key_here

# Application Settings
VITE_API_URL=http://localhost:8000
ENVIRONMENT=production
```

### Production Mode
```bash
# Start with production reverse proxy
docker compose --profile production up -d
```

## Mobile Access

### Same Network Access
1. **Find your IP**: The startup scripts show your network IP
2. **Phone browser**: Go to `http://YOUR_IP:3000`
3. **Install PWA**: Tap "Add to Home Screen"

### Port Mapping
- **Frontend**: `localhost:3000` → Container port 80
- **Backend**: `localhost:8000` → Container port 8000
- **Nginx**: `localhost:80` → Container port 80 (production only)

## Useful Commands

### Development
```bash
# View service status
docker compose ps

# View logs for specific service
docker compose logs backend
docker compose logs frontend

# Restart a service
docker compose restart backend

# Rebuild and restart
docker compose up --build backend
```

### Debugging
```bash
# Access backend container shell
docker compose exec backend bash

# Access frontend container shell
docker compose exec frontend sh

# View network information
docker network ls
docker network inspect nutrition_network
```

### Data Management
```bash
# Backup nutrition data
docker compose exec backend cp -r /app/data /app/backup

# View container sizes
docker system df

# Clean up unused resources
docker system prune
```

## Deployment Options

### 1. Local Development
```bash
docker compose up -d
```

### 2. Production with Reverse Proxy
```bash
docker compose --profile production up -d
```

### 3. Cloud Deployment

**Docker Hub:**
```bash
# Tag and push images
docker tag nutrition_backend your-username/nutrition-backend
docker tag nutrition_frontend your-username/nutrition-frontend
docker push your-username/nutrition-backend
docker push your-username/nutrition-frontend
```

**DigitalOcean/AWS/GCP:**
- Upload docker-compose.yml
- Set environment variables
- Run `docker compose up -d`

## Performance Tuning

### Resource Limits
Add to docker-compose.yml:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

### Scaling
```bash
# Scale backend horizontally
docker compose up -d --scale backend=3
```

### Health Checks
- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:3000/health`
- All services have automatic health checks

## Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Check what's using ports
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Kill processes if needed
sudo kill -9 $(lsof -ti:3000)
```

**Build failures:**
```bash
# Clean build cache
docker builder prune

# Rebuild from scratch
docker compose build --no-cache
```

**Permission issues:**
```bash
# Fix data directory permissions
sudo chown -R $USER:$USER ./data
```

### Logs and Monitoring
```bash
# Follow all logs
docker compose logs -f

# Backend API logs only
docker compose logs -f backend

# Resource usage
docker stats
```

## Security Considerations

### Production Setup
1. **Change default API keys** in .env.docker
2. **Enable HTTPS** by configuring SSL certificates
3. **Set up firewall rules** for ports 80/443 only
4. **Use secrets management** for sensitive data

### Network Security
```yaml
# In docker-compose.yml, restrict network access
networks:
  nutrition-network:
    driver: bridge
    internal: true  # Prevents external access
```

## Backup and Recovery

### Data Backup
```bash
# Create backup
docker compose exec backend tar -czf /app/backup.tar.gz /app/data

# Copy to host
docker compose cp backend:/app/backup.tar.gz ./backup.tar.gz
```

### Full System Backup
```bash
# Export all containers
docker compose config > docker-compose-backup.yml
docker save $(docker compose images -q) > nutrition-images.tar
```

## Monitoring and Maintenance

### Health Monitoring
```bash
# Check all service health
docker compose ps

# Monitor resource usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Updates
```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

This Docker setup provides a production-ready deployment that's easy to manage and scale!