"""In-memory task storage layer.

This module manages the in-memory collection of tasks with no business logic.
Storage is responsible for CRUD operations and ID generation only.
"""

from src.models import Task


class TaskStorage:
    """In-memory storage for tasks.

    Manages a list of Task objects and auto-generates sequential IDs.
    No validation or business logic; all validation delegated to service layer.
    """

    def __init__(self) -> None:
        """Initialize empty task storage and ID counter."""
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """Add a new task with auto-generated sequential ID.

        Args:
            task: Task object with id=0 (placeholder, will be assigned).

        Returns:
            The task with assigned ID added to storage.
        """
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks in storage order.

        Returns:
            List of all Task objects currently stored.
        """
        return self.tasks

    def get_task(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: ID of the task to retrieve.

        Returns:
            Task object if found, None otherwise.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str) -> bool:
        """Update a task's title.

        Args:
            task_id: ID of the task to update.
            title: New title for the task.

        Returns:
            True if task found and updated, False if task not found.
        """
        task = self.get_task(task_id)
        if task:
            task.title = title
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of the task to delete.

        Returns:
            True if task found and deleted, False if task not found.
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete.

        Returns:
            True if task found and marked, False if task not found.
        """
        task = self.get_task(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete.

        Returns:
            True if task found and marked, False if task not found.
        """
        task = self.get_task(task_id)
        if task:
            task.completed = False
            return True
        return False

    def list_ids(self) -> list[int]:
        """Get all task IDs for error messages.

        Returns:
            List of all task IDs currently in storage.
        """
        return [task.id for task in self.tasks]
