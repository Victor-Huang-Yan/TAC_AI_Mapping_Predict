# TAC Semantic Mapping System Test Manual

## Test Manual Overview

This test manual provides comprehensive instructions for testing the TAC Semantic Mapping System. It includes test cases for verifying the system's core functionality, including exact matching, semantic matching, fuzzy matching fallback, and error handling. The manual is designed to ensure the system correctly predicts transaction types based on uploaded Excel files.

## Prerequisites

Before beginning testing, ensure the following prerequisites are met:

1. **System Requirements:**
   - Python 3.8 or higher
   - Windows, macOS, or Linux operating system
   - Minimum 4GB RAM (8GB recommended for semantic matching)

2. **Software Installation:**
   - All dependencies installed via: `pip install --only-binary :all: -r requirements.txt`
   - Flask server running: `python app.py`

3. **Test Files:**
   - Master dataset file (`A.xlsx`)
   - Test input files (`B1.xlsx`, `B2.xlsx`, etc.)

4. **Access:**
   - Web browser with access to http://localhost:5000/
   - Admin access to http://localhost:5000/admin

## Testing Environment Setup

### Step 1: Start the Server

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd d:\Private\AI\AI_Expert\Trae Project\TAC_SemanticMapping_APIEmbedding
   ```
3. Start the Flask server:
   ```bash
   python app.py
   ```
4. Verify the server is running by checking the console output:
   ```
   * Running on http://0.0.0.0:5000/
   * Debug mode: on
   ```
5. Check for model loading and preprocessing messages:
   ```
   Attempting to initialize semantic matching...
   Successfully imported numpy version: x.x.x
   Successfully imported sentence-transformers
   Attempting to load model...
   Loading model from local directory: models/all-MiniLM-L6-v2
   Model loaded successfully from local directory
   Semantic matching enabled: True
   Preprocessing master file...
   Preprocessed X embeddings for master file
   ANN index built successfully with X items
   ```

### Step 2: Upload Master Dataset

1. Open a web browser and go to http://localhost:5000/admin
2. Click "Choose File" and select your `A.xlsx` master dataset
3. Click "Upload Master File"
4. Verify the success message: "Master file (A.xlsx) uploaded successfully!"

## Test Cases

### Test Case 1: Exact Match Test

**Objective:** Verify the system correctly identifies exact matches between input data and master dataset.

**Test Data:**

- **Master File (A.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
  |---------------|-------------------|-----|------------------|
  | MATERIAL_A    | Assembly          | PC  | ORDERS           |
  | MATERIAL_B    | Disassembly       | EA  | ADJUSTMENT       |

- **Input File (B1.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
  |---------------|-------------------|-----|------------------|
  | MATERIAL_A    | Assembly          | PC  |                  |
  | MATERIAL_B    | Disassembly       | EA  |                  |

**Expected Results:**
- All rows should show "Exact Match" in the "Match Type" column
- TRANSACTION_TYPE should be correctly populated from master dataset

**Pass Criteria:**
- Both rows show "Exact Match" in Match Type
- TRANSACTION_TYPE values match master dataset exactly

### Test Case 2: Semantic Matching Test

**Objective:** Verify the system correctly uses semantic matching to identify similar SUB_MATERIAL_NAME values (e.g., "PnP Destroy" vs "PnP Scrap").

**Test Data:**

- **Master File (A.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE | IMLUI_Billable Date | IMLUI_Billable Qty | IMLUI_Document ID |
  |---------------|-------------------|-----|------------------|---------------------|---------------------|---------------------|
  | MATERIAL_NAME | PnP Scrap         | EA  | ADJUSTMENT       | 2024-01-01          | 10                  | DOC-001             |

- **Input File (B2.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE | IMLUI_Billable Date | IMLUI_Billable Qty | IMLUI_Document ID |
  |---------------|-------------------|-----|------------------|---------------------|---------------------|---------------------|
  | MATERIAL_NAME | PnP Destroy       | EA  |                  | 2024-01-02          | 5                   | DOC-002             |

**Expected Results:**
- Row should show "AISemanticMapping" in the "Match Type" column
- TRANSACTION_TYPE should be predicted as "ADJUSTMENT"
- Enhanced score columns should be populated:
  - "Semantic Score": Should be > 70
  - "Fuzzy Score": Should be > 50
  - "Final Combined Score": Should be > 65
  - "Matched Master SUB_MATERIAL_NAME": Should be "PnP Scrap"

**Pass Criteria:**
- Match Type is "AISemanticMapping"
- TRANSACTION_TYPE is "ADJUSTMENT"
- All enhanced score columns are populated with appropriate values
- Matched Master SUB_MATERIAL_NAME is "PnP Scrap"

### Test Case 3: Fuzzy Matching Fallback Test

**Objective:** Verify the system falls back to fuzzy matching when semantic matching is unavailable.

**Test Setup:**
1. Temporarily rename or remove the `models` directory to simulate sentence-transformers unavailability

**Test Data:**

- **Master File (A.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
  |---------------|-------------------|-----|------------------|
  | MATERIAL_A    | Assembly          | PC  | ORDERS           |

- **Input File (B3.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE |
  |---------------|-------------------|-----|------------------|
  | MATERIAL_A    | Assmbly           | PC  |                  |

**Expected Results:**
- Row should show "FuzzyMapping" in the "Match Type" column
- TRANSACTION_TYPE should be predicted as "ORDERS"

**Pass Criteria:**
- Match Type is "FuzzyMapping"
- TRANSACTION_TYPE is "ORDERS"

### Test Case 4: Error Handling Test

**Objective:** Verify the system handles missing files and invalid data gracefully.

**Test Scenarios:**

1. **Missing Master File:**
   - Delete `knowledge_base/A.xlsx`
   - Upload test file B1.xlsx
   - Expected: Error message "Master file (A.xlsx) not found. Please upload it first."

2. **Missing Required Columns:**
   - Create input file without SUB_MATERIAL_NAME column
   - Upload file
   - Expected: Error message "Uploaded file is missing required columns."

3. **Empty Input File:**
   - Create blank Excel file
   - Upload file
   - Expected: System handles gracefully (no crash)

**Pass Criteria:**
- System displays appropriate error messages
- System does not crash
- User is redirected to appropriate page

### Test Case 5: Performance Test

**Objective:** Verify the system handles large files efficiently with ANN indexing.

**Test Data:**
- **Master File (A.xlsx):** 1000 rows
- **Input File (B5.xlsx):** 500 rows

**Expected Results:**
- Processing completes within 1 minute (with ANN indexing)
- No system crashes or timeouts
- All rows processed correctly
- ANN index is used for semantic matching

**Pass Criteria:**
- Processing time < 1 minute
- All 500 rows processed
- No errors during processing
- Console shows "ANN index built successfully" message
- Log files generated with performance metrics

## Test Data Preparation

### Creating Test Excel Files

1. **Master File (A.xlsx):**
   - Required columns: MATERIAL_NAME, SUB_MATERIAL_NAME, UOM, TRANSACTION_TYPE, IMLUI_Billable Date, IMLUI_Billable Qty, IMLUI_Document ID
   - Populate with test data covering various scenarios

2. **Input Files (B*.xlsx):**
   - Same required columns as master file
   - Leave TRANSACTION_TYPE blank for testing
   - Populate other columns with test data

### Sample Test Data

**Semantic Matching Test Data:**

- **Master File (A.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE | IMLUI_Billable Date | IMLUI_Billable Qty | IMLUI_Document ID |
  |---------------|-------------------|-----|------------------|---------------------|---------------------|---------------------|
  | MATERIAL_NAME | PnP Scrap         | EA  | ADJUSTMENT       | 2024-01-01          | 10                  | DOC-001             |

- **Input File (B2.xlsx):**
  | MATERIAL_NAME | SUB_MATERIAL_NAME | UOM | TRANSACTION_TYPE | IMLUI_Billable Date | IMLUI_Billable Qty | IMLUI_Document ID |
  |---------------|-------------------|-----|------------------|---------------------|---------------------|---------------------|
  | MATERIAL_NAME | PnP Destroy       | EA  |                  | 2024-01-02          | 5                   | DOC-002             |

## Test Execution Steps

### General Test Execution Flow

1. **Start the Flask Server:**
   ```bash
   cd d:\AI\AI_Expert\TraeProject\TAC_SemanticMapping_Bert
   python app.py
   ```
2. **Upload Master Dataset:**
   - **Web Interface Method:**
     - Navigate to http://localhost:5000/admin
     - Upload your master dataset (any name)
     - Verify upload success
     - Check for log file generation in "Update Knowledge Base log" folder
   - **Direct File Method:**
     - Place any Excel file in the `knowledge_base/` directory
     - File watcher will automatically process it
     - Check console for processing status
3. **Execute Test Case:**
   - **Web Interface Method:**
     - Navigate to http://localhost:5000/
     - Upload test input file (e.g., `B1.xlsx`)
     - Click "Upload and Process"
     - Wait for file to download automatically
   - **Direct File Method:**
     - Place test input file in the `uploads/` directory
     - File watcher will automatically process it
     - Result file will be generated in `results/` directory
4. **Verify Results:**
   - **Web Interface Method:**
     - Open downloaded `MappingResult_*.xlsx` file
     - Check "Match Type" column
     - Verify "TRANSACTION_TYPE" predictions
     - Compare with expected results
     - Check log file in "Upload and Process log" folder for performance metrics
   - **Direct File Method:**
     - Open result file from `results/` directory
     - Check "Match Type" column
     - Verify "TRANSACTION_TYPE" predictions
     - Compare with expected results
     - Check log file in "Upload and Process log" folder for performance metrics

## Result Verification

### Verification Checklist

For each test case, verify:

1. **Match Type Column:**
   - Exact matches show "Exact Match"
   - Semantic matches show "AISemanticMapping"
   - Fuzzy matches show "FuzzyMapping"

2. **TRANSACTION_TYPE Prediction:**
   - Correctly populated from master dataset
   - Matches expected value for test case

3. **Enhanced Score Columns:**
   - "Semantic Score": Populated for semantic matches
   - "Fuzzy Score": Populated for all non-exact matches
   - "Final Combined Score": Populated for all non-exact matches
   - "Matched Master SUB_MATERIAL_NAME": Populated for all non-exact matches

4. **Other Columns:**
   - IMLUI_Billable Date, IMLUI_Billable Qty, IMLUI_Document ID correctly populated
   - No unexpected changes to original data

5. **System Behavior:**
   - No crashes or timeouts
   - Appropriate error messages for invalid inputs
   - File downloads successfully

## Troubleshooting

### Common Testing Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| No AISemanticMapping matches | sentence-transformers not installed | Install with `pip install --only-binary :all: sentence-transformers` |
| Model not loading | Models directory missing | Check console logs for model download status |
| ANN index not built | Annoy library not installed | Install with `pip install --only-binary :all: annoy` |
| Slow processing | Large file size | Check if ANN index is being used (console should show "ANN index built successfully") |
| No results after upload | Server error | Check console logs for error messages |
| Incorrect predictions | Master dataset not uploaded | Re-upload A.xlsx to admin page or place in knowledge_base/ directory |
| Log files not generated | Log folders missing | Check if "Update Knowledge Base log" and "Upload and Process log" folders exist |
| File watcher not working | watchdog library not installed | Install with `pip install watchdog` |
| Result files not generated | Results directory missing | System will automatically create the directory |

### Debugging Steps

1. **Check Console Logs:**
   - Look for model loading messages
   - Check for ANN index initialization messages
   - Verify semantic matching is enabled
   - Check for processing errors

2. **Verify Model Installation:**
   - Check if `models/all-MiniLM-L6-v2` directory exists
   - Verify model files are present

3. **Test Dependencies:**
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers available')"
   python -c "from annoy import AnnoyIndex; print('annoy available')"
   python -c "import numpy; print('numpy available')"
   ```

