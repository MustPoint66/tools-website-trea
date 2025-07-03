# Docker Management Script for Tools Website
# Usage: .\docker-manager.ps1 [command]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "logs", "build", "clean", "status", "dev", "prod", "redis-ui")]
    [string]$Command = "help"
)

$ProjectName = "tools-website"

function Show-Help {
    Write-Host "Docker Management Script for Tools Website" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  start       - Start all services in production mode" -ForegroundColor Green
    Write-Host "  dev         - Start all services in development mode (with live reload)" -ForegroundColor Green
    Write-Host "  stop        - Stop all services" -ForegroundColor Red
    Write-Host "  restart     - Restart all services" -ForegroundColor Yellow
    Write-Host "  build       - Build all Docker images" -ForegroundColor Blue
    Write-Host "  logs        - Show logs from all services" -ForegroundColor Magenta
    Write-Host "  status      - Show status of all services" -ForegroundColor White
    Write-Host "  redis-ui    - Start Redis Commander UI" -ForegroundColor Cyan
    Write-Host "  clean       - Clean up Docker containers and images" -ForegroundColor Red
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\docker-manager.ps1 dev     # Start development environment" -ForegroundColor Gray
    Write-Host "  .\docker-manager.ps1 start   # Start production environment" -ForegroundColor Gray
    Write-Host "  .\docker-manager.ps1 logs    # View all service logs" -ForegroundColor Gray
}

function Start-Services {
    param([bool]$DevMode = $false)
    
    Write-Host "Starting Tools Website services..." -ForegroundColor Cyan
    
    if ($DevMode) {
        Write-Host "🚀 Starting in DEVELOPMENT mode (with live reload)" -ForegroundColor Green
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    } else {
        Write-Host "🚀 Starting in PRODUCTION mode" -ForegroundColor Green
        docker-compose up -d
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Services started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Available services:" -ForegroundColor Yellow
        Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Cyan
        Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Cyan
        Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "  Redis:     localhost:6379" -ForegroundColor Cyan
        if ($DevMode) {
            Write-Host "  Redis UI:  http://localhost:8081" -ForegroundColor Cyan
        }
        Write-Host ""
        Write-Host "Use 'docker-manager.ps1 logs' to see real-time logs" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Failed to start services" -ForegroundColor Red
    }
}

function Stop-Services {
    Write-Host "Stopping Tools Website services..." -ForegroundColor Yellow
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Services stopped successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to stop services" -ForegroundColor Red
    }
}

function Restart-Services {
    Write-Host "Restarting Tools Website services..." -ForegroundColor Yellow
    Stop-Services
    Start-Sleep -Seconds 2
    Start-Services
}

function Show-Logs {
    Write-Host "Showing logs for all services (Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f
}

function Build-Images {
    Write-Host "Building Docker images..." -ForegroundColor Blue
    docker-compose build --no-cache
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Images built successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to build images" -ForegroundColor Red
    }
}

function Show-Status {
    Write-Host "Docker Services Status:" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    docker-compose ps
    
    Write-Host ""
    Write-Host "Docker System Info:" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    docker system df
}

function Start-RedisUI {
    Write-Host "Starting Redis Commander UI..." -ForegroundColor Cyan
    docker-compose --profile debug up -d redis-commander
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Redis Commander started!" -ForegroundColor Green
        Write-Host "🌐 Access at: http://localhost:8081" -ForegroundColor Cyan
    }
}

function Clean-Docker {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor Yellow
    
    # Stop all containers
    Stop-Services
    
    # Remove containers
    Write-Host "Removing containers..." -ForegroundColor Yellow
    docker-compose down --volumes --remove-orphans
    
    # Remove images
    Write-Host "Removing images..." -ForegroundColor Yellow
    docker image prune -f
    
    # Remove volumes (optional)
    $response = Read-Host "Do you want to remove volumes (this will delete Redis data)? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        docker volume prune -f
        Write-Host "✅ Volumes removed" -ForegroundColor Green
    }
    
    Write-Host "✅ Cleanup completed!" -ForegroundColor Green
}

# Check if Docker is running
function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    }
    catch {
        Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        return $false
    }
}

# Main script logic
if (-not (Test-DockerRunning)) {
    exit 1
}

switch ($Command) {
    "start" { Start-Services }
    "dev" { Start-Services -DevMode $true }
    "stop" { Stop-Services }
    "restart" { Restart-Services }
    "logs" { Show-Logs }
    "build" { Build-Images }
    "status" { Show-Status }
    "redis-ui" { Start-RedisUI }
    "clean" { Clean-Docker }
    default { Show-Help }
}
