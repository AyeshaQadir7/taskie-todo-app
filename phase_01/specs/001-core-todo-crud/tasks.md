---
description: "Task list for Phase I – In-Memory Todo Console Application"
---

# Tasks: Phase I – In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-core-todo-crud/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (optional)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Three user stories with two P2 stories running in parallel after P1 MVP completion.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths in descriptions
- Checkbox format: `- [ ]` (required)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Checkpoint**: Project skeleton ready; all src/ and tests/ directories exist; can import modules

- [x] T001 Create project directory structure per plan.md in src/ (models, storage, service, cli, main)
- [x] T002 [P] Initialize tests/ directory with __init__.py for test discovery
- [x] T003 [P] Create README.md with project overview, running instructions, and architecture diagram

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement Task dataclass in src/models.py (id: int, title: str, completed: bool = False)
- [x] T005 [P] Implement TaskStorage class in src/storage.py with:
  - `__init__()` method initializing empty tasks list and next_id counter
  - `add_task(task: Task) -> Task` with auto-generated sequential IDs
  - `get_all_tasks() -> list[Task]` returning all tasks in order
  - `get_task(id: int) -> Task | None` returning task by ID
  - `list_ids() -> list[int]` returning all task IDs for error messages
  - `update_task(id: int, title: str) -> bool` returning success
  - `delete_task(id: int) -> bool` returning success
  - `mark_complete(id: int) -> bool` returning success
  - `mark_incomplete(id: int) -> bool` returning success
- [x] T006 [P] Implement TaskService class in src/service.py with:
  - `__init__(storage: TaskStorage)` taking storage dependency
  - `add_task(title: str) -> tuple[bool, Task | None, str]` validating and creating tasks
  - `list_tasks() -> list[Task]` delegating to storage
  - `update_task(id: int, title: str) -> tuple[bool, Task | None, str]` with validation
  - `delete_task(id: int) -> tuple[bool, str]` returning success and available IDs on failure
  - `mark_complete(id: int) -> tuple[bool, Task | None, str]` with validation
  - `mark_incomplete(id: int) -> tuple[bool, Task | None, str]` with validation
- [x] T007 [P] Implement TodoCLI class in src/cli.py with:
  - `__init__(service: TaskService)` taking service dependency
  - `display_menu() -> None` printing main menu with 6 options (1-6)
  - `run() -> None` implementing main loop until exit
  - `get_menu_choice() -> int | None` validating numeric input 1-6 with retry
  - `display_tasks(tasks: list[Task]) -> None` with status indicators `[ ]` and `[X]`
  - `prompt_for_title(action: str) -> str` getting user input for task title
  - `prompt_for_id() -> int | None` validating numeric ID input
  - `display_message(message: str) -> None` printing messages to user
- [x] T008 Implement entry point in src/main.py:
  - `def main() -> None:` creating storage → service → cli and starting cli.run()
  - `if __name__ == "__main__": main()` guard for direct execution

**Checkpoint**: Foundation ready - all 5 modules implemented with correct interfaces; user story implementation can now begin

---

## Phase 3: User Story 1 - Create and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement core CRUD operations (Add, Delete, Update, View, Mark Complete) with menu-driven CLI

**Independent Test**: Launch app → add task → view list → mark complete → update title → delete task → exit. All operations succeed without crashes; task state persists in-memory during session.

**User Scenarios Covered**:
1. Add task with unique auto-generated ID (US1 scenario 1)
2. Mark task as complete with `[X]` indicator (US1 scenario 2)
3. Update task title while preserving ID (US1 scenario 3)
4. Delete task by ID from list (US1 scenario 4)
5. View all tasks with both complete and incomplete indicators (US1 scenario 5)

### Implementation for User Story 1

- [x] T009 [US1] Implement `add_task()` menu option in src/cli.py:
  - Prompt user for task title
  - Call service.add_task(title)
  - Display success message with task ID or error message
  - Return to menu on success or allow retry on error

- [x] T010 [US1] Implement `view_tasks()` menu option in src/cli.py:
  - Call service.list_tasks()
  - Display "No tasks yet" if empty
  - Display each task with format: `[status] Task #ID: title`
  - Status: `[ ]` for incomplete, `[X]` for complete
  - Return to menu

