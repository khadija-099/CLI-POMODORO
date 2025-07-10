#!/usr/bin/env python3
"""
Easy launcher for Personal Productivity Assistant
Just run this file to start the application
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def main():
    """Launch the application"""
    print("=" * 50)
    print("🚀 Personal Productivity Assistant Launcher")
    print("=" * 50)
    
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    try:
        # Check if main.py exists
        if not os.path.exists('main.py'):
            print("Error: main.py not found!")
            print("Make sure you're in the correct directory.")
            input("Press Enter to exit...")
            return
        
        print("✓ Starting application...")
        
        # Run the main application
        result = subprocess.run([sys.executable, 'main.py'], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode != 0:
            print("Application exited with an error.")
        else:
            print("Application closed successfully.")
            
    except Exception as e:
        print(f"Error launching application: {e}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()