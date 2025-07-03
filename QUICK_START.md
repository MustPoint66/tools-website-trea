# 🚀 Quick Start Guide - Test All Tools Locally

## Step 1: Start Docker Desktop

1. **Open Docker Desktop** application on your Windows PC
2. **Wait for it to fully start** (you'll see "Engine Running" status)
3. **Verify Docker is running** by opening PowerShell and running:
   ```powershell
   docker info
   ```

## Step 2: Build Your Environment

1. **Open PowerShell** in your project directory:
   ```powershell
   cd "E:\Coding FIles\Tools Website Trea"
   ```

2. **Set execution policy** (if needed):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Build all Docker images** (this will take a few minutes the first time):
   ```powershell
   .\docker-manager.ps1 build
   ```

## Step 3: Start Your Services

### Option A: Development Mode (Recommended for testing)
```powershell
.\docker-manager.ps1 dev
```

### Option B: Production Mode
```powershell
.\docker-manager.ps1 start
```

## Step 4: Access Your Website

Once services are running, open your browser and go to:

- **🌐 Main Website**: http://localhost:3000
- **🔧 API Documentation**: http://localhost:8000/docs
- **📊 Redis Management** (dev mode): http://localhost:8081

## Step 5: Test Your Tools

### PDF Tools Testing
1. Go to http://localhost:3000
2. Navigate to PDF tools section
3. Try these tools:
   - **PDF Merger**: Upload 2+ PDF files and merge them
   - **PDF Splitter**: Upload a PDF and split into pages
   - **PDF Compressor**: Upload a large PDF and compress it
   - **PDF to Image**: Convert PDF pages to images
   - **Image to PDF**: Convert images to PDF

### File Conversion Testing
1. Test various file conversions:
   - **DOCX ↔ PDF**
   - **Excel ↔ PDF** 
   - **PowerPoint ↔ PDF**
   - **Image formats** (JPG, PNG, etc.)

### OCR Testing
1. Upload images with text
2. Test OCR text extraction
3. Try with scanned documents

### AI Chat Testing
1. Upload a PDF document
2. Try the AI chat feature
3. Ask questions about the document content

## Step 6: Monitor Your Services

### View Real-time Logs
```powershell
.\docker-manager.ps1 logs
```

### Check Service Status
```powershell
.\docker-manager.ps1 status
```

### View Specific Service Logs
```powershell
# Backend API logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Background worker logs
docker-compose logs -f celery-worker

# Redis logs
docker-compose logs -f redis
```

## Troubleshooting

### If Services Don't Start
1. **Check Docker Desktop is running**
2. **Check ports are available**:
   ```powershell
   netstat -an | findstr "3000 8000 6379"
   ```
3. **Restart services**:
   ```powershell
   .\docker-manager.ps1 restart
   ```

### If Tools Don't Work
1. **Check backend logs**:
   ```powershell
   docker-compose logs -f backend
   ```
2. **Check worker logs**:
   ```powershell
   docker-compose logs -f celery-worker
   ```
3. **Check file permissions** in uploads/temp folders

### Performance Issues
1. **Increase Docker resources** in Docker Desktop settings:
   - Memory: 4GB+ recommended
   - CPU: 2+ cores recommended
2. **Monitor resource usage**:
   ```powershell
   .\docker-manager.ps1 status
   ```

## File Locations

- **Uploaded Files**: `./uploads/`
- **Temporary Files**: `./temp/`
- **Log Files**: `./logs/`

## Stopping Services

When you're done testing:

```powershell
.\docker-manager.ps1 stop
```

## Complete Cleanup

To remove all containers and images:

```powershell
.\docker-manager.ps1 clean
```

## Testing Checklist

- [ ] Docker Desktop started and running
- [ ] Built all Docker images successfully
- [ ] Started services in dev/prod mode
- [ ] Website accessible at http://localhost:3000
- [ ] API accessible at http://localhost:8000
- [ ] Tested PDF merge functionality
- [ ] Tested PDF split functionality
- [ ] Tested file conversion tools
- [ ] Tested OCR functionality
- [ ] Tested AI chat with PDFs
- [ ] Checked logs for any errors
- [ ] Verified file upload/download works

## Next Steps

Once you've tested locally:

1. **Fix any issues** you find
2. **Add more tools** as needed
3. **Optimize performance** 
4. **Deploy to production** when ready

## Need Help?

If you encounter any issues:

1. Check the logs: `.\docker-manager.ps1 logs`
2. Verify all services are running: `.\docker-manager.ps1 status`
3. Try restarting: `.\docker-manager.ps1 restart`
4. Clean and rebuild: `.\docker-manager.ps1 clean` then `.\docker-manager.ps1 build`

Happy testing! 🎉