- [x] T011 [US1] Implement `mark_complete()` menu option in src/cli.py:
  - Prompt user for task ID
  - Call service.mark_complete(id)
  - Display success message or error message with available IDs
  - Return to menu

- [x] T012 [US1] Implement `update_task()` menu option in src/cli.py:
  - Prompt user for task ID to update
  - Prompt for new title
  - Call service.update_task(id, title)
  - Display success message or error message
  - Return to menu

- [x] T013 [US1] Implement `delete_task()` menu option in src/cli.py:
  - Prompt user for task ID to delete
  - Call service.delete_task(id)
  - Display success message with remaining count or error message
  - Return to menu

- [x] T014 [US1] Implement `exit()` menu option in src/cli.py:
  - Display "Goodbye!"
  - Return False from handle_choice() to exit loop
  - Terminate application cleanly

- [x] T015 [US1] Add all FR requirements in src/service.py validation:
  - FR-002: Accept title string and create task with auto-generated ID
  - FR-003: Store tasks in-memory in storage.py list
  - FR-004: View tasks with ID, title, completion status
  - FR-005: Mark complete by ID
  - FR-006: Mark incomplete by ID (support toggle)
  - FR-007: Update title by ID
  - FR-008: Delete by ID
  - FR-009: Validate all input; invalid input → error message + retry (no crash)
  - FR-010: Assign sequential increasing IDs (1, 2, 3...)
  - FR-011: Display status as `[ ]` and `[X]`
  - FR-012: Exit option with "Goodbye!" message
  - FR-013: Return to menu after each operation

**Checkpoint**: User Story 1 fully functional and independently testable. User can perform complete CRUD cycle: add → view → mark complete → update → delete → exit without crashes.

---

## Phase 4: User Story 2 - Input Validation and Error Handling (Priority: P2)

**Goal**: Handle all invalid user inputs gracefully with specific, helpful error messages

**Independent Test**: Enter empty title → error + retry. Enter non-existent ID → error with available IDs. Enter non-numeric menu → error + retry. Enter out-of-range menu → error + retry. Verify app never crashes.

**User Scenarios Covered**:
1. Empty or whitespace-only title validation (US2 scenario 1)
2. Non-existent task ID error with available IDs listed (US2 scenario 2)
3. Non-numeric menu input error (US2 scenario 3)
4. Out-of-range menu option error (US2 scenario 4)
5. Error messages allow retry without termination (US2 scenario 5)

### Implementation for User Story 2

- [x] T016 [P] [US2] Add title validation in src/service.py:
  - Validate title is not empty after whitespace strip
  - Return (False, None, "Task title cannot be empty. Please try again.") if invalid
  - All add_task() and update_task() calls use this validation

- [x] T017 [P] [US2] Add ID existence validation in src/service.py:
  - For delete_task(), mark_complete(), mark_incomplete(), update_task():
  - Check if ID exists in storage via storage.list_ids()
  - If not found, return (False, None/error_str, f"Task ID {id} not found. Available IDs: {ids_list}")
  - Allow listing of available IDs in error message

- [x] T018 [P] [US2] Add menu input validation in src/cli.py get_menu_choice():
  - Try to parse user input as integer
  - If parse fails (non-numeric), display "Invalid input. Please enter a number corresponding to a menu option."
  - If integer parsed but not in 1-6, display "Option {choice} does not exist. Please select 1-6."
  - On any error, prompt user to retry without crashing

- [x] T019 [P] [US2] Add ID input validation in src/cli.py prompt_for_id():
  - Try to parse user input as integer
  - If parse fails, display "Invalid task ID. Please enter a number."
  - Allow retry or return to menu
  - No crash on invalid input

- [x] T020 [P] [US2] Add exception handling in src/cli.py run() loop:
  - Wrap all user interactions in try-except to catch unexpected errors
  - Display "An unexpected error occurred. Returning to menu." (never show traceback to user)
  - Return to menu on any exception
  - Application never crashes due to invalid user input

- [x] T021 [US2] Add specific error messages for each scenario per spec.md:
  - Empty title: exact message from spec (FR-009)
  - Non-existent ID: exact message with available IDs (FR-009)
  - Non-numeric menu: exact message from spec (FR-009)
  - Out-of-range menu: exact message from spec (FR-009)

