"""
Configuration settings for Personal Productivity Assistant
"""

import os

# Application Info
APP_NAME = "Personal Productivity Assistant"
AUTHOR = "Khadija Abbas"

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


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)