# TAC Semantic Mapping System Implementation Specification

## Project Overview

The TAC Semantic Mapping System is a Flask-based web application designed to intelligently match transaction data from uploaded Excel files against a master dataset. It uses a hybrid approach combining semantic matching (using sentence-transformers) and fuzzy string matching to accurately predict transaction types, even when exact matches are not available.

## Technical Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python     | 3.8+    | Core programming language |
| Flask      | 2.0.1   | Web framework for file upload and processing |
| pandas     | 1.3.3   | Excel file processing and data manipulation |
| fuzzywuzzy | 0.18.0  | Character-level string matching (fallback) |
| sentence-transformers | 2.2.2 | Semantic text matching (primary method) |
| numpy      | 1.21.2  | Mathematical operations for embedding calculations |
| openpyxl   | 3.0.9   | Excel file reading/writing with cell formatting |
| annoy      | 1.17.0  | Approximate nearest neighbor search for faster semantic matching |
| PyJWT      | 2.4.0+  | JWT token generation and validation for API authentication |
| Werkzeug   | 2.0.1+  | Secure filename handling for file uploads |

## System Architecture

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  User Upload (B.xlsx) │────>│  Processing Engine  │────>│  Result File (C.xlsx) │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
          ↑                         │                         ↑
          │                         │                         │
          │                         ↓                         │
          │                     ┌─────────────────────┐       │
          │                     │                     │       │
          └─────────────────────│  Master Dataset     │───────┘
                                │  (A.xlsx)          │
                                │                     │
                                └─────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  API Request        │────>│  Processing Engine  │────>│  API Response       │
│  (JSON)             │     │                     │     │  (JSON)             │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
          ↑                         │                         ↑
          │                         │                         │
          │                         │                         │
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                                    │
                                    ↓
                              ┌─────────────────────┐
                              │                     │
                              │  Master Dataset     │
                              │  (A.xlsx)          │
                              │                     │
                              └─────────────────────┘
```

## Core Functionality

### 1. Semantic Matching Engine

The system uses the `all-MiniLM-L6-v2` model from sentence-transformers to generate text embeddings for SUB_MATERIAL_NAME values. These embeddings capture semantic meaning, allowing the system to recognize that "PnP Destroy" and "PnP Scrap" are semantically similar.

**Key Implementation:**

```python
# Model local storage path
MODEL_DIR = 'models/all-MiniLM-L6-v2'

# Try to load model from local directory, download and save if not exists
if os.path.exists(MODEL_DIR):
    print("Loading model from local directory...")
    model = SentenceTransformer(MODEL_DIR)