**Checkpoint**: All invalid input scenarios handled gracefully. User Story 2 independently testable. App does not crash on any documented invalid input.

---

## Phase 5: User Story 3 - Continuous Application Flow and Exit (Priority: P2)

**Goal**: Ensure menu loops correctly and clean exit works

**Independent Test**: Perform 5+ consecutive operations (add → view → mark → update → delete → view) with menu returning after each. Select exit and verify "Goodbye!" message and clean termination. Restart and verify empty list (in-memory reset).

**User Scenarios Covered**:
1. Menu returns after each operation (US3 scenario 1)
2. Application stable for 5+ consecutive operations (US3 scenario 2)
3. Clean exit with "Goodbye!" message (US3 scenario 3)
4. Restart resets in-memory storage to empty (US3 scenario 4)

### Implementation for User Story 3

- [x] T022 [P] [US3] Implement menu loop in src/cli.py run() method:
  - `while True: display_menu() → get_choice() → handle_choice()`
  - handle_choice() returns True to continue, False to exit
  - Loop exits cleanly when option 6 (Exit) selected

- [x] T023 [P] [US3] Implement handle_choice() dispatch in src/cli.py:
  - Route option 1 → add_task flow
  - Route option 2 → delete_task flow
  - Route option 3 → update_task flow
  - Route option 4 → view_tasks flow
  - Route option 5 → mark_complete/incomplete flow
  - Route option 6 → exit (return False)
  - All options except 6 return True to continue loop

- [x] T024 [P] [US3] Add menu loop continuation test:
  - After each operation, verify menu reappears
  - Verify user can perform next operation without restart
  - Verify state persists (newly added task visible in next view)

- [x] T025 [P] [US3] Implement clean exit in src/cli.py:
  - When option 6 selected: display "Goodbye!"
  - Return False from handle_choice() to exit loop
  - src/main.py main() returns normally
  - Application terminates (no hanging processes)

- [x] T026 [US3] Verify in-memory reset on restart:
  - Add task → exit application → restart application
  - Verify view_tasks shows "No tasks" (storage was recreated in main())
  - Confirm each restart creates fresh TaskStorage() instance

- [x] T027 [US3] Add state persistence tests in menu loop:
  - Create 3 tasks in single session
  - Mark task 1 complete
  - Delete task 2
  - Verify view shows [X] task #1, [ ] task #3 (correct IDs, status)
  - Perform 10 consecutive operations without state loss or crash

**Checkpoint**: User Story 3 fully functional. Menu loops correctly. Application exits cleanly. In-memory storage resets on restart. User can perform many consecutive operations without state loss.

---

## Phase 6: Polish & Integration Testing

**Purpose**: Final validation that all three user stories work together; all requirements met; app is production-ready for Phase I

### Integration Testing

