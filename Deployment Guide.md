# TAC Semantic Mapping System - Deployment Guide

## Overview

This document provides detailed instructions for deploying TAC Semantic Mapping System from GitHub, including first-time installation, configuration, and rollback procedures.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher (3.11+ recommended)
- **Memory**: Minimum 4GB RAM (8GB recommended for semantic matching)
- **Disk Space**: Minimum 2GB free space (for application and model storage)
- **Network**: Internet connection required for initial model download

### Software Dependencies
- **Git**: For cloning repository
- **pip**: Python package manager
- **Optional**: Virtual environment tool (e.g., venv, conda)

## Deployment Steps

### 1. Clone Repository

```bash
# Clone repository from GitHub
git clone https://github.com/Victor-Huang-Yan/TAC_AI_Mapping_Predict.git

# Navigate to the project directory
cd TAC_AI_Mapping_Predict
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

#### 3.1 Standard Installation (Recommended)

```bash
# Install required packages with binary packages (faster, no compilation)
pip install --only-binary :all: -r requirements.txt
```

#### 3.2 Alternative Installation (if binary packages fail)

```bash
# If --only-binary option is not available, use standard installation
pip install -r requirements.txt

# Note: This may trigger compilation for some packages
# See Troubleshooting section for compilation issues
```

#### 3.3 Optional Performance Enhancements

```bash
# Install python-Levenshtein for faster fuzzy matching
pip install python-Levenshtein

# For GPU acceleration (NVIDIA GPUs only)
# First check CUDA version: nvidia-smi
# Then install appropriate PyTorch version
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 4. Configure Environment

#### 4.1 Create Necessary Directories

```bash
# Create required directories
mkdir -p uploads knowledge_base results models "Update Knowledge Base log" "Upload and Process log"
```

#### 4.2 Update Configuration Settings

Edit `app.py` to update the following settings if needed:

- **Secret Key**: Change `app.secret_key` to a secure value
- **Token Expiration**: Adjust `TOKEN_EXPIRATION` if needed
- **User Credentials**: Update `users` dictionary with your actual users

### 5. Initialize Master Dataset

1. Start the application temporarily to create the uploads directory structure
2. Navigate to `http://localhost:5000/admin`
3. Upload your master dataset (A.xlsx) containing reference data
4. The system will automatically preprocess data and create embeddings

**Note**: During initialization, the application will display performance diagnostics showing:
- Annoy library availability
- Semantic matching status
- Model loading status
- Master dataset statistics

### 6. Start Application

#### Development Mode

```bash
# Start application in development mode
python app.py
```

#### Production Mode (Using Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Start application with Gunicorn
# Replace `workers` with appropriate number for your server
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### 7. Verify Deployment

1. Open a web browser and navigate to `http://localhost:5000`
2. Upload a test file (B.xlsx) to verify processing
3. Check that the result file is generated correctly with formatted scores
4. Test API endpoints using a tool like Postman or curl

## API Authentication

### Generate Access Token

```bash
# Example curl command to get access token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser1", "password": "maersktac901"}'
```

### Use Access Token

```bash
# Example curl command to use the API
curl -X POST http://localhost:5000/api/map \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"items": [{"MATERIAL_NAME": "MATERIAL_A", "SUB_MATERIAL_NAME": "PnP Destroy", "UOM": "EA"}]}'
```

## Configuration Management

### Environment Variables

The following environment variables can be set to configure the application:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment (development/production) | development |
| `FLASK_APP` | Flask application entry point | app.py |
| `SECRET_KEY` | Secret key for session management | your_secret_key_here |

### Master Dataset Configuration

- **File**: `knowledge_base/A.xlsx`
- **Required Columns**: MATERIAL_NAME, SUB_MATERIAL_NAME, UOM, TRANSACTION_TYPE, IMLUI_Billable Date, IMLUI_Billable Qty, IMLUI_Document ID
- **Update Frequency**: As needed via admin interface
- **Alternative Update**: Directly place Excel files in `knowledge_base` directory for automatic processing

## Performance Optimization

### Current Optimizations

The application includes several built-in performance optimizations:

1. **Pre-computed Embeddings**: Master dataset embeddings are computed once during initialization
2. **Fast Index Lookup**: O(1) dictionary-based lookup instead of O(n) linear search
3. **Progress Feedback**: Real-time progress display during file processing
4. **Automatic Fallback**: Graceful degradation if Annoy library is unavailable

### Performance Modes

#### Mode 1: Annoy Index (Best Performance)

**Requirements**: Annoy library successfully installed
**Performance**: 1000x+ faster than linear search
**Installation**: `pip install annoy --only-binary :all:`

#### Mode 2: Optimized Linear Search (Good Performance)

**Requirements**: No additional dependencies
**Performance**: 50-100x faster than naive linear search
**Features**:
- Pre-computed master embeddings
- O(1) index lookup
- Single user embedding per row
- Automatic fallback from Mode 1

#### Mode 3: Naive Linear Search (Baseline)

