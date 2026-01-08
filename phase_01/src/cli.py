"""CLI interface for the todo application.

This module handles all menu rendering, user input, and output formatting.
No business logic; all validation delegated to service layer.
"""

from src.models import Task
from src.service import TaskService


class TodoCLI:
    """Command-line interface for todo application.

    Manages menu display, user input handling, and output formatting.
    All business logic delegated to service layer.
    """

    def __init__(self, service: TaskService) -> None:
        """Initialize CLI with service dependency.

        Args:
            service: TaskService instance for business logic.
        """
        self.service = service

    def display_menu(self) -> None:
        """Display the main menu with 6 options."""
        print("\n" + "=" * 40)
        print("          TODO APPLICATION")
        print("=" * 40)
        print("\nMain Menu:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Tasks")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print()

    def run(self) -> None:
        """Main event loop: display menu, get choice, handle action until exit."""
        while True:
            self.display_menu()
            choice = self.get_menu_choice()
            if choice is None:
                continue

            should_continue = self.handle_choice(choice)
            if not should_continue:
                break

    def get_menu_choice(self) -> int | None:
        """Get and validate menu choice from user.

        Returns:
            Integer choice 1-6, or None if invalid input (with error displayed).
        """
        while True:
            try:
                user_input = input("Select an option (1-6): ").strip()
                choice = int(user_input)
                if 1 <= choice <= 6:
                    return choice
                else:
                    print(f"Option {choice} does not exist. Please select 1-6.")
            except ValueError:
                print("Invalid input. Please enter a number corresponding to a menu option.")

    def handle_choice(self, choice: int) -> bool:
        """Route menu choice to appropriate action.

        Args:
            choice: Menu option selected (1-6).

        Returns:
            False if exit selected, True to continue menu loop.
        """
        try:
            if choice == 1:
                self._handle_add_task()
            elif choice == 2:
                self._handle_delete_task()
            elif choice == 3:
                self._handle_update_task()
            elif choice == 4:
                self._handle_view_tasks()
            elif choice == 5:
                self._handle_mark_task()
            elif choice == 6:
                print("\nGoodbye!")
                return False
            return True
        except Exception as e:
            print("An unexpected error occurred. Returning to menu.")
            return True

    def _handle_add_task(self) -> None:
        """Handle add task menu option."""
        title = self.prompt_for_title("Enter task title: ")
        if title:
            success, task, message = self.service.add_task(title)
            self.display_message(message)

    def _handle_view_tasks(self) -> None:
        """Handle view tasks menu option."""
        tasks = self.service.list_tasks()
        self.display_tasks(tasks)

    def _handle_mark_task(self) -> None:
        """Handle mark complete/incomplete menu option."""
        task_id = self.prompt_for_id()
        if task_id is None:
            return

        try:
            toggle_choice = input("Mark as (1) Complete or (2) Incomplete? ").strip()
        except EOFError:
            # Default to marking complete in non-interactive mode
            toggle_choice = "1"

        if toggle_choice == "1":
            success, task, message = self.service.mark_complete(task_id)
            self.display_message(message)
        elif toggle_choice == "2":
            success, task, message = self.service.mark_incomplete(task_id)
            self.display_message(message)
        else:
            print("Invalid choice. Please enter 1 or 2.")

    def _handle_update_task(self) -> None:
        """Handle update task menu option."""
        task_id = self.prompt_for_id()
        if task_id is None:
            return

        new_title = self.prompt_for_title("Enter new title: ")
        if new_title:
            success, task, message = self.service.update_task(task_id, new_title)
            self.display_message(message)

    def _handle_delete_task(self) -> None:
        """Handle delete task menu option."""
        task_id = self.prompt_for_id()
        if task_id is None:
            return

        success, message = self.service.delete_task(task_id)
        self.display_message(message)

    def display_tasks(self, tasks: list[Task]) -> None:
        """Display all tasks with status indicators.

        Args:
            tasks: List of Task objects to display.
        """
        if not tasks:
            print("\nNo tasks yet. Add one to get started!")
            return

        print("\n" + "-" * 40)
        for task in tasks:
            status = "[X]" if task.completed else "[ ]"
            print(f"{status} Task #{task.id}: {task.title}")
        print("-" * 40)

    def prompt_for_title(self, prompt: str) -> str:
        """Prompt user for task title.

        Args:
            prompt: Prompt message to display.

        Returns:
            User input as string.
        """
        try:
            return input(prompt).strip()
        except EOFError:
            # Handle EOF gracefully in non-interactive mode
            return ""

    def prompt_for_id(self) -> int | None:
        """Prompt user for task ID.

        Returns:
            Integer ID, or None if invalid input.
        """
        while True:
            try:
                user_input = input("Enter task ID: ").strip()
                if not user_input:
                    return None
                return int(user_input)
            except (ValueError, EOFError):
                print("Invalid task ID. Please enter a number.")

    def display_message(self, message: str) -> None:
        """Display message to user.

        Args:
            message: Message to display.
        """
        print(message)
