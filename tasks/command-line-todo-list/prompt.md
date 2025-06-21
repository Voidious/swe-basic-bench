# Command-Line To-Do List Application

## Objective

Create a command-line application to manage a to-do list.

## Requirements

The application should be a Python script named `todo.py` inside the `solution/` directory. It must support the following commands:

1.  **`add <task>`**: Adds a new task to the to-do list.
    *   `<task>` is a string describing the task.
    *   Tasks should be stored in a file named `tasks.json` in the `solution/` directory.

2.  **`list`**: Lists all the tasks with their corresponding index and status.
    *   The format should be: `[index] [status] - <task description>`
    *   Example of a completed task: `1. [x] - Buy milk`
    *   Example of an incomplete task: `2. [ ] - Walk the dog`
    *   If there are no tasks, it should print `No tasks yet.`

3.  **`complete <index>`**: Marks a task as complete.
    *   `<index>` is the 1-based index of the task to mark as complete.

4.  **`delete <index>`**: Deletes a task from the list.
    *   `<index>` is the 1-based index of the task to be deleted.

## Storage

The to-do list tasks should be persisted in a JSON file named `tasks.json` located in the `solution` directory. The application should create this file if it doesn't exist.

The JSON structure can be a list of objects, for example:
```json
[
    {"task": "Buy milk", "completed": true},
    {"task": "Walk the dog", "completed": false}
]
```

## Example Usage

```sh
# Add tasks
python solution/todo.py add "Buy groceries"
python solution/todo.py add "Pay electricity bill"

# List tasks
python solution/todo.py list
# Expected output:
# 1. [ ] - Buy groceries
# 2. [ ] - Pay electricity bill

# Complete a task
python solution/todo.py complete 1

# List tasks again
python solution/todo.py list
# Expected output:
# 1. [x] - Buy groceries
# 2. [ ] - Pay electricity bill

# Delete a task
python solution/todo.py delete 2

# List tasks again
python solution/todo.py list
# Expected output:
# 1. [x] - Buy groceries

# List empty tasks
python solution/todo.py delete 1
python solution/todo.py list
# Expected output:
# No tasks yet.
``` 