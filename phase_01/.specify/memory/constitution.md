# Evolution of Todo — Phase I Constitution

## Core Principles

### I. Simplicity-First Design

Prioritize clarity and functional correctness over premature optimization. The application is a console MVP suitable for beginners. Design decisions should enable incremental evolution without blocking Phase II features (persistence, web UI, or distributed features).

### II. No External Dependencies

The implementation uses **Python 3.13+ standard library only**. This constraint ensures portability and teaches fundamental principles (input validation, data structures, state management).

### III. In-Memory Storage Only

All task data exists in Python objects (lists, dictionaries, dataclasses) during runtime. No files, databases, or persistence mechanisms. Tasks are lost on application exit. This clarifies the scope of Phase I and prepares for Phase II persistence.

### IV. Console-Based Interaction

Single entry point: `python src/main.py`. User interaction occurs via numbered menus and text prompts. Output includes task lists with clear completion indicators (`[ ]` incomplete, `[X]` complete). All user input must be validated; invalid input produces helpful error messages, never crashes.

### V. Spec-Driven Development (Non-Negotiable)

All code is generated from active specifications. Manual code edits are forbidden. If behavior is incorrect:

1. Refine the spec to clarify intent.
2. Re-run code generation.
3. Never patch code directly.

This enforces discipline and ensures all behavior is traceable to requirements.

### VI. Clean Architecture & Modularity

Strict separation of concerns:

- **models.py**: Task data model (attributes, minimal logic)
- **storage.py**: In-memory storage, ID generation, no business rules
- **service.py**: Task CRUD operations, validation, business logic
- **cli.py**: Menu, input prompts, output formatting
- **main.py**: Entry point, orchestration only

No global mutable state outside storage. CLI must not directly manipulate storage; all mutations flow through service layer.

## Technology Constraints

| Aspect             | Requirement                              |
| ------------------ | ---------------------------------------- |
| Language           | Python 3.13+                             |
| Storage            | In-memory (lists, dicts, dataclasses)    |
| UI                 | Console only (stdin/stdout)              |
| External Libraries | None (standard library only)             |
| Entry Point        | `python src/main.py`                     |
| Required Features  | Add, Delete, Update, View, Mark Complete |
| Task Attributes    | ID (unique), Title, Completion Status    |

## Code Standards

- **Type Hints**: Required on all function signatures
- **Docstrings**: Required for all public methods (module, class, function)
- **Error Handling**: Graceful degradation; no unhandled exceptions visible to user
- **Naming**: Descriptive, snake_case for functions/variables, PascalCase for classes
- **Comments**: Explain intent, not obvious logic; clarify "why", not "what"
- **PEP 8**: Strict adherence (4-space indents, max line length 88 or context-appropriate)
- **Testing**: All business logic must be testable; tests live in `tests/` directory

## CLI Interaction Rules

1. **Menu-Driven**: Present numbered options, accept integer input
2. **Prompts**: Clear, concise language; no jargon
3. **Task Display**:
   ```
   [ ] Task #1: Buy groceries
   [X] Task #2: Review PRs
   ```
4. **Error Messages**: Specific guidance (e.g., "Task ID 5 not found. Available: 1, 2, 3")
5. **Exit Gracefully**: "Goodbye!" message; clean shutdown

## Required Features

| Feature         | Input               | Output                         | Validation                        |
| --------------- | ------------------- | ------------------------------ | --------------------------------- |
| Add Task        | Title (string)      | Confirmation + task ID         | Title required, non-empty         |
| Delete Task     | Task ID             | Confirmation + remaining count | ID must exist                     |
| Update Task     | Task ID + new title | Updated task + confirmation    | ID must exist, new title required |
| View Tasks      | (none)              | Numbered list with status      | Show "No tasks" if empty          |
| Mark Complete   | Task ID             | Updated task + status          | ID must exist                     |
| Mark Incomplete | Task ID             | Updated task + status          | ID must exist                     |

## Success Criteria

- ✓ Application runs without errors from clean start
- ✓ All 6 features work as specified
- ✓ User can interact via menu continuously until explicit exit
- ✓ Tasks persist in-memory during runtime
- ✓ Code is modular, readable, and extensible
- ✓ Invalid input handled gracefully (no crashes)
- ✓ Clear CRUD understanding and state management demonstrated

## Governance

**Constitution Supersedes**: All architectural guidance, code reviews, and PR processes must verify compliance with this constitution. When conflicts arise:

1. **Constitution** (this document) → Authority
2. **Active Specification** (in `specs/`) → Implements constitution
3. **This file** (`CLAUDE.md`) → Directs workflow

**Amendments**: Any change to core principles requires:

- Documentation of rationale
- Impact assessment on existing code
- Explicit user consent before implementation

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
