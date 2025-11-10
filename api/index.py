import sys
import os

# Set Vercel environment variable
os.environ['VERCEL'] = '1'

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, initialize_app

# Initialize app on import (runs on cold start)
try:
    initialize_app()
except Exception as e:
    print(f"Warning: Could not initialize app: {e}")

# Vercel serverless function handler
# This is the entry point that Vercel will use
handler = app

