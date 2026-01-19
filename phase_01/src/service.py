"""Business logic layer for task operations.

This module orchestrates task CRUD operations, validation, and error handling.
All business rules and validation logic reside here.
"""

from src.models import Task
from src.storage import TaskStorage


class TaskService:
    """Service layer for task management.

    Handles validation, business logic, and orchestration of storage operations.
    Returns structured results (success, result, message) for CLI to display.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize service with storage dependency.

        Args:
            storage: TaskStorage instance for data persistence.
        """
        self.storage = storage

    def add_task(self, title: str) -> tuple[bool, Task | None, str]:
        """Add a new task with validation.

        Args:
            title: Task title (will be stripped of whitespace).

        Returns:
            Tuple of (success: bool, task: Task | None, message: str)
        """
        # Validate title
        clean_title = title.strip()
        if not clean_title:
            return (False, None, "Task title cannot be empty. Please try again.")

        # Create and add task
        task = Task(id=0, title=clean_title, completed=False)
        added_task = self.storage.add_task(task)
        message = f"✓ Task added: Task #{added_task.id}: {added_task.title}"
        return (True, added_task, message)

    def list_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects in storage.
        """
        return self.storage.get_all_tasks()

    def update_task(self, task_id: int, title: str) -> tuple[bool, Task | None, str]:
        """Update a task's title with validation.

        Args:
            task_id: ID of task to update.
            title: New title (will be stripped of whitespace).

        Returns:
            Tuple of (success: bool, task: Task | None, message: str)
        """
        # Validate task exists
        if task_id not in self.storage.list_ids():
            available = self.storage.list_ids()
            return (False, None, f"Task ID {task_id} not found. Available IDs: {available}")

        # Validate title
        clean_title = title.strip()
        if not clean_title:
            return (False, None, "Task title cannot be empty. Please try again.")

        # Update task
        self.storage.update_task(task_id, clean_title)
        updated_task = self.storage.get_task(task_id)
        message = f"✓ Task #{task_id} updated: {updated_task.title}"
        return (True, updated_task, message)

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task with validation.

        Args:
            task_id: ID of task to delete.

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate task exists
        if task_id not in self.storage.list_ids():
            available = self.storage.list_ids()
            return (False, f"Task ID {task_id} not found. Available IDs: {available}")

        # Delete task
        self.storage.delete_task(task_id)
        remaining_count = len(self.storage.list_ids())
        message = f"✓ Task #{task_id} deleted. {remaining_count} task(s) remaining."
        return (True, message)

    def mark_complete(self, task_id: int) -> tuple[bool, Task | None, str]:
        """Mark a task as complete with validation.

        Args:
            task_id: ID of task to mark complete.

        Returns:
            Tuple of (success: bool, task: Task | None, message: str)
        """
        # Validate task exists
        if task_id not in self.storage.list_ids():
            available = self.storage.list_ids()
            return (False, None, f"Task ID {task_id} not found. Available IDs: {available}")

        # Mark complete
        self.storage.mark_complete(task_id)
        task = self.storage.get_task(task_id)
        message = f"✓ Task #{task_id} marked as complete."
        return (True, task, message)

    def mark_incomplete(self, task_id: int) -> tuple[bool, Task | None, str]:
        """Mark a task as incomplete with validation.

        Args:
            task_id: ID of task to mark incomplete.

        Returns:
            Tuple of (success: bool, task: Task | None, message: str)
        """
        # Validate task exists
        if task_id not in self.storage.list_ids():
            available = self.storage.list_ids()
            return (False, None, f"Task ID {task_id} not found. Available IDs: {available}")

        # Mark incomplete
        self.storage.mark_incomplete(task_id)
        task = self.storage.get_task(task_id)
        message = f"✓ Task #{task_id} marked as incomplete."
        return (True, task, message)
