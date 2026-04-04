import os
import sys

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Test importing the app module
try:
    import app
    print("App imported successfully")
    print(f"App object exists: {hasattr(app, 'app')}")
    
    # Test model loading
    print(f"use_semantic_matching: {app.use_semantic_matching}")
    
    # Test creating uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("Created uploads directory")
    else:
        print("Uploads directory exists")
        
    print("All tests passed - app should start successfully")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()