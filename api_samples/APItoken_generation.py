# Install dependency: pip install pyjwt

import jwt
import datetime
from flask import Flask, request, jsonify

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Use environment variable in production
app.config['TOKEN_EXPIRATION'] = 86400  # Token expiration time (seconds)

# Mock user database
users = {
    'testuser1': 'maersktac901',  # Use hashed passwords in production
    'testuser2': 'maersktac902',
    'testuser3': 'maersktac903',
    'testuser4': 'maersktac904'   
}

def generate_token(username):
    """Generate JWT token for authenticated user"""
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=app.config['TOKEN_EXPIRATION']),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def validate_token(token):
    """Validate JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login to get access token"""
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    # Validate user (use hashed password validation in production)
    if username not in users or users[username] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = generate_token(username)
    return jsonify({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': app.config['TOKEN_EXPIRATION']
    })

# Protected API endpoint
@app.route('/api/map', methods=['POST'])
def api_map():
    """Semantic Mapping API Interface"""
    # Validate token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header is required'}), 401
    
    try:
        token = auth_header.split(' ')[1]  # Extract Bearer token
    except IndexError:
        return jsonify({'error': 'Invalid authorization header format'}), 401
    
    if not validate_token(token):
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    # Existing code...
    # Process API request...

# Other protected endpoints also need to add the same token validation logic