4. **Check Log Files:**
   - Examine log files in "Update Knowledge Base log" and "Upload and Process log" folders
   - Look for performance metrics and error messages

## Test Summary

### Test Results Template

| Test Case | Test ID | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|---------|----------------|---------------|-----------|-------|
| Exact Match Test | TC-001 | All exact matches | | | |
| Semantic Matching Test | TC-002 | AISemanticMapping for PnP Destroy with enhanced scores | | | |
| Fuzzy Matching Fallback | TC-003 | FuzzyMapping when model unavailable | | | |
| Error Handling Test | TC-004 | Appropriate error messages | | | |
| Performance Test | TC-005 | Processing < 1 minute with ANN indexing | | | |
| Enhanced Columns Test | TC-006 | All new columns populated correctly | | | |
| Log Generation Test | TC-007 | Log files generated with performance metrics | | | |

### Final Test Conclusion

After completing all test cases, document:

1. Overall system performance
2. Any issues encountered
3. Recommendations for improvement
4. Whether the system meets requirements

## Appendix: Sample Test Files

### Master File (A.xlsx) Structure

```
MATERIAL_NAME,SUB_MATERIAL_NAME,UOM,TRANSACTION_TYPE,IMLUI_Billable Date,IMLUI_Billable Qty,IMLUI_Document ID
MATERIAL_A,Assembly,PC,ORDERS,2024-01-01,10,DOC-001
MATERIAL_NAME,PnP Scrap,EA,ADJUSTMENT,2024-01-01,5,DOC-002
MATERIAL_B,Disassembly,EA,ADJUSTMENT,2024-01-01,3,DOC-003
```

### Input File (B2.xlsx) Structure

```
MATERIAL_NAME,SUB_MATERIAL_NAME,UOM,TRANSACTION_TYPE,IMLUI_Billable Date,IMLUI_Billable Qty,IMLUI_Document ID
MATERIAL_NAME,PnP Destroy,EA,,2024-01-02,2,DOC-004
```

### Output File (MappingResult_*.xlsx) Structure

```
MATERIAL_NAME,SUB_MATERIAL_NAME,UOM,TRANSACTION_TYPE,IMLUI_Billable Date,IMLUI_Billable Qty,IMLUI_Document ID,Match Type,Semantic Score,Fuzzy Score,Final Combined Score,Matched Master SUB_MATERIAL_NAME
MATERIAL_NAME,PnP Destroy,EA,ADJUSTMENT,2024-01-02,2,DOC-004,AISemanticMapping,85.42,60,80.34,PnP Scrap
```

## Contact Information

For testing assistance or questions:

- Project Repository: https://github.com/Victor-Huang-Yan/TACMappingTest-Semantic.git
- Technical Support: [Your Contact Information]

---

**Test Manual Version:** 1.0
**Last Updated:** 2026-04-04