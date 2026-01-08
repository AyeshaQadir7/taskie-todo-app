# Implementation Plan: Phase I – In-Memory Todo Console Application

**Branch**: `001-core-todo-crud` | **Date**: 2026-01-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-core-todo-crud/spec.md`

## Summary

Build a Python console-based todo application with core CRUD operations (Add, Delete, Update, View, Mark Complete) using in-memory storage and a menu-driven CLI interface. The design emphasizes clean architecture with strict separation of concerns: data model, storage layer, business logic, and CLI interaction. This foundation supports future evolution to persistent storage, web/API backends, and additional features without requiring major architectural refactoring.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory only (lists, dictionaries, dataclasses)
**Testing**: Python `unittest` (standard library)
**Target Platform**: Cross-platform console application (Linux, Windows, macOS)
**Project Type**: Single-module console application
**Performance Goals**: Instant response to user actions (<100ms); handle 1000+ tasks without degradation
**Constraints**: No external dependencies; no persistence; single-process; no concurrency
**Scale/Scope**: Single-user; ~5 core features; ~500 LOC target

## Constitution Check

✅ **Language**: Python 3.13+ — Compliant
✅ **Storage**: In-memory (lists/dicts/dataclasses) — Compliant
✅ **UI**: Console/CLI (menu-driven, stdin/stdout) — Compliant
✅ **External Libraries**: None (stdlib only) — Compliant
✅ **Entry Point**: `python src/main.py` — Compliant
✅ **Modular Architecture**: models.py, storage.py, service.py, cli.py, main.py — Compliant
✅ **Code Standards**: Type hints, docstrings, PEP 8, error handling required — Will be enforced in implementation
✅ **Spec-Driven Development**: All code generated from this plan — Compliant

All gates PASS. No violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-todo-crud/
├── spec.md                          # Feature specification
├── plan.md                          # This file (architecture & design)
├── research.md                      # Phase 0 (research findings - none required for this feature)
├── data-model.md                    # Phase 1 output (entity definitions)
├── quickstart.md                    # Phase 1 output (developer guide)
├── contracts/                       # Phase 1 output (API contracts - N/A for Phase I)
├── tasks.md                         # Phase 2 output (implementation tasks)
└── checklists/
    └── requirements.md              # Specification quality checklist
```

### Source Code (repository root)

```text
src/
├── main.py                          # Application entry point and orchestration
├── models.py                        # Task data model (dataclass)
├── storage.py                       # In-memory task storage and ID generation
├── service.py                       # Business logic (CRUD operations, validation)
└── cli.py                           # Menu interface and user interaction

tests/
├── test_models.py                   # Task model tests
├── test_storage.py                  # Storage layer tests
├── test_service.py                  # Business logic tests
└── test_cli.py                      # CLI interaction tests

README.md                            # Project documentation
```

**Structure Decision**: Single-module console application. Modules are separated by responsibility (models, storage, service, CLI, main) as defined in the constitution. This structure supports Phase II migration to a web/API backend by allowing storage and service layers to be reused unchanged, with only the CLI layer replaced by API handlers.

## Data Model Design

### Core Entity: Task

```python
class Task:
    id: int                  # Unique, auto-generated, sequential
    title: str              # Non-empty string, required
    completed: bool         # Default: False
```

**ID Generation Strategy**: Sequential counter in storage layer. Each new task receives ID = max(existing_ids) + 1, starting at 1.

**Validation Rules**:

- `title`: Must be non-empty and non-whitespace-only (strip whitespace; reject if empty after strip)
- `id`: Must be unique; auto-generated
- `completed`: Boolean flag (no validation needed)

**State Transitions**:

- Initial: `completed = False`
- User marks complete: `completed = True`
- User marks incomplete: `completed = False`
- No constraints on re-marking or toggling

## Architectural Layers

### Layer 1: Data Model (`models.py`)

**Responsibility**: Define the Task entity with minimal logic.

**Interface**:

```
Task(id: int, title: str, completed: bool)
  - Attributes: id, title, completed
  - Methods: None (dataclass, use properties if needed)
```

**Key Principles**:

- Dataclass definition; no methods except `__init__`, `__repr__`
- All validation delegated to service layer
- Immutable attributes (optional: use frozen=False to allow updates via service)

