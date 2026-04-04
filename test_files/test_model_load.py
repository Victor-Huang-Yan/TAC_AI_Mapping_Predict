import os
import sys

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test model loading in isolation
try:
    print("Testing numpy import...")
    import numpy as np
    print(f"Numpy imported successfully: {np.__version__}")
    
    print("Testing sentence-transformers import...")
    from sentence_transformers import SentenceTransformer
    print("Sentence-transformers imported successfully")
    
    # Test model loading
    MODEL_DIR = 'models/all-MiniLM-L6-v2'
    
    if os.path.exists(MODEL_DIR):
        print("Loading model from local directory...")
        model = SentenceTransformer(MODEL_DIR)
        print("Model loaded successfully from local")
    else:
        print("Model directory not found, downloading from Hugging Face...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model downloaded successfully")
        # Save model to local
        print("Saving model to local directory...")
        model.save(MODEL_DIR)
        print("Model saved successfully")
    
    print("Model load test passed!")
    
    # Test encoding a simple string
    print("Testing model encoding...")
    embedding = model.encode("test")
    print(f"Embedding generated successfully: {embedding.shape}")
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
