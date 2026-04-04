# TAC_AI_Mapping_Predict
# TAC Semantic Mapping System

## Project Overview

The TAC Semantic Mapping System is an application designed for intelligent matching of transaction data with a master dataset. It leverages semantic matching technology to accurately identify similar items even when exact matches are not available.

## Key Features

- **Intelligent Matching**: Combines exact matching, semantic matching, and fuzzy matching for accurate results
- **Semantic Matching**: Uses sentence-transformers library with all-MiniLM-L6-v2 model for advanced semantic understanding
- **Performance Optimization**: Implements ANN (Approximate Nearest Neighbor) indexing for fast lookup
- **Automatic File Processing**: Monitors directories for new files and processes them automatically
- **REST API Interface**: Provides API endpoints for programmatic access
- **Web Interface**: User-friendly web pages for file uploads and administration
- **Error Handling**: Graceful degradation to fuzzy matching when semantic matching is unavailable
- **Comprehensive Logging**: Detailed logs for performance monitoring and troubleshooting

## Technical Stack

- **Backend**: Python 3.8+, Flask
- **Data Processing**: Pandas, Openpyxl
- **Semantic Matching**: sentence-transformers, NumPy
- **Fuzzy Matching**: fuzzywuzzy, python-Levenshtein
- **Performance Optimization**: Annoy (for ANN indexing)
- **File Monitoring**: watchdog
- **API Documentation**: OpenAPI 3.0

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Windows, macOS, or Linux operating system
- Minimum 4GB RAM (8GB recommended for semantic matching)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Victor-Huang-Yan/TAC_AI_Mapping_Predict.git
   cd TAC_AI_Mapping_Predict
   ```

2. **Install dependencies**:
   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

3. **Create required directories**:
   ```bash
   mkdir -p uploads knowledge_base results models "Update Knowledge Base log" "Upload and Process log"
   ```

4. **Start the server**:
   ```bash
   python app.py
   ```

## Usage

### Web Interface

1. **Access the application**:
   - Main page: http://localhost:5000/
   - Admin page: http://localhost:5000/admin

2. **Upload Master Dataset**:
   - Go to the admin page
   - Upload your master dataset (any Excel file)
   - The system will automatically process it and generate embeddings

3. **Upload Prediction Files**:
   - Go to the main page
   - Upload your Excel file for processing
   - The system will match against the master dataset and return results

### Automatic File Processing

1. **Knowledge Base Updates**:
   - Place Excel files in the `knowledge_base/` directory
   - The system will automatically process them and update the master dataset

2. **Prediction Files**:
   - Place Excel files in the `uploads/` directory
   - The system will automatically process them and generate results in the `results/` directory

### API Usage

#### Endpoints

- **Semantic Mapping**: `POST /api/map`
- **Health Check**: `GET /api/health`
- **API Documentation**: `GET /api/docs`

#### Sample API Request

```python
import requests
import json

url = "http://localhost:5000/api/map"

payload = {
  "items": [
    {
      "MATERIAL_NAME": "Picking",
      "SUB_MATERIAL_NAME": "PnP Destroy",
      "UOM": "EA"
    }
  ]
}

response = requests.post(url, json=payload)
print(response.json())
```

## Directory Structure

```
├── app.py                 # Main application file
├── models/                # Model storage directory
│   └── all-MiniLM-L6-v2/  # Semantic matching model
├── templates/             # HTML templates
│   ├── index.html         # Main page
│   └── admin.html         # Admin page
├── knowledge_base/        # Knowledge base files
├── uploads/               # User upload files
├── results/               # Result files
├── api_samples/           # API usage examples
├── test_files/            # Test scripts
├── documentation/         # Documentation files
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Deployment

### Local Development

For local development, follow the installation steps above.

### Production Deployment

1. **Configure production settings**:
   - Set appropriate environment variables
   - Configure a WSGI server (e.g., Gunicorn)

2. **Example Gunicorn command**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Reverse Proxy**:
   - Use Nginx or Apache as a reverse proxy
   - Configure SSL for secure access

## Performance Optimization

- **ANN Indexing**: Enabled by default for fast semantic matching
- **Embedding Caching**: Precomputes embeddings for master dataset
- **Batch Processing**: Efficiently processes multiple items
- **Fallback Mechanism**: Uses optimized linear search when ANN is unavailable

## Troubleshooting

### Common Issues

| Issue                    | Possible Cause                      | Solution                                                     |
| ------------------------ | ----------------------------------- | ------------------------------------------------------------ |
| No semantic matches      | sentence-transformers not installed | Install with `pip install --only-binary :all: sentence-transformers` |
| Model not loading        | Models directory missing            | Check console logs for model download status                 |
| ANN index not built      | Annoy library not installed         | Install with `pip install --only-binary :all: annoy`         |
| File watcher not working | watchdog library not installed      | Install with `pip install watchdog`                          |
| Slow processing          | Large file size                     | Ensure ANN index is being used                               |

### Log Files

- **Knowledge Base Updates**: `Update Knowledge Base log/`
- **File Processing**: `Upload and Process log/`

## API Documentation

API documentation is available at:
- Local: http://localhost:5000/api/docs
- Remote: http://{server}:{port}/api/docs

## Testing

Run the API test script:

```bash
python test_files/test_api.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- Project Repository: https://github.com/yourusername/TAC_SemanticMapping_APIEmbedding.git
- Technical Support: [Your Contact Information]

## Version History

- **v1.0.0** - Initial release with semantic matching, ANN indexing, and file monitoring

---

**Note**: This system is designed for intelligent semantic matching of transaction data. For optimal performance, ensure you have sufficient memory for the semantic matching model.