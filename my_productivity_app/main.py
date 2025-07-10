



# !/usr/bin/env python3
"""
CLI Pomodoro Task Manager
A command-line application for task management with Pomodoro timer functionality.
"""

from src.app_interface import PomodoroApp

def main():
    """Entry point of the application"""
    try:
        app = PomodoroApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()