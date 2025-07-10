import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum


# Import TASKS_FILE from config.py
import config # You can import config directly


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    created_at: str = ""
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class TaskManager:
    def __init__(self, data_file: str = config.TASKS_FILE):
        self.tasks: List[Task] = []
        self.next_id = 1
        self.data_file = data_file
        self.load_data()
        
    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> Task:
        """Add a new task"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save_data()
        return task
        
    def remove_task(self, task_id: int) -> bool:
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_data()
                return True
        return False
        
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task attributes"""
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    if key == 'priority' and isinstance(value, (int, str)):
                        try:
                            task.priority = Priority(int(value))
                        except ValueError:
                            print(f"Invalid priority value: {value}")
                            continue
                    elif key == 'status' and isinstance(value, str):
                        try:
                            task.status = TaskStatus(value)
                        except ValueError:
                            print(f"Invalid status value: {value}")
                            continue
                    else:
                        setattr(task, key, value)
            self.save_data()
            return True
        return False
        
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
        
    def reorder_tasks(self, task_id: int, new_position: int) -> bool:
        """Reorder tasks by moving task to new position"""
        task = None
        old_index = -1
        
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                task = t
                old_index = i
                break
                
        if task and 0 <= new_position < len(self.tasks):
            self.tasks.pop(old_index)
            self.tasks.insert(new_position, task)
            self.save_data()
            return True
        return False
        
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Filter tasks by status"""
        return [task for task in self.tasks if task.status == status]
        
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Filter tasks by priority"""
        return [task for task in self.tasks if task.priority == priority]
        
    def mark_complete(self, task_id: int) -> bool:
        """Mark task as completed"""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            self.save_data()
            return True
        return False
        
    def save_data(self):
        """Save tasks to JSON file"""
        data = {
            'tasks': [],
            'next_id': self.next_id
        }
        
        for task in self.tasks:
            task_dict = asdict(task)
            task_dict['priority'] = task.priority.value
            task_dict['status'] = task.status.value
            data['tasks'].append(task_dict)
            
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_data(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                self.next_id = data.get('next_id', 1)
                
                for task_data in data.get('tasks', []):
                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data.get('description', ''),
                        priority=Priority(task_data.get('priority', 2)),
                        status=TaskStatus(task_data.get('status', 'todo')),
                        created_at=task_data.get('created_at', ''),
                        completed_at=task_data.get('completed_at')
                    )
                    self.tasks.append(task)
        except Exception as e:
            print(f"Error loading data: {e}")