### Layer 2: Storage (`storage.py`)

**Responsibility**: Manage in-memory task collection and ID generation. Zero business logic.

**Interface**:

```
class TaskStorage:
  __init__()
    - Initialize empty list of tasks
    - Initialize ID counter

  add_task(task: Task) -> Task
    - Append task to storage
    - Return task with assigned ID

  get_task(id: int) -> Task | None
    - Return task by ID, or None if not found

  get_all_tasks() -> list[Task]
    - Return all tasks in order

  update_task(id: int, title: str) -> bool
    - Update task title; return True if successful, False if not found

  delete_task(id: int) -> bool
    - Remove task by ID; return True if successful, False if not found

  mark_complete(id: int) -> bool
    - Set task.completed = True; return True if successful

  mark_incomplete(id: int) -> bool
    - Set task.completed = False; return True if successful

  list_ids() -> list[int]
    - Return all task IDs for error messages
```

**Key Principles**:

- No validation (service layer handles this)
- No business logic beyond CRUD and ID management
- Single source of truth for task state
- Return None or False to signal "not found"; service layer translates to user messages

### Layer 3: Service (`service.py`)

**Responsibility**: Business logic—validation, error handling, CRUD orchestration.

**Interface**:

```
class TaskService:
  __init__(storage: TaskStorage)

  add_task(title: str) -> tuple[bool, Task | None, str]
    - Validate title (non-empty, non-whitespace)
    - Create Task with next ID
    - Call storage.add_task()
    - Return (success: bool, task: Task | None, message: str)

  list_tasks() -> list[Task]
    - Delegate to storage.get_all_tasks()

  update_task(id: int, title: str) -> tuple[bool, Task | None, str]
    - Validate task exists
    - Validate title (non-empty, non-whitespace)
    - Call storage.update_task()
    - Return (success, updated_task, message)

  delete_task(id: int) -> tuple[bool, str]
    - Validate task exists
    - Call storage.delete_task()
    - Return (success, message with available IDs if failure)

  mark_complete(id: int) -> tuple[bool, Task | None, str]
    - Validate task exists
    - Call storage.mark_complete()
    - Return (success, updated_task, message)

  mark_incomplete(id: int) -> tuple[bool, Task | None, str]
    - Validate task exists
    - Call storage.mark_incomplete()
    - Return (success, updated_task, message)
```

**Validation Rules**:

- Title: Strip whitespace; reject if empty
- Task ID: Check existence via storage.list_ids()
- Return user-friendly error messages with available IDs

### Layer 4: CLI (`cli.py`)

**Responsibility**: Menu rendering, input parsing, output formatting. Zero business logic.

**Interface**:

```
class TodoCLI:
  __init__(service: TaskService)

  display_menu() -> None
    - Print main menu with 6 options (1-6)

  run() -> None
    - Loop: display_menu() → handle_choice() until exit

  handle_choice(choice: int) -> bool
    - Route to menu option (1=add, 2=delete, 3=update, 4=view, 5=toggle, 6=exit)
    - Return False if exit, True to continue loop

  get_menu_choice() -> int | None
    - Prompt for choice 1-6
    - Validate input (must be numeric, 1-6)
    - Return choice or None if invalid
    - Print error and retry on invalid input

  display_tasks(tasks: list[Task]) -> None
    - Print "No tasks" if empty
    - For each task: print "[X]" or "[ ]" + "Task #ID: title"

  prompt_for_title(action: str) -> str
    - Prompt user for task title (e.g., "Enter task title:")
    - Return input (let service validate)

  prompt_for_id() -> int | None
    - Prompt user for task ID
    - Validate numeric input
    - Return ID or None if invalid

  display_message(message: str) -> None
    - Print message to user
```

**Key Principles**:

- No validation; service validates all inputs
- Menu loops and retries on invalid input
- Clear error messages with available IDs
- Status display: `[ ]` for incomplete, `[X]` for complete

### Layer 5: Main (`main.py`)

**Responsibility**: Entry point and orchestration.

**Interface**:

```
def main() -> None:
    - Create TaskStorage
    - Create TaskService(storage)
    - Create TodoCLI(service)
    - Call cli.run()

if __name__ == "__main__":
    main()
```