**Requirements**: None
**Performance**: Baseline (slowest)
**Note**: This mode is only used if both Mode 1 and Mode 2 fail

### GPU Acceleration (Optional)

For NVIDIA GPU acceleration:

1. **Install CUDA-enabled PyTorch**:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

2. **Modify Model Loading** (in `app.py`):
```python
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(MODEL_DIR, device=device)
```

3. **Expected Performance**: 2-10x faster than CPU for large datasets

### Performance Benchmarks

Based on testing with 55 records and 400 master items:

| Mode | Processing Time | Speedup |
|------|----------------|----------|
| Annoy Index | <1 second | 400x |
| Optimized Linear | 4-8 seconds | 50-100x |
| Naive Linear | 399 seconds | 1x (baseline) |

## Rollback Plan

### Version Control

The project uses Git for version control, allowing easy rollback to previous versions.

### Rollback Steps

#### 1. Identify Target Version

```bash
# View commit history
git log --oneline

# Example output:
# a1b2c3d (HEAD -> main) Add API authentication
# d4e5f6g Update Excel formatting
# 7h8i9j0 Initial deployment
```

#### 2. Rollback to Previous Version

```bash
# Rollback to specific commit
git checkout d4e5f6g

# OR rollback by number of commits
git reset --hard HEAD~1
```

#### 3. Reinstall Dependencies (if needed)

```bash
# Reinstall dependencies if they changed
pip install --only-binary :all: -r requirements.txt
```

#### 4. Restore Master Dataset

If the master dataset structure changed, restore the previous version:

```bash
# Restore from backup
cp backups/A.xlsx.old uploads/A.xlsx
```

#### 5. Restart Application

```bash
# Restart application
python app.py
# OR with Gunicorn
# gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Rollback Testing

Before deploying to production, test the rollback procedure in a staging environment to ensure:
- Application starts successfully
- API endpoints function correctly
- Master dataset is properly loaded
- Semantic matching works as expected

## Backup Strategy

### Regular Backups

1. **Master Dataset**: Back up `uploads/A.xlsx` regularly
2. **Configuration**: Back up `app.py` if custom configurations are made
3. **Models**: Back up `models/` directory to avoid re-downloading
4. **Logs**: Archive logs periodically for audit purposes

### Backup Commands

```bash
# Create backup directory if it doesn't exist
mkdir -p backups

# Backup master dataset
cp knowledge_base/A.xlsx backups/A.xlsx.$(date +%Y%m%d)

# Backup models directory
zip -r backups/models_$(date +%Y%m%d).zip models/

# Backup configuration
cp app.py backups/app.py.$(date +%Y%m%d)

# Backup results directory (optional)
zip -r backups/results_$(date +%Y%m%d).zip results/
```

## Monitoring

### Health Checks

Use the API health endpoint to monitor system status:

```bash
# Check system health
curl -X GET http://localhost:5000/api/health \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "semantic_matching": true,
    "ann_index": false,
    "master_data": true
  },
  "version": "1.0.0"
}
```

### Log Monitoring

Monitor the following log files for issues:
- `Update Knowledge Base log/`: For master dataset processing
- `Upload and Process log/`: For transaction processing
- Console output: For real-time errors and warnings

### Performance Monitoring

Key metrics to monitor:
- **Processing Time**: Should be <10 seconds for 100 records (with optimizations)
- **Memory Usage**: Monitor for memory leaks during long-running operations
- **CPU/GPU Usage**: Ensure resources are being utilized efficiently

## Troubleshooting

### Common Deployment Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Annoy installation fails** | "Microsoft Visual C++ 14.0 required" | Install Visual C++ Build Tools or use optimized linear search (automatic fallback) |
| **Model download failure** | Semantic matching disabled | Check internet connection, try manual model download |
| **Memory error** | Application crashes during processing | Increase system RAM, reduce batch size |
| **Port already in use** | Application won't start | Change port in gunicorn command or kill existing process |
| **Permission denied** | Cannot write to directories | Check file permissions, run as appropriate user |
| **API authentication failure** | 401 errors | Verify token format, check user credentials |
| **Slow processing** | Files take minutes to process | Check if Annoy is installed, verify performance diagnostics output |

### Debug Mode

To enable debug mode for troubleshooting:

```bash
# Set debug mode
export FLASK_ENV=development

# Start application
python app.py
```

### Performance Diagnostics

The application displays performance diagnostics on startup:

```
============================================================
PERFORMANCE DIAGNOSTICS
============================================================
Annoy library available: True/False
Semantic matching enabled: True/False
Model loaded: True/False
Master embeddings shape: (400, 384)
Master embeddings count: 400
Master item index mapping: 400 entries
ANN index initialized: True/False
Master dict count: 400
============================================================
```

**Interpretation**:
- `Annoy library available: False` → Application using optimized linear search
- `ANN index initialized: False` → Annoy installation failed or incompatible
- `Master item index mapping: 400 entries` → Fast lookup optimization active

### Annoy Installation Issues

#### Windows

If Annoy installation fails with compilation errors:

**Option 1**: Install Visual C++ Build Tools
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++" workload
3. Retry: `pip install annoy`

**Option 2**: Use optimized linear search (recommended for quick deployment)
- Application will automatically fall back to optimized linear search
- Performance is still 50-100x better than naive implementation
- No additional dependencies required

**Option 3**: Use pre-built wheels
```bash
pip install annoy --only-binary :all:
```

#### Linux/macOS

```bash
# Install build dependencies
# Ubuntu/Debian
sudo apt-get install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"

