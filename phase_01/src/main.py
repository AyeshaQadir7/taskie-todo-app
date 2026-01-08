"""Entry point for the todo application.

This module orchestrates application startup and wires dependencies together.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import Task
from src.storage import TaskStorage
from src.service import TaskService
from src.cli import TodoCLI


def main() -> None:
    """Start the todo application.

    Creates storage, service, and CLI instances, then starts the main event loop.
    """
    storage = TaskStorage()
    service = TaskService(storage)
    cli = TodoCLI(service)
    cli.run()


if __name__ == "__main__":
    main()
