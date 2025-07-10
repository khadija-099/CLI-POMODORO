import time
from datetime import datetime, timedelta
from typing import Optional
import sys

class PomodoroSettings:
    def __init__(self):
        self.focus_duration = 25 * 60  # 25 minutes in seconds
        self.short_break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 15 * 60  # 15 minutes
        self.sessions_before_long_break = 4

class PomodoroTimer:
    def __init__(self, settings: PomodoroSettings):
        self.settings = settings
        self.session_count = 0
        self.is_running = False
        self.current_session = None
        self.paused = False
        self.remaining_time = 0
        
    def start_focus_session(self, task_id: Optional[int] = None, on_complete_callback=None):
        """Start a focus session"""
        self.current_session = {
            'type': 'focus',
            'duration': self.settings.focus_duration,
            'task_id': task_id
        }
        self._start_timer(on_complete_callback)
        
    def start_break_session(self, on_complete_callback=None):
        """Start appropriate break session based on session count"""
        if self.session_count % self.settings.sessions_before_long_break == 0:
            session_type = 'long_break'
            duration = self.settings.long_break_duration
        else:
            session_type = 'short_break'
            duration = self.settings.short_break_duration
            
        self.current_session = {
            'type': session_type,
            'duration': duration,
            'task_id': None
        }
        self._start_timer(on_complete_callback)
        
    def _start_timer(self, on_complete_callback=None):
        """Internal timer logic"""
        self.is_running = True
        self.remaining_time = self.current_session['duration']
        
        print(f"\n🍅 {self.current_session['type'].replace('_', ' ').title()} Session Started!")
        print(f"Duration: {self.remaining_time // 60} minutes")
        print("Press 'Ctrl+C' to pause/quit.")
        
        try:
            while self.remaining_time > 0 and self.is_running:
                if not self.paused:
                    mins, secs = divmod(self.remaining_time, 60)
                    print(f"\r⏰ {mins:02d}:{secs:02d} remaining", end="", flush=True)
                    
                    time.sleep(1)
                    self.remaining_time -= 1
                else:
                    time.sleep(0.1) # Check pause status more frequently
                    
            if self.remaining_time <= 0 and self.is_running: # Ensure not stopped by user
                self._session_complete(on_complete_callback)
        except KeyboardInterrupt:
            self._handle_interrupt()
            
    def _session_complete(self, on_complete_callback=None):
        """Handle session completion"""
        print(f"\n\n✅ {self.current_session['type'].replace('_', ' ').title()} Complete!")
        
        if self.current_session['type'] == 'focus':
            self.session_count += 1
            print(f"🎉 Focus sessions completed: {self.session_count}")
            
            if on_complete_callback and self.current_session['task_id']:
                on_complete_callback(self.current_session['task_id'])
            
            # Prompt for break
            print("\nTime for a break!")
            input("Press Enter when ready to start break...")
            self.start_break_session(on_complete_callback) # Pass callback for the next session
        else:
            print("\nBreak time over! Ready to focus again?")
            input("Press Enter to continue...")
            
        self.is_running = False
        
    def _handle_interrupt(self):
        """Handle Ctrl+C gracefully"""
        self.paused = True
        print("\n\n⏸️  Timer paused. What would you like to do?")
        print("1. Resume")
        print("2. Stop session")
        choice = input("Choice (1-2): ").strip()
        
        if choice == '1':
            self.paused = False
            print("Resuming...")
            self._start_timer() # Resume with remaining time
        else:
            self.is_running = False
            self.paused = False
            print("Session stopped.")
            # Reset current session if stopped
            self.current_session = None