## Control Flow

### User Launches Application

```
1. main.py: Create storage → service → CLI
2. CLI.run() starts menu loop
3. Display main menu (options 1-6)
4. Get user choice
5. Handle choice → call service → display result
6. Return to menu or exit (step 3)
```

### Add Task Flow

```
1. CLI: Prompt for title
2. Service: Validate title (non-empty, non-whitespace)
   - If invalid: print error, return to menu
3. Service: Call storage.add_task(Task(id=next, title=title, completed=False))
4. CLI: Display "Task added: Task #ID: title"
5. Return to menu
```

### Delete Task Flow

```
1. CLI: Prompt for task ID
2. CLI: Validate input is numeric
   - If invalid: print error, retry
3. Service: Validate task exists
   - If not found: print "Task ID X not found. Available IDs: 1, 2, 3"
4. Service: Call storage.delete_task(id)
5. CLI: Display "Task #ID deleted. X tasks remaining."
6. Return to menu
```

### View Tasks Flow

```
1. CLI: Call service.list_tasks()
2. CLI: Display tasks with status indicators
   - [ ] Task #1: Buy groceries
   - [X] Task #2: Review PRs
3. Return to menu
```

### Exit Flow

```
1. User selects option 6 (Exit)
2. CLI: Print "Goodbye!"
3. CLI.run() returns
4. main() terminates
```

## Error Handling Strategy

**At Service Layer**: Validate all inputs; return (success: bool, result, message: str).

**At CLI Layer**:

- Get numeric input → validate is int, is 1-6 → retry on invalid
- Get title input → pass to service → let service validate
- Get task ID → validate is int → let service check existence

**Error Messages** (per spec):

- Empty title: "Task title cannot be empty. Please try again."
- Non-existent ID: "Task ID 5 not found. Available IDs: 1, 2, 3."
- Non-numeric menu: "Invalid input. Please enter a number corresponding to a menu option."
- Out-of-range menu: "Option 7 does not exist. Please select 1-6."

**No Crashes**: All exceptions caught at CLI layer; invalid input triggers error message and retry, not application termination.

## Design Decisions

| Decision          | Choice                                     | Rationale                                                                                     |
| ----------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| Task ID Strategy  | Sequential integer, auto-generated         | Simple, deterministic, matches user expectations. No gaps in numbering.                       |
| Storage Structure | List of Task objects                       | Simple, in-memory, supports iteration and ID lookup. Adequate for <1000 tasks.                |
| ID Lookup         | Linear search by ID                        | Acceptable for <1000 tasks. Phase II can add indexing if needed.                              |
| Error Handling    | Service returns (success, result, message) | Decouples CLI from validation logic; allows testing service independently.                    |
| Menu Choice       | Numeric input 1-6                          | Beginner-friendly; matches spec; easy to validate.                                            |
| Status Display    | `[ ]` and `[X]`                            | Per spec; clear visual indicator; easy to parse.                                              |
| Module Structure  | 5 separate files                           | Follows constitution; supports Phase II migration to API (keep storage/service, replace CLI). |
| Testing           | unittest (stdlib)                          | No external dependencies; testing required by constitution.                                   |

## Phase II Evolution Path

This architecture prepares for Phase II (persistence, API, web UI) by:

1. **Storage Layer**: Swap in-memory list for database query layer. Service interface unchanged.
2. **Service Layer**: Unchanged. Can be used by both CLI and API.
3. **CLI Layer**: Remove entirely; replace with Flask/FastAPI handlers. Service handles requests.
4. **Models Layer**: Can add fields (description, due_date, tags) without touching storage/service.

Example Phase II refactor:

- **Phase I**: `CLI → Service → Storage (in-memory list)`
- **Phase II**: `API (FastAPI) → Service → Storage (PostgreSQL)` + keep original CLI as legacy

## Testing Strategy

Each layer has independent tests:

- **test_models.py**: Task dataclass initialization, attributes
- **test_storage.py**: add, get, update, delete, mark_complete/incomplete
- **test_service.py**: Validation, error messages, business logic
- **test_cli.py**: Menu rendering, input parsing, user flow simulation

All tests use stdlib `unittest`; no external test dependencies.

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
