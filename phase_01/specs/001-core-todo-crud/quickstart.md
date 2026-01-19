# Quickstart: Phase I Todo Application

**Status**: Planning Phase | **Branch**: `001-core-todo-crud`

This guide is for developers who want to understand and work with the Phase I todo application architecture.

## Project Layout

```text
.
├── src/
│   ├── main.py                 # Application entry point
│   ├── models.py               # Task dataclass
│   ├── storage.py              # In-memory task storage
│   ├── service.py              # Business logic (CRUD, validation)
│   └── cli.py                  # Menu interface & user interaction
├── tests/
│   ├── test_models.py          # Task model tests
│   ├── test_storage.py         # Storage layer tests
│   ├── test_service.py         # Service layer tests
│   └── test_cli.py             # CLI interaction tests
├── specs/
│   └── 001-core-todo-crud/
│       ├── spec.md             # Feature specification
│       ├── plan.md             # Implementation plan (this architecture)
│       ├── data-model.md       # Entity definitions
│       └── quickstart.md       # This file
└── README.md
```

## Running the Application

### Prerequisites

- Python 3.13+
- No external dependencies (standard library only)

### Execution

```bash
# From the repository root
python src/main.py
```

**Expected Output**:
```
========================================
          TODO APPLICATION
========================================

Main Menu:
1. Add Task
2. Delete Task
3. Update Task
4. View Tasks
5. Mark Complete/Incomplete
6. Exit

Select an option (1-6): _
```

## Typical User Flow

### 1. View Empty Task List

```
Select an option (1-6): 4

No tasks yet. Add one to get started!

Main Menu:
...
```

### 2. Add a Task

```
Select an option (1-6): 1
Enter task title: Buy groceries

✓ Task added: Task #1: Buy groceries

Main Menu:
...
```

### 3. Add Another Task

```
Select an option (1-6): 1
Enter task title: Review pull requests

✓ Task added: Task #2: Review pull requests

Main Menu:
...
```

### 4. View All Tasks

```
Select an option (1-6): 4

[ ] Task #1: Buy groceries
[ ] Task #2: Review pull requests

Main Menu:
...
```

### 5. Mark Task Complete

```
Select an option (1-6): 5
Enter task ID: 1

✓ Task #1 marked as complete.

Main Menu:
...
```

### 6. View Updated List

```
Select an option (1-6): 4

[X] Task #1: Buy groceries
[ ] Task #2: Review pull requests

Main Menu:
...
```

### 7. Update Task

```
Select an option (1-6): 3
Enter task ID to update: 2
Enter new title: Code review and QA approval

✓ Task #2 updated: Code review and QA approval

Main Menu:
...
```

### 8. Delete Task

```
Select an option (1-6): 2
Enter task ID to delete: 1

✓ Task #1 deleted. 1 task remaining.

Main Menu:
...
```

### 9. Exit Application

```
Select an option (1-6): 6

Goodbye!

[Application terminates]
```

## Architecture Overview

### Layer 1: Data Model (`models.py`)

Defines the Task entity as a dataclass.

```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
```

**Responsibilities**:
- Represent a single task
- Store id, title, completed status
- No business logic

### Layer 2: Storage (`storage.py`)

Manages the in-memory task collection.

```python
class TaskStorage:
    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """Add task with auto-assigned ID"""

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks"""

    def get_task(self, id: int) -> Task | None:
        """Get task by ID"""

    def update_task(self, id: int, title: str) -> bool:
        """Update task title"""

    def delete_task(self, id: int) -> bool:
        """Delete task by ID"""

    def mark_complete(self, id: int) -> bool:
        """Mark task as complete"""

    def mark_incomplete(self, id: int) -> bool:
        """Mark task as incomplete"""

    def list_ids(self) -> list[int]:
        """Return all task IDs for error messages"""
```

**Responsibilities**:
- Store tasks in-memory
- Auto-generate sequential IDs
- Provide CRUD operations without validation
- Return None/False to signal "not found"

**Key Principle**: Storage has NO business logic. It's a dumb data container.

### Layer 3: Service (`service.py`)

Orchestrates business logic and validation.

```python
class TaskService:
    def __init__(self, storage: TaskStorage):
        self.storage = storage

    def add_task(self, title: str) -> tuple[bool, Task | None, str]:
        """Validate title, create task, return (success, task, message)"""

    def list_tasks(self) -> list[Task]:
        """Return all tasks"""

    def update_task(self, id: int, title: str) -> tuple[bool, Task | None, str]:
        """Validate task exists and title, update, return result"""

    def delete_task(self, id: int) -> tuple[bool, str]:
        """Validate task exists, delete, return result"""

    def mark_complete(self, id: int) -> tuple[bool, Task | None, str]:
        """Validate task exists, mark complete, return result"""

    def mark_incomplete(self, id: int) -> tuple[bool, Task | None, str]:
        """Validate task exists, mark incomplete, return result"""
```

**Responsibilities**:
- Validate all input (title non-empty, task IDs exist)
- Call storage methods
- Return user-friendly error messages
- All business rules live here

