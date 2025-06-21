import subprocess
import json
from pathlib import Path
import pytest
import os

# Path to the solution script
SOLUTION_PATH = Path(__file__).parent.parent / "solution" / "todo.py"
TASKS_FILE = Path(__file__).parent.parent / "solution" / "tasks.json"

@pytest.fixture(autouse=True)
def cleanup_tasks_file():
    """Fixture to ensure the tasks.json file is clean before each test."""
    if TASKS_FILE.exists():
        TASKS_FILE.unlink()
    yield
    if TASKS_FILE.exists():
        TASKS_FILE.unlink()

def run_command(command):
    """Helper function to run a command and return the output."""
    project_root = Path(__file__).parent.parent.parent.parent
    # We need to run from the root of the project
    process = subprocess.run(
        ["python", str(SOLUTION_PATH)] + command,
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    return process.stdout.strip(), process.stderr.strip()

def read_tasks():
    """Helper function to read tasks from the JSON file."""
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def test_add_task():
    """Test adding a single task."""
    task = "Buy milk"
    run_command(["add", task])
    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0]["task"] == task
    assert not tasks[0]["completed"]

def test_add_multiple_tasks():
    """Test adding multiple tasks."""
    run_command(["add", "Task 1"])
    run_command(["add", "Task 2"])
    tasks = read_tasks()
    assert len(tasks) == 2
    assert tasks[0]["task"] == "Task 1"
    assert tasks[1]["task"] == "Task 2"

def test_list_tasks_empty():
    """Test listing tasks when the list is empty."""
    output, _ = run_command(["list"])
    assert output == "No tasks yet."

def test_list_tasks():
    """Test listing multiple tasks with different statuses."""
    run_command(["add", "Task 1"])
    run_command(["add", "Task 2"])
    
    # Manually mark one as completed to test listing
    tasks = read_tasks()
    tasks[0]["completed"] = True
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

    output, _ = run_command(["list"])
    expected_lines = [
        "1. [x] - Task 1",
        "2. [ ] - Task 2",
    ]
    assert output == "\n".join(expected_lines)

def test_complete_task():
    """Test marking a task as complete."""
    run_command(["add", "Task 1"])
    run_command(["complete", "1"])
    tasks = read_tasks()
    assert tasks[0]["completed"]

def test_complete_task_invalid_index():
    """Test completing a task with an invalid index."""
    run_command(["add", "Task 1"])
    output, _ = run_command(["complete", "2"])
    assert "Invalid index" in output
    tasks = read_tasks()
    assert not tasks[0]["completed"]

def test_delete_task():
    """Test deleting a task."""
    run_command(["add", "Task 1"])
    run_command(["add", "Task 2"])
    run_command(["delete", "1"])
    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0]['task'] == 'Task 2'

def test_delete_task_invalid_index():
    """Test deleting a task with an invalid index."""
    run_command(["add", "Task 1"])
    output, _ = run_command(["delete", "2"])
    assert "Invalid index" in output
    tasks = read_tasks()
    assert len(tasks) == 1

def test_persistence():
    """Test that tasks are persisted between runs."""
    run_command(["add", "Persistent Task"])
    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0]['task'] == "Persistent Task"

    # Run another command and check if the task is still there
    output, _ = run_command(["list"])
    assert "1. [ ] - Persistent Task" in output 