else:
    print("Downloading model from Hugging Face...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Save model to local directory
    print("Saving model to local directory...")
    model.save(MODEL_DIR)
```

### 2. Hybrid Matching Strategy

For SUB_MATERIAL_NAME, the system combines both semantic matching and fuzzy string matching using weighted averaging:

- Semantic matching score: 90% weight
- Fuzzy string matching score: 10% weight

**Combined Scoring Logic:**

```python
# For SUB_MATERIAL_NAME, use both semantic similarity and fuzzy matching
current_fuzzy_score = fuzz.token_sort_ratio(str(sub_material_name), str(master_sub_material))
current_semantic_score = 0

if use_semantic_matching and model:
    try:
        # Generate embeddings for both strings
        embedding1 = model.encode(str(sub_material_name))
        embedding2 = model.encode(str(master_sub_material))
        # Calculate cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        current_semantic_score = (dot_product / (norm1 * norm2)) * 100 if (norm1 * norm2) > 0 else 0
        # Use weighted average of semantic and fuzzy scores
        sub_material_score = (current_semantic_score * 0.9 + current_fuzzy_score * 0.1)
        matching_method = 'AISemanticMapping'  # Using semantic mapping
    except Exception as e:
        print(f"Error in semantic matching: {str(e)}")
        # Fallback to fuzzy matching only if semantic similarity fails
        sub_material_score = current_fuzzy_score
        matching_method = 'FuzzyMapping'  # Using only fuzzy mapping
else:
    # Use fuzzy matching only
    sub_material_score = current_fuzzy_score
    matching_method = 'FuzzyMapping'  # Using only fuzzy mapping

# Give more weight to SUB_MATERIAL_NAME as it's the most important for semantic matching
combined_score = (material_score * 0.2 + sub_material_score * 0.6 + uom_score * 0.2)
```

### 3. Result Processing

The system processes uploaded files and generates a result file with the following enhancements:

- **TRANSACTION_TYPE** prediction based on best match
- **Match Type** column indicating the matching method used:
  - "Exact Match": When all three fields match exactly
  - "AISemanticMapping": When semantic matching was used
  - "FuzzyMapping": When only fuzzy string matching was used
  - "Unknown": When no match could be found
- **Enhanced Score Columns**:
  - "Semantic Score": Semantic similarity score (0-100)
  - "Fuzzy Score": Fuzzy string matching score (0-100)
  - "Final Combined Score": Weighted average of semantic and fuzzy scores
  - "Matched Master SUB_MATERIAL_NAME": The master SUB_MATERIAL_NAME value that was matched
- **Excel Cell Formatting**:
  - Red fill for "Final Combined Score" < 70
  - Red fill for "Semantic Score" < 50
  - Yellow fill for "SUB_MATERIAL_NAME" columns with values
- **Result File Naming**: `MappingResult_{timestamp}.xlsx` with timestamp for uniqueness
- **Confidence scores** for each match (stored internally)

## Directory Structure

```
TAC_SemanticMapping_APIEmbedding/
├── app.py                  # Core application file
├── requirements.txt        # Dependencies file
├── templates/              # Flask templates directory
├── models/                 # Model storage directory
├── uploads/                # Prediction files directory
├── knowledge_base/         # Knowledge base files directory
├── results/                # Result files directory
├── Update Knowledge Base log/  # Knowledge base update logs
├── Upload and Process log/     # File processing logs
├── __pycache__/            # Python compilation cache
├── test_files/             # Test files directory
├── api_samples/            # API samples directory
├── documentation/          # Documentation directory
├── backups/                # Backup files directory
└── other_files/            # Other files directory
```

## Code Structure

### Main Components

| Component | File | Description |
|-----------|------|-------------|
| Web Interface | app.py | Flask routes for file upload and processing |
| Processing Engine | app.py (process_excel function) | Core matching logic |
| Model Management | app.py (model loading section) | Handles local model storage and loading |
| Result Generation | app.py (process_excel function) | Creates output file with predictions and enhanced score columns |

### Key Functions

#### process_excel(file_path)

**Purpose:** Processes the uploaded Excel file (Dataset B) against the master file (Dataset A)

**Parameters:**
- `file_path`: Path to the uploaded Excel file

**Returns:**
- Tuple containing: (output_file_path, error_message)

**Processing Steps:**
1. Load master file (A.xlsx) and user file
2. Check for required columns
3. Create lookup dictionary for exact matches
4. Process each row in user file:
   - Check for exact match first
   - If no exact match, perform semantic/fuzzy matching
   - Calculate weighted combined score
   - Select best match above threshold (70)
5. Add "Match Type" column
6. Save result to C.xlsx

#### allowed_file(filename)

**Purpose:** Validates that uploaded files are Excel files

**Parameters:**
- `filename`: Name of the uploaded file

**Returns:**
- Boolean indicating if file is allowed

## Installation and Deployment

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Victor-Huang-Yan/TACMappingTest-Semantic.git
   cd TACMappingTest-Semantic
   ```

2. **Install dependencies:**
   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open browser to http://localhost:5000/

### Dependencies

The `requirements.txt` file includes:

```
Flask
pandas
openpyxl
fuzzywuzzy
sentence-transformers
numpy
annoy
PyJWT
Werkzeug
```

## Usage Guide

### Uploading Master Dataset (A.xlsx)

1. **Web Interface Method:**
   - Navigate to http://localhost:5000/admin
   - Upload your master Excel file (any name)
   - The file will be saved as `knowledge_base/A.xlsx`

2. **Direct File Method:**
   - Place any Excel file in the `knowledge_base/` directory
   - The file watcher will automatically detect and process it
   - The file will be copied to `knowledge_base/A.xlsx`
   - Embeddings will be regenerated automatically

### Processing Transaction Data (B.xlsx)

1. **Web Interface Method:**
   - Navigate to http://localhost:5000/
   - Upload your transaction data file (any name)
   - Click "Upload and Process"
   - The system will process the file and generate `MappingResult_{timestamp}.xlsx` for download
   - The result file will include predicted TRANSACTION_TYPE, Match Type, and enhanced score columns
   - Low scores will be highlighted in red, and SUB_MATERIAL_NAME columns will be highlighted in yellow

2. **Direct File Method:**
   - Place any Excel file in the `uploads/` directory
   - The file watcher will automatically detect and process it
   - Result file will be generated in the `results/` directory
   - No manual intervention required

## Technical Highlights

### 1. Local Model Storage

The system downloads and stores the sentence-transformers model locally in the `models/` directory, ensuring:
- Offline availability
- Faster model loading
- Avoidance of cache-related issues

### 2. Fault Tolerance

The system includes robust error handling:
- Falls back to fuzzy matching if sentence-transformers is not available
- Handles missing files and columns gracefully
- Provides clear error messages to users
- Automatic fallback to optimized linear search if Annoy library is unavailable

### 3. Performance Optimization

- **ANN Indexing**: Uses Annoy library to build approximate nearest neighbor index for semantic matching, reducing time complexity from O(N*M) to O(N*logM)
- **Preprocessing and Caching**: Precomputes and caches master file embeddings during application startup to avoid repeated calculations
- **Batch Processing**: Batch computes embedding vectors to reduce Python loop overhead
- **Dictionary Lookups**: Uses dictionary lookups for exact matches (O(1) time complexity)
- **Selective Processing**: Only processes rows with complete data and where exact matches are not found
- **Fast Index Lookup**: O(1) dictionary-based lookup for master items
- **Progress Feedback**: Real-time progress display during file processing

### 4. Match Transparency

The output file includes detailed information about each match, building trust in the system's decisions:
- "Match Type" column indicates the matching method used
- "Semantic Score" and "Fuzzy Score" show the individual scores
- "Final Combined Score" shows the weighted average
- "Matched Master SUB_MATERIAL_NAME" shows which master value was matched
- Visual formatting with color coding for low scores and important columns

This transparency allows users to understand and verify each prediction.

### 5. Automatic File Processing

The system includes intelligent file watchers for:
- **Knowledge Base Directory**: Automatically processes Excel files placed in `knowledge_base/`
- **Prediction Files Directory**: Automatically processes Excel files placed in `uploads/`
- **Result Generation**: Automatically generates result files in `results/` directory
- **Prevent Duplicate Processing**: Prevents duplicate processing with time-based throttling
- **Thread Safety**: Uses locking mechanisms to prevent concurrent processing

### 6. Enhanced Directory Structure

The system uses a clear directory structure for better organization:
- `knowledge_base/`: Dedicated directory for master dataset files
- `uploads/`: Directory for user-uploaded prediction files
- `results/`: Directory for generated result files
- `models/`: Local storage for semantic models
- `logs/`: Dedicated directories for different types of logs

## Example Usage

### Input Data (B.xlsx)

| MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
|---------------|-------------------|-----|------------------|
| MATERIAL_A    | PnP Destroy       | EA  |                  |
| MATERIAL_B    | Assembly          | PC  |                  |

### Master Data (A.xlsx)

| MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
|---------------|-------------------|-----|------------------|
| MATERIAL_A    | PnP Scrap         | EA  | ADJUSTMENT       |
| MATERIAL_B    | Assembly          | PC  | ORDERS           |

### Output Data (C.xlsx)

| MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE | Match Type         | Semantic Score | Fuzzy Score | Final Combined Score | Matched Master SUB_MATERIAL_NAME |
|---------------|-------------------|-----|------------------|--------------------|---------------|-------------|----------------------|----------------------------------|
| MATERIAL_A    | PnP Destroy       | EA  | ADJUSTMENT       | AISemanticMapping  | 85.42         | 60          | 80.34                | PnP Scrap                        |
| MATERIAL_B    | Assembly          | PC  | ORDERS           | Exact Match        | -             | -           | -                    | Assembly                         |

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| sentence-transformers not available | Missing dependency | Install with `pip install --only-binary :all: sentence-transformers` |
| No AISemanticMapping matches | Model not loaded | Check console logs for model loading errors |
| Low matching accuracy | Insufficient master data | Add more examples to knowledge_base/A.xlsx |
| Processing takes too long | Large input file | Split large files into smaller chunks |
| API authentication failed | Authentication is disabled | No authentication required for API access |
| Excel formatting not applied | openpyxl not installed | Install with `pip install openpyxl` |
| File watcher not working | watchdog library not installed | Install with `pip install watchdog` |
| Result files not generated | Results directory missing | System will automatically create the directory |
| Knowledge base not updating | File not in correct directory | Place files in `knowledge_base/` directory |

### Logging

The system provides comprehensive logging for both operations:

**Update Knowledge Base Logs:**
- Stored in "Update Knowledge Base log" folder
- Filename format: `Update Knowledge Base_YYYYMMDDHHSSMM.log`
- Records reading time, data count, vectorization time, and other metrics

**Upload and Process Logs:**
- Stored in "Upload and Process log" folder
- Filename format: `Upload and Process_YYYYMMDDHHSSMM.log`
- Records reading time, data count, vectorization time, vector similarities, and matching statistics

**API Request Logs:**
- Stored in the same log files as Upload and Process operations
- Include API request details and processing times

**Console Logs:**
- Model loading status
- Matching method used for each row
- Error messages for failed operations
- Performance metrics
- API request processing status

## API Integration

The system now provides a RESTful API for programmatic access, allowing external systems to integrate with the semantic mapping functionality.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/map` | POST | Perform semantic mapping for multiple items (no authentication required) |
| `/api/health` | GET | Check API health status (no authentication required) |
| `/api/docs` | GET | Get API documentation (no authentication required) |
| `/api/auth/login` | POST | User login to get access token (currently disabled) |

### `/api/auth/login` Endpoint

**Request Format:**

```json
{
  "username": "testuser1",
  "password": "maersktac901"
}
```

**Response Format:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 72000
}
```

### `/api/map` Endpoint

**Request Format:**

```json
{
  "items": [
    {
      "MATERIAL_NAME": "MATERIAL_A",
      "SUB_MATERIAL_NAME": "PnP Destroy",
      "UOM": "EA"
    }
  ]
}
```

**Headers:**
- No authentication headers required

**Response Format:**

```json
{
  "status": "success",
  "results": [
    {
      "input": {
        "MATERIAL_NAME": "Picking",
        "SUB_MATERIAL_NAME": "PnP Destroy",
        "UOM": "EA"
      },
      "output": {
        "TRANSACTION_TYPE": "ADJUSTMENT",
        "IMLUI_Billable Date": "Column+RECEIPT.EDITDATE",
        "IMLUI_Billable Qty": "Column+RECEIPTDETAIL.QTYRECEIVED",
        "IMLUI_Document ID": "Column+RECEIPT.RECEIPTKEY",
        "Match Type": "AISemanticMapping",
        "Matched Master SUB_MATERIAL_NAME": "PnP Scrap",
        "Semantic Score": 85.42,
        "Fuzzy Score": 60,
        "Final Combined Score": 80.34
      }
    }
  ],
  "metadata": {
    "total_items": 1,
    "processed_items": 1
  }
}
```

### `/api/health` Endpoint

**Response Format:**

```json
{
  "status": "healthy",
  "services": {
    "semantic_matching": true,
    "ann_index": true,
    "master_data": true
  },
  "version": "1.0.0"
}
```

### API Usage Example

```python
import requests
import json

url = "http://localhost:5000/api/map"

payload = {
  "items": [
    {
      "MATERIAL_NAME": "MATERIAL_A",
      "SUB_MATERIAL_NAME": "PnP Destroy",
      "UOM": "EA"
    },
    {
      "MATERIAL_NAME": "MATERIAL_B",
      "SUB_MATERIAL_NAME": "Assembly",
      "UOM": "PC"
    }
  ]
}

# No authentication required
response = requests.post(url, json=payload)
data = response.json()
print(json.dumps(data, indent=2))
```

## Future Enhancements

1. **Model Fine-tuning**: Train the semantic model on domain-specific data for improved accuracy
2. **Batch Processing**: Add support for processing multiple files simultaneously
3. **Web Interface Improvements**: Add progress indicators and more detailed results
4. **Model Selection**: Allow users to choose between different semantic models
5. **API Authentication**: Add authentication mechanisms for API access (currently disabled)
6. **Rate Limiting**: Implement rate limiting for API requests
7. **Extended API Documentation**: Add Swagger UI for interactive API documentation
8. **Advanced File Watcher**: Add more configurable file watcher options
9. **Result Notification**: Add email or webhook notifications for processing completion
10. **Batch API Endpoint**: Add endpoint for processing multiple items in a single request

## Conclusion

The TAC Semantic Mapping System demonstrates how combining semantic matching with traditional fuzzy matching can significantly improve the accuracy of transaction type prediction. By leveraging state-of-the-art NLP techniques while maintaining compatibility with existing systems through fallback mechanisms, it provides a robust solution for intelligent data matching.