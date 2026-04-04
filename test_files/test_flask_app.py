from flask import Flask, render_template
import os

# Create a minimal Flask app to test the structure
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'test_secret_key'

@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/admin')
def admin():
    return "Admin page is accessible!"

if __name__ == '__main__':
    # Ensure uploads directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    print("Starting minimal Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
