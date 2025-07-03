# Docker Setup for Tools Website Local Testing

This guide will help you set up and test all the tools in your website locally using Docker.

## Prerequisites

1. **Docker Desktop** installed and running
2. **Git** for version control
3. **PowerShell** (for Windows management script)

## Architecture Overview

The Docker setup includes the following services:

- **Frontend**: Next.js application (Port 3000)
- **Backend**: FastAPI application (Port 8000)
- **Redis**: Cache and task queue (Port 6379)
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled tasks
- **Redis Commander**: Redis management UI (Port 8081, dev only)

## Quick Start

### 1. Build Docker Images

First, build all the Docker images:

```powershell
.\docker-manager.ps1 build
```

### 2. Start Development Environment

For development with live reloading:

```powershell
.\docker-manager.ps1 dev
```

### 3. Start Production Environment

For production-like environment:

```powershell
.\docker-manager.ps1 start
```

## Available Services

Once started, you can access:

- **Website Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Redis Commander** (dev mode): http://localhost:8081

## Management Commands

Use the `docker-manager.ps1` script for easy management:

```powershell
# Start development environment
.\docker-manager.ps1 dev

# Start production environment
.\docker-manager.ps1 start

# Stop all services
.\docker-manager.ps1 stop

# Restart all services
.\docker-manager.ps1 restart

# View logs from all services
.\docker-manager.ps1 logs

# Show service status
.\docker-manager.ps1 status

# Start Redis UI
.\docker-manager.ps1 redis-ui

# Clean up Docker resources
.\docker-manager.ps1 clean

# Show help
.\docker-manager.ps1
```

## Manual Docker Commands

If you prefer using Docker commands directly:

```bash
# Start all services
docker-compose up -d

# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery-worker

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

## Testing Your Tools

### 1. PDF Tools
- Navigate to http://localhost:3000
- Try uploading PDF files and using various tools like merge, split, compress
- Check the backend logs to see processing: `.\docker-manager.ps1 logs`

### 2. File Conversion Tools
- Test different file format conversions
- Upload images, documents, etc.

### 3. OCR Tools
- Upload images with text to test OCR functionality
- Try scanned documents

### 4. AI Chat with PDFs
- Upload a PDF and try the AI chat feature
- Monitor Celery worker logs for background processing

## Environment Variables

Create a `.env` file in the project root with:

```env
# Redis Configuration
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# File Storage
TEMP_DIR=/app/temp
UPLOAD_DIR=/app/uploads

# API Keys (if using AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Development settings
DEBUG=true
LOG_LEVEL=info
```

## Troubleshooting

### Common Issues

1. **Docker not running**
   - Start Docker Desktop
   - Check with: `docker info`

2. **Port conflicts**
   - Stop other services using ports 3000, 8000, 6379, 8081
   - Or modify ports in docker-compose.yml

3. **Build failures**
   - Clean up: `.\docker-manager.ps1 clean`
   - Rebuild: `.\docker-manager.ps1 build`

4. **Service not starting**
   - Check logs: `.\docker-manager.ps1 logs`
   - Check service status: `.\docker-manager.ps1 status`

### Viewing Logs

```powershell
# All services
.\docker-manager.ps1 logs

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery-worker
docker-compose logs -f redis
```

### Debugging

1. **Access Redis directly**:
   ```bash
   docker exec -it tools-redis redis-cli
   ```

2. **Access backend container**:
   ```bash
   docker exec -it tools-backend bash
   ```

3. **Check file processing**:
   - Files are uploaded to `./uploads/`
   - Temporary files in `./temp/`
   - Logs in `./logs/`

## Development Workflow

### Making Changes

1. **Frontend changes**: In dev mode, changes are automatically reflected
2. **Backend changes**: In dev mode, FastAPI auto-reloads
3. **New dependencies**: Rebuild the relevant service
   ```powershell
   docker-compose build backend  # or frontend
   .\docker-manager.ps1 restart
   ```

### Performance Monitoring

- **Redis Commander**: http://localhost:8081 (dev mode)
- **Backend metrics**: http://localhost:8000/health
- **System resources**: `.\docker-manager.ps1 status`

## Production Deployment

For production deployment:

1. Set production environment variables
2. Use: `.\docker-manager.ps1 start`
3. Consider using Docker Swarm or Kubernetes for scaling

## Cleanup

To completely clean up:

```powershell
.\docker-manager.ps1 clean
```

This will:
- Stop all containers
- Remove containers and images
- Optionally remove volumes (Redis data)

## Support

If you encounter issues:

1. Check Docker Desktop is running
2. Verify all required ports are free
3. Check logs for error messages
4. Try rebuilding images
5. Consider cleaning up and starting fresh
