"""
Configuration settings for Personal Productivity Assistant
"""

import os

# Application Info
APP_NAME = "Personal Productivity Assistant"
APP_VERSION = "1.0.0"
AUTHOR = "[Your Name]"

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

# Default Timer Settings (in minutes)
DEFAULT_FOCUS_TIME = 25
DEFAULT_SHORT_BREAK = 5
DEFAULT_LONG_BREAK = 15
DEFAULT_SESSIONS_FOR_LONG_BREAK = 4

# Task Priority Levels
PRIORITY_LOW = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3

# Colors for CLI (optional)
COLOR_SUCCESS = '\033[92m'  # Green
COLOR_ERROR = '\033[91m'    # Red
COLOR_WARNING = '\033[93m'  # Yellow
COLOR_INFO = '\033[94m'     # Blue
COLOR_RESET = '\033[0m'     # Reset

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)