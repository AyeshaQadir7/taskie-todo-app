"""Task model for the todo application.

This module defines the Task dataclass that represents a single todo item.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier for the task (auto-generated, sequential).
        title: Description of the task (required, non-empty).
        completed: Whether the task is marked as complete (default: False).
    """
    id: int
    title: str
    completed: bool = False