- [x] T028 [P] Run end-to-end acceptance scenario test in tests/ (optional, can be manual):
  - Launch application
  - Add task "Buy groceries"
  - View tasks (verify [ID] [ ] Task #ID: Buy groceries)
  - Add task "Review PRs"
  - Mark task 1 complete (verify [X])
  - Update task 2 to "Code review"
  - Delete task 1
  - View tasks (verify only task 2 remains with updated title)
  - Perform 5 more operations
  - Exit (verify "Goodbye!")
  - Restart (verify empty list)
  - All without crashes

- [x] T029 [P] Verify all code standards per constitution:
  - All functions have type hints (args and return type)
  - All public methods have docstrings
  - PEP 8 compliant (4-space indents, line length ~88 or reasonable)
  - No global mutable state outside storage layer
  - Error handling: no unhandled exceptions visible to user

- [x] T030 [P] Create unit test skeletons in tests/:
  - test_models.py - Task dataclass tests (optional)
  - test_storage.py - TaskStorage CRUD tests (optional)
  - test_service.py - TaskService validation tests (optional)
  - test_cli.py - CLI interaction tests (optional)
  - Note: Full test implementation optional; skeletons satisfy constitution requirement for testability

- [x] T031 Verify all functional requirements implemented:
  - Checklist all FRs from spec.md (FR-001 through FR-013)
  - Each FR has implementation task linked
  - Each FR manually verified in end-to-end test (T028)

- [x] T032 Verify all success criteria met:
  - SC-001: All 5 features work without crashes ✓ (T009-T014 + manual test T028)
  - SC-002: 10+ operations in one session without state loss ✓ (T027)
  - SC-003: 100% invalid input handling ✓ (T016-T020)
  - SC-004: Clean exit with "Goodbye!" ✓ (T025)
  - SC-005: Code understandable for 30-min Phase II extension ✓ (constitutionalcode standards T029 + design docs)
  - SC-006: Clean architecture (models, storage, service, CLI, main separated) ✓ (T004-T008)

- [x] T033 Final code review:
  - Check all 5 modules follow architecture from plan.md
  - Verify no business logic in CLI or Storage
  - Verify no logic in models (dataclass only)
  - Verify service handles all validation
  - All layer responsibilities respected (T004-T008 contracts)

**Checkpoint**: Phase I complete. All user stories integrated and functional. All requirements met. All success criteria verified. Application ready for demonstration and Phase II evolution.

---

## Summary & Execution Strategy

**Total Tasks**: 33 (T001-T033)

**Task Breakdown by Phase**:
- Phase 1 (Setup): 3 tasks (T001-T003)
- Phase 2 (Foundation): 5 tasks (T004-T008)
- Phase 3 (US1 - MVP): 7 tasks (T009-T015)
- Phase 4 (US2 - Validation): 7 tasks (T016-T021)
- Phase 5 (US3 - Flow): 8 tasks (T022-T027)
- Phase 6 (Polish): 6 tasks (T028-T033)

**MVP Scope**: Phases 1, 2, 3 (T001-T015)
- Delivers: Complete CRUD (add, view, mark complete, update, delete) + menu + exit
- Independently testable: Yes (core functionality from spec.md User Story 1)
- Estimated LOC: ~400

**Full Scope (All Phases)**: T001-T033
- Adds: Input validation + error handling + menu loop reliability + integration tests
- Estimated LOC: ~500

**Parallelization Opportunities**:

- **Phase 1**: T002, T003 can run in parallel with T001 (different files)
- **Phase 2**: T005, T006, T007 can run in parallel (different files, all depend on T004 models)
  - Sequential: T004 → (T005, T006, T007 in parallel) → T008
- **Phase 3**: T009-T014 can run in parallel after foundation complete (different menu options, all use same service)
  - All read from same service, write to different CLI handlers
  - Sequential: Foundation (T004-T008) → (T009-T015 with T009-T014 parallel, T015 final)
- **Phase 4**: T016-T020 can run in parallel (different validation locations, same service/CLI interaction)
  - Sequential: Phase 3 → (T016-T020 in parallel) → T021
- **Phase 5**: T022-T026 can run in parallel (different flow aspects, same main loop)
  - Sequential: Phase 4 → (T022-T026 in parallel) → T027
- **Phase 6**: T028-T032 can run in parallel (different concerns, final integration last)
  - Sequential: Phase 5 → (T028-T032 in parallel) → T033

**Estimated Implementation Time**:
- MVP (Phases 1-3): 4-6 hours
- Full (Phases 1-6): 6-8 hours
- Parallel execution could reduce by ~30%

**Definition of Done**:
- All tasks completed (checkboxes checked)
- All user stories independently testable
- All requirements (FR) implemented and verified
- All success criteria (SC) validated
- All code standards (constitution) met
- Application runs: `python src/main.py` without errors
- User can complete CRUD cycle without crashes

---

## Dependency Graph

```
T001 (Setup structure)
  ↓
T002, T003 (Setup - parallel)
  ↓
T004 (Models - foundational)
  ↓
T005, T006, T007 (Storage, Service, CLI - parallel, depend on T004)
  ↓
T008 (Main - depends on T005-T007)
  ↓
T009-T014 (US1 MVP - parallel menu options, depend on T008)
  ├─ T015 (FR requirements for US1)
  ↓
T016-T020 (US2 Validation - parallel, depend on US1)
  ├─ T021 (Specific error messages for US2)
  ↓
T022-T026 (US3 Flow - parallel, depend on US2)
  ├─ T027 (State persistence tests)
  ↓
T028-T032 (Polish - parallel, integration test T033 depends on all)
  ↓
T033 (Final code review - gates completion)
```

---

## Next Step

Run `/sp.implement` to generate code for all tasks in priority order, starting with Phase 1 Setup.
