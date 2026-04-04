# Python 客户端示例
import requests
import json

# 登录获取令牌
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "username": "admin",
    "password": "password123"
}

response = requests.post(login_url, json=login_data)
token_response = response.json()

if "access_token" in token_response:
    access_token = token_response["access_token"]
    print(f"获取到令牌: {access_token}")
else:
    print("登录失败:", token_response.get("error"))