# macOS
xcode-select --install

# Then install Annoy
pip install annoy
```

### Model Loading Issues

If the model fails to load:

1. **Check available memory**: Ensure at least 2GB free RAM
2. **Verify model files**: Check `models/all-MiniLM-L6-v2/` directory exists
3. **Check PyTorch installation**: `python -c "import torch; print(torch.__version__)"`
4. **Network connectivity**: Required for initial model download

## Scaling Considerations

### Horizontal Scaling

For high-volume deployments:
1. Use a load balancer in front of multiple application instances
2. Share master dataset via network storage (NFS, S3, etc.)
3. Consider using a dedicated vector database for large datasets
4. Implement session affinity for consistent performance
5. Use shared storage for `knowledge_base`, `uploads`, and `results` directories

### Vertical Scaling

For single-server optimization:
1. **Increase RAM**: More memory allows larger master datasets
2. **Add GPU**: Significant performance boost for semantic matching
3. **Use SSD**: Faster disk I/O for model loading and file operations
4. **Optimize CPU**: More cores allow parallel processing

### Performance Tuning

- **Model Caching**: Keep models loaded in memory (default behavior)
- **ANN Index**: Use Annoy index for faster semantic matching
- **Batch Processing**: Process multiple items simultaneously when possible
- **Asynchronous Processing**: Consider Celery for background tasks (future enhancement)

## Security Best Practices

- **API Authentication**: Use strong passwords and HTTPS in production
- **File Uploads**: Validate file types and sizes (16MB limit configured)
- **Error Handling**: Don't expose detailed errors to users
- **Dependency Updates**: Regularly update dependencies to patch vulnerabilities
- **Environment Variables**: Use secure method for storing secrets
- **Token Management**: Implement token refresh mechanism for long-running sessions

## Deployment Checklist

Before deploying to production:

- [ ] All dependencies installed successfully
- [ ] Master dataset uploaded and processed
- [ ] Performance diagnostics show expected configuration
- [ ] API endpoints tested (authentication disabled)
- [ ] File upload/download functionality verified
- [ ] Error handling tested (invalid files, missing columns, etc.)
- [ ] Backup procedures documented and tested
- [ ] Monitoring and logging configured
- [ ] Security measures implemented (HTTPS if exposed to internet)
- [ ] Rollback procedures tested in staging environment
- [ ] File watcher functionality verified for both knowledge_base and uploads directories
- [ ] Results directory access verified
- [ ] Automatic file processing tested

## File Watcher Functionality

The application includes automatic file watchers for:

### 1. Knowledge Base Directory (`knowledge_base/`)
- **Purpose**: Monitor for new or updated master dataset files
- **Behavior**: Automatically processes any Excel file placed in this directory
- **Output**: Copies files to `A.xlsx` and regenerates embeddings
- **Processing**: Preprocesses data and initializes ANN index

### 2. Prediction Files Directory (`uploads/`)
- **Purpose**: Monitor for new or updated prediction files
- **Behavior**: Automatically processes any Excel file placed in this directory
- **Output**: Generates result files in `results/` directory
- **Processing**: Performs semantic matching and generates formatted results

### 3. Results Directory (`results/`)
- **Purpose**: Store generated result files
- **Structure**: `MappingResult_{timestamp}.xlsx`
- **Access**: Results can be accessed directly from this directory
- **Cleanup**: Consider implementing regular cleanup for old results

## Automatic Processing Workflow

1. **Knowledge Base Update**:
   - Place Excel file in `knowledge_base/` directory
   - File watcher detects and processes the file
   - System automatically:
     - Copies file to `A.xlsx`
     - Preprocesses data
     - Generates embeddings
     - Initializes ANN index

2. **Prediction Processing**:
   - Place Excel file in `uploads/` directory
   - File watcher detects and processes the file
   - System automatically:
     - Reads the file
     - Performs semantic matching
     - Generates result file
     - Saves result to `results/` directory

This automatic workflow eliminates the need for manual web interface interactions, providing a seamless way to process files through simple file system operations.

## Conclusion

This deployment guide provides a comprehensive framework for installing and maintaining the TAC Semantic Mapping System. The application includes built-in performance optimizations and graceful fallback mechanisms to ensure reliable operation even in environments with limited dependencies.

Following these procedures will ensure a reliable deployment with minimal downtime and effective rollback capabilities.

For additional support, please refer to project documentation or contact the development team.

---

*Last Updated: April 4, 2026*
*Version: 1.0.0*
