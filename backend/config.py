"""
F1 Telemetry Viewer - Configuration Settings
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# FastF1 Cache directory
CACHE_DIR = os.path.join(BASE_DIR, '.fastf1-cache')

# Computed data directory
COMPUTED_DATA_DIR = os.path.join(BASE_DIR, 'computed_data')

# Frames per second for replay
FPS = 25

# Time delta between frames
DT = 1 / FPS

# CORS settings
CORS_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]

# Flask settings
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
PORT = int(os.environ.get('FLASK_PORT', 5000))
