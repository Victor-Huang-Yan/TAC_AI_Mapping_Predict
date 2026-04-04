import requests
import json

# API endpoint URL
url = "http://localhost:5000/api/map"

# Sample request payload
payload = {
  "items": [
    {
      "MATERIAL_NAME": "Picking",
      "SUB_MATERIAL_NAME": "PnP Destroy",
      "UOM": "EA"
    },
    {
      "MATERIAL_NAME": "Picking",
      "SUB_MATERIAL_NAME": "PnP Discard",
      "UOM": "EA"
    }
  ]
}

try:
  # Send POST request
  response = requests.post(url, json=payload)
  
  # Print response status and content
  print(f"Status Code: {response.status_code}")
  print("Response:")
  print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
  print(f"Error: {str(e)}")