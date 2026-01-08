# Claude Code Instructions

This project uses **Claude Code** as the sole code author.
All source code must be generated from specifications using Spec-Kit Plus.
Manual code changes are strictly prohibited.

---

## Project Context

Project Name: Evolution of Todo  
Phase: Phase I – In-Memory Python Console Application

The goal is to implement a basic Todo application using a **spec-driven, agentic development workflow**.

---

## Authoring Rules (Strict)

- DO NOT write or modify code manually.
- DO NOT introduce features not explicitly defined in the active spec.
- DO NOT persist data to files or databases.
- DO NOT use external frameworks or libraries.
- DO NOT add AI, web, or network functionality.

---

## Technology Constraints

- Python version: 3.13+
- Execution mode: Console application
- Data storage: In-memory only
- Entry point: `src/main.py`

---

## Architectural Guidelines

Follow clean separation of concerns:

- `models.py`
  - Defines the Task data model
- `storage.py`
  - In-memory task storage and ID generation
- `service.py`
  - Business logic for task operations
- `cli.py`
  - User input/output and menu handling
- `main.py`
  - Application entry point

Avoid:

- Global mutable state outside storage layer
- Tight coupling between CLI and storage
- Redundant logic

---

## Spec-Driven Development Workflow

For every change:

1. Read the Constitution (`CONSTITUTION.md`)
2. Read the active specification from `specs-history/`
3. Generate an implementation plan
4. Generate code that satisfies ONLY the current spec
5. If output is incorrect:
   - Update the spec
   - Re-run Claude Code
   - Do not manually fix code
6. Generate phr in a good structure and file name

---

## Coding Standards

- Use type hints for all functions
- Use docstrings for public methods
- Use clear and descriptive variable names
- Follow PEP 8 formatting
- Handle invalid user input gracefully

---

## CLI Interaction Rules

- Present a numbered menu for user actions
- Prompt users clearly for required input
- Display task lists with completion indicators:
  - `[ ]` for incomplete
  - `[X]` for completed
- Display meaningful error messages

---

## Output Expectations

The application must support:

- Adding tasks (title + description)
- Viewing all tasks
- Updating existing tasks
- Deleting tasks by ID
- Marking tasks as complete or incomplete

All behavior must be traceable back to a specification.

---

## Enforcement

If any instruction conflicts with:

- A specification → Follow the specification
- The Constitution → Follow the Constitution
- This file → Follow this file

In case of ambiguity, ask for clarification **by refining the spec**, not by adding assumptions.

---

## Final Note

This repository will be reviewed for:

- Spec quality
- Spec evolution history
- Strict adherence to spec-driven development
- Clean architecture and maintainability

Claude Code must act as a disciplined engineering agent, not a creative assistant.
