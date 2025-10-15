import json
import os
from datetime import datetime
from enum import Enum

TASK_FILE = 'tasks.josn'

class Priority(Enum):
    """
    An enumeration to clearly define task priority levels.
    This encapsulates the priority state for clenaer, safer code.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __str__(self):
        """
        Returns string reperesentation for user display"""
        return self.name

class Task:
    """
    Represents a single task with its attributes and status.
    Demonstrates encapsulation by  bundling all task data and behaviour.
    """
    def __init__(self, title, description, due_date, priority_level):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = "Pending"
        self.priority = Priority[priority_level.upper()]

    def mark_complete(self):
        """Changes the state of the task to 'Complete'."""
        self.status = "Complete"

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON serialization"""
        return {
                "title": self.title,
                "description": self.description,
                "due_date": self.due_date,
                "status": self.status,
                "priority": self.priority.name
                }

    @staticmethod
    def from_dict(data):
        """Creates a Task objet form a dictionary (for JSON deserialization)"""
        # Note: We pass the priortiy string directly to the constructor
        task = Task(data['title'], data['description'], data['due_date'], data['priority'])
        return task

    def __str__(self):
        """Provides a user-friendly string representation of the task."""
        due_str = f"Due: {self.due_date}"
        priority_str = str(self.priority)
        if self.priority == Priority.CRITICAL:
            priority_str = f" {priority_str}"
        elif self.priority == Priority.HIGH:
            priority_str = f" {priortiy_str}"

        return (
                f"{indicator} Title: {self.title}\n"
                f"  > Priority: {priority_str} | Status: {self.status} | {due_str}\n"
                f"  > Description: {self.description}"
                )

class Scheduler:
        """
        Manages the collection of tasks and handles persistence and prioritization.
        Encapsulates all logic related to managing the task list.
        """
        def __init__(self, file_path):
            self.file_path = file_path
            self.tasks = []
            self._load_tasks()

        def _load_tasks(self):
            """Loads tasks from the JSON file"""
            if not os.path.exists(self.file_path):
                print("Task file not found. Starting with an empty scheduler.")
                return
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in data]
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading task file. {e} Starting with an emoty scheduler")
                self.tasks = []

        def save_tasks(self):
            """Saves all tasks to the JSON file"""
            data_to_save = [t.to_dict() for t in self.tasks]
            with open(self.file_path, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print("Tasks saved successfully.")

        def add_task(self, task):
            """Adds a new task object and saves the list."""
            self.tasks.append(task)
            self.save_tasks()
            print("\nTask added.")

        def view_task_by_priority(self):
            """
            Displays pending tasks sorted by priority (Critical > High > Medium > Low) and then by due date
            """
            pending_tasks = [t for t in self.tasks if t.status == "Pending"]
            # Re-sort to match the displayed view_tasks_by_priority order
            sorted_tasks = sorted(
                    pending_tasks,
                    key=lambda t: (t.priority.value, t.due_date),
                    reverse = True
                    )
            try:
                #Get the actual Task object from the sorted list
                task_to_compelete = sorted_tasks[task_index - 1]
                # Now, find that *same* object in the main list and mark it complete
                for t in self.tasks:
                    if t is task_to_complete:
                        t.mark_complete()
                        break
                    self.save_tasks()
                    print(f"\nTask '{task_to_complete.title}' narked as complete!")
            except IndexError:
                    print("Invalid task number.")
            except Exception as e:
                    print(f"An error occured: {e}")

def get_task_details():
        """Helper function to get task details from the user."""
        title = input("Enter task title: ")
        description = input("Enter description: ")
        while True:
            due_date_str = input("Enter due date (YYYY-MM-DD): ")
            try:
                datetime.strptime(due_date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYY-MM-DD.")
        priority_options = [p.name for p in Priority]
        while True:
            priority_level = input(f"Enter priority ({', '.join(priority_options)}): ")
            if priority_level.upper() in priority_options:
                break
            print("Invalid priority. Please choose form the list.")
        return Task(title, description, due_date_str, priority_level)

def main():
        """The main function to run the command-line interface."""
        scheduler = Scheduler(TASK_FILE)
        print("Welcome to your Simple Taks Scheduler!")

        while True:
            print("\n--- Menu ---")
            print("1: Add a new task")
            print("2: View scheduled tasks (by priority)")
            print("3: Mark a task as complete")
            print("4: Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                new_task = get_task_details()
                scheduler.add_task(new_task)
            elif choice == '2':
                scheduler.view_task_by_priority()
            elif choice == '3':
                scheduler.view_task_by_priority()
                if [t for t in scheduler.tasks if t.status == "Pending"]:
                    try:
                        task_num = int(input("Enter the number of the task to mark complete: "))
                        scheduler.complete_task(task_num)
                    except ValueError:
                        print("Please enter a valid number.")
            elif choice == '4':
                print("Saving tasks and exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
