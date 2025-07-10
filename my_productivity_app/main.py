# my_productivity_app/main.py
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.app_interface import PomodoroApp
from src.utils import display_banner

def main():
    display_banner()
    app = PomodoroApp()
    app.run()

if __name__ == "__main__":
    main()











# # !/usr/bin/env python3
# """
# CLI Pomodoro Task Manager
# A command-line application for task management with Pomodoro timer functionality.
# """

# from src.app_interface import PomodoroApp

# def main():
#     """Entry point of the application"""
#     try:
#         app = PomodoroApp()
#         app.run()
#     except KeyboardInterrupt:
#         print("\n\n👋 Application terminated by user.")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")

# if __name__ == "__main__":
#     main()