import sys
from .task_manager import TaskManager, Priority, TaskStatus
from .focus_timer import PomodoroTimer, PomodoroSettings
from datetime import datetime





class PomodoroApp:
    def __init__(self):
        self.task_manager = TaskManager()
        self.timer_settings = PomodoroSettings()
        self.timer = PomodoroTimer(self.timer_settings)
        
    def display_banner(self):
        """Display app banner"""
        print("\n" + "="*50)
        print("🍅 CLI POMODORO TASK MANAGER 🍅")
        print("="*50)
        
    def display_main_menu(self):
        """Display main menu options"""
        print("\n📋 MAIN MENU:")
        print("1. 📝 Task Management")
        print("2. 🍅 Start Pomodoro Session")
        print("3. ⚙️  Settings")
        print("4. 📊 Statistics")
        print("5. 🚪 Exit")
        
    def display_task_menu(self):
        """Display task management menu"""
        print("\n📝 TASK MANAGEMENT:")
        print("1. ➕ Add Task")
        print("2. 📋 View Tasks")
        print("3. ✏️  Update Task")
        print("4. ❌ Remove Task")
        print("5. 🔄 Reorder Tasks")
        print("6. ✅ Mark Complete")
        print("7. 🔙 Back to Main Menu")
        
    def display_tasks(self, tasks: list = None):
        """Display tasks in a formatted table"""
        if tasks is None:
            tasks = self.task_manager.tasks
            
        if not tasks:
            print("\n📭 No tasks found!")
            return
            
        print(f"\n📋 TASKS ({len(tasks)} total):")
        print("-" * 80)
        print(f"{'ID':<4} {'Title':<25} {'Priority':<10} {'Status':<12} {'Created':<15}")
        print("-" * 80)
        
        priority_symbols = {Priority.LOW: "🟢", Priority.MEDIUM: "🟡", Priority.HIGH: "🔴"}
        status_symbols = {
            TaskStatus.TODO: "⏳",
            TaskStatus.IN_PROGRESS: "🔄", 
            TaskStatus.COMPLETED: "✅"
        }
        
        for task in tasks:
            priority_display = f"{priority_symbols[task.priority]} {task.priority.name}"
            status_display = f"{status_symbols[task.status]} {task.status.value}"
            created_date = datetime.fromisoformat(task.created_at).strftime("%Y-%m-%d")
            
            print(f"{task.id:<4} {task.title[:25]:<25} {priority_display:<10} {status_display:<12} {created_date:<15}")
            
            if task.description:
                print(f"      📄 {task.description}")
                
    def add_task_interactive(self):
        """Interactive task addition"""
        print("\n➕ ADD NEW TASK:")
        title = input("Task title: ").strip()
        
        if not title:
            print("❌ Task title cannot be empty!")
            return
            
        description = input("Description (optional): ").strip()
        
        print("\nPriority:")
        print("1. 🟢 Low")
        print("2. 🟡 Medium") 
        print("3. 🔴 High")
        
        priority_choice = input("Choose priority (1-3, default 2): ").strip()
        priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)
        
        task = self.task_manager.add_task(title, description, priority)
        print(f"✅ Task '{task.title}' added successfully! (ID: {task.id})")
        
    def update_task_interactive(self):
        """Interactive task update"""
        self.display_tasks()
        
        try:
            task_id = int(input("\nEnter task ID to update: "))
            task = self.task_manager.get_task(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
                
            print(f"\nUpdating task: {task.title}")
            print("(Leave empty to keep current value)")
            
            new_title = input(f"New title [{task.title}]: ").strip()
            new_description = input(f"New description [{task.description}]: ").strip()
            
            # Allow updating priority and status as well
            print("\nUpdate Priority:")
            print("1. 🟢 Low")
            print("2. 🟡 Medium")
            print("3. 🔴 High")
            print(f"Current: {task.priority.name}")
            new_priority_choice = input("New priority (1-3, leave empty to keep current): ").strip()
            
            print("\nUpdate Status:")
            print(f"1. {TaskStatus.TODO.value.title()}")
            print(f"2. {TaskStatus.IN_PROGRESS.value.title()}")
            print(f"3. {TaskStatus.COMPLETED.value.title()}")
            print(f"Current: {task.status.value.title()}")
            new_status_choice = input("New status (1-3, leave empty to keep current): ").strip()

            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_description:
                updates['description'] = new_description
            if new_priority_choice:
                priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
                new_priority = priority_map.get(new_priority_choice)
                if new_priority:
                    updates['priority'] = new_priority
                else:
                    print("Invalid priority choice, keeping current.")
            if new_status_choice:
                status_map = {"1": TaskStatus.TODO, "2": TaskStatus.IN_PROGRESS, "3": TaskStatus.COMPLETED}
                new_status = status_map.get(new_status_choice)
                if new_status:
                    updates['status'] = new_status
                else:
                    print("Invalid status choice, keeping current.")
                    
            if updates:
                self.task_manager.update_task(task_id, **updates)
                print("✅ Task updated successfully!")
            else:
                print("ℹ️ No changes made.")
                
        except ValueError:
            print("❌ Invalid task ID or input!")
            
    def remove_task_interactive(self):
        """Interactive task removal"""
        self.display_tasks()
        
        try:
            task_id = int(input("\nEnter task ID to remove: "))
            task = self.task_manager.get_task(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
                
            confirm = input(f"Are you sure you want to remove '{task.title}'? (y/N): ")
            if confirm.lower() == 'y':
                self.task_manager.remove_task(task_id)
                print("✅ Task removed successfully!")
            else:
                print("ℹ️ Task removal cancelled.")
                
        except ValueError:
            print("❌ Invalid task ID!")
            
    def reorder_tasks_interactive(self):
        """Interactive task reordering"""
        self.display_tasks()
        if not self.task_manager.tasks:
            return

        try:
            task_id = int(input("\nEnter task ID to reorder: "))
            task_to_move = self.task_manager.get_task(task_id)

            if not task_to_move:
                print("❌ Task not found!")
                return

            print(f"Moving task: '{task_to_move.title}'")
            new_position_input = input(f"Enter new position (1 to {len(self.task_manager.tasks)}): ")
            
            if not new_position_input.strip().isdigit():
                print("❌ Invalid position. Please enter a number.")
                return
            
            new_position = int(new_position_input) - 1 # Adjust to 0-indexed list

            if self.task_manager.reorder_tasks(task_id, new_position):
                print("✅ Task reordered successfully!")
                self.display_tasks() # Show updated order
            else:
                print("❌ Invalid new position or task ID.")
        except ValueError:
            print("❌ Invalid input!")

            
    def start_pomodoro_interactive(self):
        """Interactive Pomodoro session start"""
        todo_tasks = self.task_manager.get_tasks_by_status(TaskStatus.TODO)
        
        if not todo_tasks:
            print("\n📭 No pending tasks! Add some tasks first.")
            return
            
        print("\n🍅 START POMODORO SESSION:")
        print("Select a task to work on:")
        print("0. Work without specific task")
        
        for i, task in enumerate(todo_tasks, 1):
            priority_symbol = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
            print(f"{i}. {priority_symbol[task.priority.name]} {task.title}")
            
        try:
            choice_input = input(f"\nChoose task (0-{len(todo_tasks)}): ")
            
            if not choice_input.strip().isdigit():
                print("❌ Invalid choice! Please enter a number.")
                return

            choice = int(choice_input)
            
            task_id = None
            if 1 <= choice <= len(todo_tasks):
                task_id = todo_tasks[choice - 1].id
                # Mark task as in progress
                self.task_manager.update_task(task_id, status=TaskStatus.IN_PROGRESS)
                print(f"🔄 Working on: {todo_tasks[choice - 1].title}")
            elif choice == 0:
                print("🔄 Starting focus session without specific task")
            else:
                print("❌ Invalid choice!")
                return
                
            def on_session_complete(completed_task_id):
                if completed_task_id:
                    self.task_manager.update_task(completed_task_id, status=TaskStatus.COMPLETED)
                    print(f"Task ID {completed_task_id} marked as COMPLETED.")

            self.timer.start_focus_session(task_id, on_complete_callback=on_session_complete)
            
        except ValueError:
            print("❌ Invalid input!")
            
    def display_statistics(self):
        """Display task and session statistics"""
        tasks = self.task_manager.tasks
        completed_tasks = self.task_manager.get_tasks_by_status(TaskStatus.COMPLETED)
        todo_tasks = self.task_manager.get_tasks_by_status(TaskStatus.TODO)
        in_progress_tasks = self.task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        
        print("\n📊 STATISTICS:")
        print("-" * 40)
        print(f"📋 Total Tasks: {len(tasks)}")
        print(f"✅ Completed: {len(completed_tasks)}")
        print(f"⏳ To Do: {len(todo_tasks)}")
        print(f"🔄 In Progress: {len(in_progress_tasks)}")
        print(f"🍅 Focus Sessions Today: {self.timer.session_count}")
        
        if tasks:
            completion_rate = len(completed_tasks) / len(tasks) * 100
            print(f"📈 Completion Rate: {completion_rate:.1f}%")
            
    def display_settings(self):
        """Display and modify settings"""
        print("\n⚙️ SETTINGS:")
        print(f"🍅 Focus Duration: {self.timer_settings.focus_duration // 60} minutes")
        print(f"☕ Short Break: {self.timer_settings.short_break_duration // 60} minutes")
        print(f"🛋️ Long Break: {self.timer_settings.long_break_duration // 60} minutes")
        print(f"🔄 Sessions before long break: {self.timer_settings.sessions_before_long_break}")
        
        print("\nModify settings:")
        print("1. Focus duration")
        print("2. Short break duration") 
        print("3. Long break duration")
        print("4. Sessions before long break")
        print("5. Back to main menu")
        
        try:
            choice = int(input("Choice (1-5): "))
            
            if choice == 1:
                new_duration = int(input("New focus duration (minutes): "))
                if new_duration > 0:
                    self.timer_settings.focus_duration = new_duration * 60
                    print("✅ Focus duration updated!")
                else:
                    print("❌ Duration must be positive.")
                    
            elif choice == 2:
                new_duration = int(input("New short break duration (minutes): "))
                if new_duration > 0:
                    self.timer_settings.short_break_duration = new_duration * 60
                    print("✅ Short break duration updated!")
                else:
                    print("❌ Duration must be positive.")
                    
            elif choice == 3:
                new_duration = int(input("New long break duration (minutes): "))
                if new_duration > 0:
                    self.timer_settings.long_break_duration = new_duration * 60
                    print("✅ Long break duration updated!")
                else:
                    print("❌ Duration must be positive.")
                    
            elif choice == 4:
                new_count = int(input("Sessions before long break: "))
                if new_count > 0:
                    self.timer_settings.sessions_before_long_break = new_count
                    print("✅ Settings updated!")
                else:
                    print("❌ Count must be positive.")
                    
            elif choice == 5:
                pass # Back to main menu
            else:
                print("❌ Invalid choice!")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
            
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        while True:
            self.display_main_menu()
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    # Task Management
                    while True:
                        self.display_task_menu()
                        task_choice = input("\nEnter your choice (1-7): ").strip()
                        
                        if task_choice == '1':
                            self.add_task_interactive()
                        elif task_choice == '2':
                            self.display_tasks()
                        elif task_choice == '3':
                            self.update_task_interactive()
                        elif task_choice == '4':
                            self.remove_task_interactive()
                        elif task_choice == '5':
                            self.reorder_tasks_interactive()
                        elif task_choice == '6':
                            self.display_tasks(self.task_manager.get_tasks_by_status(TaskStatus.TODO) +
                                               self.task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS))
                            if not (self.task_manager.get_tasks_by_status(TaskStatus.TODO) or
                                    self.task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)):
                                print("No tasks to mark complete.")
                                continue
                            try:
                                task_id = int(input("Enter task ID to mark complete: "))
                                if self.task_manager.mark_complete(task_id):
                                    print("✅ Task marked as complete!")
                                else:
                                    print("❌ Task not found or already completed!")
                            except ValueError:
                                print("❌ Invalid task ID!")
                        elif task_choice == '7':
                            break
                        else:
                            print("❌ Invalid choice!")
                            
                elif choice == '2':
                    self.start_pomodoro_interactive()
                    
                elif choice == '3':
                    self.display_settings()
                    
                elif choice == '4':
                    self.display_statistics()
                    
                elif choice == '5':
                    print("\n👋 Thank you for using Pomodoro Task Manager!")
                    print("Stay productive! 🍅")
                    break
                    
                else:
                    print("❌ Invalid choice! Please enter 1-5.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")