**Key Principle**: Service is testable independent of CLI. It returns structured results (success, result, message) that CLI can display.

### Layer 4: CLI (`cli.py`)

Handles menu rendering and user interaction.

```python
class TodoCLI:
    def __init__(self, service: TaskService):
        self.service = service

    def run(self) -> None:
        """Main loop: display menu, get choice, handle action until exit"""

    def display_menu(self) -> None:
        """Print main menu"""

    def handle_choice(self, choice: int) -> bool:
        """Route to action; return False to exit, True to continue"""

    def display_tasks(self, tasks: list[Task]) -> None:
        """Print task list with status indicators"""
```

**Responsibilities**:
- Display menu and prompts
- Get and validate user input (numeric, 1-6)
- Call service methods
- Display results and error messages
- Loop until exit

**Key Principle**: CLI has NO business logic. It delegates validation to service and displays results.

### Layer 5: Main (`main.py`)

Orchestrates application startup.

```python
def main() -> None:
    storage = TaskStorage()
    service = TaskService(storage)
    cli = TodoCLI(service)
    cli.run()

if __name__ == "__main__":
    main()
```

## Control Flow: Add Task Example

```
User types: 1 (Add Task)
↓
CLI.handle_choice(1)
↓
CLI.prompt_for_title() → "Buy groceries"
↓
Service.add_task("Buy groceries")
  ├─ Validate title non-empty ✓
  ├─ Storage.add_task(Task(id=1, title="Buy groceries", completed=False))
  │   └─ Assign ID, append to list
  └─ Return (True, task, "Task added: Task #1: Buy groceries")
↓
CLI.display_message("✓ Task added: Task #1: Buy groceries")
↓
Back to menu
```

## Error Handling Example

```
User types: 1 (Add Task)
↓
CLI.prompt_for_title() → "" (empty input)
↓
Service.add_task("")
  ├─ Validate title non-empty ✗
  └─ Return (False, None, "Task title cannot be empty. Please try again.")
↓
CLI.display_message("Task title cannot be empty. Please try again.")
↓
Back to menu (or re-prompt, depending on design)
```

## Testing Strategy

Each layer is tested independently using `unittest`:

### Test Models (`test_models.py`)
```python
# Test Task initialization and attributes
def test_task_creation():
    task = Task(id=1, title="Test", completed=False)
    assert task.id == 1
    assert task.title == "Test"
    assert task.completed == False
```

### Test Storage (`test_storage.py`)
```python
# Test CRUD operations
def test_add_task():
    storage = TaskStorage()
    task = Task(id=0, title="Buy groceries", completed=False)
    added = storage.add_task(task)
    assert added.id == 1  # ID auto-assigned
    assert len(storage.get_all_tasks()) == 1

def test_delete_task():
    storage = TaskStorage()
    # ... add tasks ...
    success = storage.delete_task(1)
    assert success == True
    assert len(storage.get_all_tasks()) == 0
```

### Test Service (`test_service.py`)
```python
# Test validation and error handling
def test_add_task_with_empty_title():
    service = TaskService(TaskStorage())
    success, task, message = service.add_task("")
    assert success == False
    assert "cannot be empty" in message

def test_delete_nonexistent_task():
    service = TaskService(TaskStorage())
    success, message = service.delete_task(999)
    assert success == False
    assert "not found" in message
```

### Test CLI (`test_cli.py`)
```python
# Test menu rendering and input parsing
# Note: CLI testing often uses mock input/output to avoid interactive prompts
def test_menu_display(capsys):
    cli = TodoCLI(TaskService(TaskStorage()))
    cli.display_menu()
    captured = capsys.readouterr()
    assert "1. Add Task" in captured.out
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_service

# Run specific test
python -m unittest tests.test_service.TestTaskService.test_add_task
```

## Key Design Principles

1. **Separation of Concerns**: Each module has a single responsibility.
2. **No Business Logic in CLI**: CLI is dumb; service does validation.
3. **No Business Logic in Storage**: Storage is dumb; service does orchestration.
4. **Testable**: Each layer can be tested independently.
5. **Extensible**: Phase II can replace CLI with API, storage with database, without touching service.

## Next Steps

1. **Implement**: Use `/sp.tasks` to generate implementation tasks and code.
2. **Test**: Run test suite to verify all features work.
3. **Extend**: Phase II can add persistence, API, web UI using same architecture.

## FAQ

**Q: Can I run the app without Python 3.13?**
A: Phase I targets Python 3.13+ for consistency. Earlier versions may work but are untested.

**Q: Why no external libraries?**
A: The constitution prioritizes learning and portability. Phase II can add dependencies for persistence/API.

**Q: How do I debug a failing test?**
A: Add `print()` statements in your test, or use Python's debugger: `python -m pdb -m unittest tests.test_service`

**Q: Can I modify the architecture?**
A: No. Per the constitution, all changes are spec-driven. Propose changes by refining the specification first.

**Q: How does Phase II differ?**
A: Phase II adds persistence (database), API (FastAPI), and web UI. The service and model layers remain unchanged; storage and CLI are replaced.
