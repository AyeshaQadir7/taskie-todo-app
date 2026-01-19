# Data Model: Phase I – In-Memory Todo Console Application

**Created**: 2026-01-02 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Entity Definitions

### Task

Represents a single todo item in the application.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | `int` | Unique, auto-generated, sequential | System-assigned unique identifier. Starts at 1, increments by 1 for each new task. Never reused. |
| `title` | `str` | Required, non-empty, non-whitespace-only | Human-readable task description. User-provided. Stripped of leading/trailing whitespace before validation. |
| `completed` | `bool` | Required | Completion flag. Default: `False`. User can toggle between `True` and `False` at any time. |

**Initialization**:
```python
Task(id: int, title: str, completed: bool = False)
```

**Default Values**:
- `completed`: `False` (all new tasks start incomplete)

**Validation Rules** (enforced by Service layer, not Model):
- `title`: After stripping whitespace, must be non-empty (len > 0)
- `id`: Must be unique across all tasks; auto-assigned by Storage layer
- `completed`: No validation needed (boolean)

**State Transitions**:
- New task: `completed = False` (default)
- User marks complete: `completed = True` (allowed at any time)
- User marks incomplete: `completed = False` (allowed at any time)
- Edit title: `title` updated; `id` and `completed` unchanged
- No other state changes

**Immutability**:
- `id`: Assigned once at creation; never changes
- `title`: Mutable; updated via service layer
- `completed`: Mutable; toggled via service layer

**Display Format** (in CLI):
```
[ ] Task #1: Buy groceries     (incomplete)
[X] Task #2: Review PRs        (complete)
```

## Storage Model

**Collection Type**: List of Task objects

**In-Memory Representation**:
```python
tasks: list[Task] = []  # Initially empty; grows as user adds tasks
next_id: int = 1         # Counter for auto-generating IDs
```

**ID Assignment**:
- First task created: `id = 1`
- Second task: `id = 2`
- If a task is deleted, the ID is not reused
- Example sequence: Tasks 1, 2, 3 exist. Delete 2. Next task created gets `id = 4` (not `id = 3`)

**Lookup Strategy**:
- Search by ID: Linear search through list (O(n), acceptable for <1000 tasks)
- List all tasks: Return full list in order

**Memory Footprint**:
- Per task: ~64 bytes (id: 8, title: 20-50+, completed: 1, Python overhead: ~35)
- For 1000 tasks: ~64 KB (negligible)

## Relationships

In Phase I, there are no relationships. Tasks are independent.

**Future relationships** (Phase II):
- Task → Category (one-to-many)
- Task → User (many-to-one)
- Task → Subtasks (one-to-many)

## Constraints & Edge Cases

### Edge Case: Repeated Completion Toggle
**Scenario**: User marks Task #1 complete, then marks it complete again.
**Behavior**: Allow (no error). `completed` remains `True`.

### Edge Case: ID Gaps
**Scenario**: Tasks 1, 2, 3 exist. Delete Task 2.
**Behavior**: Tasks 1, 3 remain. Next new task gets `id = 4` (not reusing deleted ID 2).
**Why**: Simpler logic; IDs remain unique identifiers of "creation order"; no collision risk.

### Edge Case: Long Titles
**Scenario**: User enters a 1000+ character title.
**Behavior**: Accept and store the full title. Display may wrap or truncate in CLI, but stored value is unchanged. Service layer does not truncate.

### Edge Case: Empty Task List
**Scenario**: User launches app with no tasks; selects "View Tasks".
**Behavior**: Display "No tasks" message. Not an error.

### Edge Case: Maximum Tasks
**Scenario**: User creates 10,000+ tasks.
**Behavior**: No explicit limit in Phase I. Python list will grow dynamically. Performance acceptable for typical single-user workloads. Phase II can add pagination or archiving.

## Validation & Error Handling

**Validation Layer**: Service layer only (not Model or Storage).

**Validation Rules**:

| Input | Rule | Action on Failure |
|-------|------|------------------|
| Task title (add/update) | Non-empty after whitespace strip | Service returns error; CLI prompts for retry |
| Task ID (delete/update/toggle) | Must exist in storage | Service returns error listing available IDs |
| Menu choice (1-6) | Must be numeric int in range | CLI prompts for retry |

**Error Messages**:
- Title validation: "Task title cannot be empty. Please try again."
- ID not found: "Task ID 5 not found. Available IDs: 1, 2, 3."
- Menu validation: "Invalid input. Please enter a number corresponding to a menu option."
- Menu out-of-range: "Option 7 does not exist. Please select 1-6."

## Phase II Evolution

**Additions** (without breaking Phase I):

1. **New Task Fields**:
   - `description` (string, optional)
   - `due_date` (string or date, optional)
   - `priority` (enum: low, medium, high, optional)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)

2. **New Entities**:
   - `Category`: Group tasks by category
   - `Project`: Group tasks by project
   - `User`: Support multi-user

3. **Persistence**:
   - Replace in-memory list with database (PostgreSQL, SQLite)
   - Storage layer becomes ORM/query layer
   - Service layer unchanged (same interface)

4. **Example Phase II Task Entity**:
   ```python
   @dataclass
   class Task:
       id: int
       user_id: int  # NEW
       title: str
       description: str = ""  # NEW
       completed: bool = False
       priority: str = "medium"  # NEW
       category_id: int | None = None  # NEW
       due_date: str | None = None  # NEW
       created_at: str = None  # NEW (auto-set)
       updated_at: str = None  # NEW (auto-set)
   ```

**Migration Path**:
- Phase I Task → Phase II Task with new optional fields (all default to existing values)
- Service layer logic extends (new validation for new fields)
- Storage layer swaps to database (query interface changes, service interface same)
- CLI layer unchanged (still calls service methods)

## Summary

The Phase I data model is minimal: three fields on a Task entity. Validation is centralized in the Service layer. Storage uses a simple in-memory list with sequential ID generation. This design is simple, testable, and extensible for Phase II without requiring architectural changes.
