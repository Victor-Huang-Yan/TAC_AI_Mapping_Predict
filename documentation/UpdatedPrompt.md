


          
# Reverse-Generated Prompt

Please create a Flask-based web application for processing Excel file uploads, semantic matching, and downloads with the following requirements:

## Functional Requirements

1. **Web Interface**:
   - Main page: For uploading user Excel files (Dataset B)
   - Admin page: For uploading master Excel files (Dataset A)

2. **File Processing Functionality**:
   - Support uploading .xlsx format Excel files
   - Master file (Dataset A) must be named A.xlsx, stored in the knowledge_base directory
   - User-uploaded files (Dataset B) need to be matched against the master file
   - After processing, generate result file (Dataset C) named MappingResult_{timestamp}.xlsx, stored in the results directory

3. **Intelligent Matching Logic**:
   - Check if user files contain required columns: MATERIAL_NAME, SUB_MATERIAL_NAME, UOM, TRANSACTION_TYPE, IMLUI_Billable Date, IMLUI_Billable Qty, IMLUI_Document ID
   - First attempt exact matching based on MATERIAL_NAME, SUB_MATERIAL_NAME, and UOM
   - If exact match fails, use hybrid matching strategy:
     - For SUB_MATERIAL_NAME: Prioritize semantic matching, fallback to fuzzy matching if unavailable
     - For MATERIAL_NAME and UOM: Use fuzzy string matching
   - Assign different weights to different fields: MATERIAL_NAME (20%), SUB_MATERIAL_NAME (60%), UOM (20%)
   - Only use matching results when the combined matching score exceeds 70

4. **Semantic Matching Implementation**:
   - Use sentence-transformers library and all-MiniLM-L6-v2 model for semantic matching
   - Implement local model storage to avoid dependency on remote cache
   - Add fault tolerance mechanism to automatically fallback to fuzzy matching when semantic matching is unavailable
   - Use both semantic matching and fuzzy matching for SUB_MATERIAL_NAME, with weighted average (semantic matching 70% + fuzzy matching 30%)

5. **Result Output**:
   - Fill matched TRANSACTION_TYPE, IMLUI_Billable Date, IMLUI_Billable Qty, IMLUI_Document ID into user files
   - Add "Match Type" column to mark matching type:
     - "Exact Match": Exact match
     - "AISemanticMapping": Used semantic matching
     - "FuzzyMapping": Only used fuzzy matching
   - Generated result files can be directly downloaded

6. **Error Handling**:
   - Check if master file exists
   - Validate upload file format and required columns
   - Handle various exception cases and display friendly error messages
   - Implement dependency checking to gracefully degrade to fuzzy matching when semantic matching is unavailable

7. **Automatic File Processing**:
   - Implement file watchers for knowledge_base and uploads directories
   - Automatically process Excel files placed in these directories
   - Generate result files in the results directory

## Technical Stack

- Flask framework
- Pandas library (for Excel file processing)
- fuzzywuzzy library (for fuzzy string matching)
- sentence-transformers library (for semantic matching)
- numpy library (for calculating cosine similarity)
- Werkzeug (for secure file upload handling)
- watchdog library (for file system monitoring)

## File Structure

```
app.py
models/
  all-MiniLM-L6-v2/  # Semantic matching model storage directory
templates/
  index.html
  admin.html
knowledge_base/  # Master dataset files directory
uploads/  # User upload files directory
results/  # Result files directory
requirements.txt
```

## Page Design

- Main page: Clean file upload form with upload button and result download link
- Admin page: Form for uploading master files

## Security Requirements

- Limit file size (maximum 16MB)
- Use secure_filename to handle uploaded filenames
- Validate file extensions, only allow .xlsx files

## Deployment Requirements

- Provide clear dependency installation instructions, including using --only-binary option to avoid compilation issues
- Ensure efficient operation on ordinary hardware without GPU acceleration
- Implement local model storage to ensure deployment reliability
- Include automatic directory creation for required folders

Please ensure clear code structure with appropriate comments and handle possible exception cases. Pay special attention to the implementation of semantic matching functionality to ensure it can correctly handle semantically similar but character-different vocabulary, such as "Destroy" and "Scrap."
        