import requests
import json

# Test API without authentication
print("Testing API without authentication...")

# Test health endpoint
try:
    response = requests.get('http://localhost:5000/api/health')
    print(f"Health endpoint status: {response.status_code}")
    print(f"Health response: {response.json()}")
except Exception as e:
    print(f"Error accessing health endpoint: {e}")

# Test docs endpoint
try:
    response = requests.get('http://localhost:5000/api/docs')
    print(f"Docs endpoint status: {response.status_code}")
    print("Docs response received successfully")
except Exception as e:
    print(f"Error accessing docs endpoint: {e}")

# Test map endpoint
try:
    test_data = {
        "items": [
            {
                "MATERIAL_NAME": "Test Material",
                "SUB_MATERIAL_NAME": "Test Sub Material",
                "UOM": "EA"
            }
        ]
    }
    response = requests.post('http://localhost:5000/api/map', json=test_data)
    print(f"Map endpoint status: {response.status_code}")
    print(f"Map response: {response.json()}")
except Exception as e:
    print(f"Error accessing map endpoint: {e}")