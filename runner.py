# Before running this script, please read the README.md file for instructions and explanations.
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

CONFIRMATION_FILE = ".readme_confirmed"

def get_task_dir(task_name):
    """Get the directory for a given task."""
    task_dir = os.path.join("tasks", task_name)
    if not os.path.isdir(task_dir):
        print(f"Error: Task '{task_name}' not found at '{task_dir}'")
        sys.exit(1)
    return task_dir

def prepare_workspace(task_name):
    """Prepares the workspace for a task by cleaning and copying initial code."""
    task_dir = get_task_dir(task_name)
    initial_code_dir = os.path.join(task_dir, "initial_code")
    solution_dir = os.path.join(task_dir, "solution")

    if os.path.exists(initial_code_dir):
        if os.path.exists(solution_dir):
            shutil.rmtree(solution_dir)
        os.makedirs(solution_dir)
        
        for item in os.listdir(initial_code_dir):
            s = os.path.join(initial_code_dir, item)
            d = os.path.join(solution_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks=True)
            else:
                shutil.copy2(s, d)
        print(f"Workspace prepared: '{initial_code_dir}' copied to '{solution_dir}'.")

def display_prompt(task_name):
    """Displays the prompt for a given task."""
    task_dir = get_task_dir(task_name)
    prompt_path = os.path.join(task_dir, "prompt.md")
    if not os.path.exists(prompt_path):
        print(f"Error: prompt.md not found for task '{task_name}'")
        sys.exit(1)

    print("\n" + "="*80)
    print(f"PROMPT FOR: {task_name}")
    print("="*80 + "\n")
    with open(prompt_path, 'r') as f:
        print(f.read())
    print("\n" + "="*80)
    print("The agent should now perform the task based on the prompt above.")
    print("The agent's working directory should be the project root.")
    print("All generated files must be placed in the 'solution' directory for this task.")
    print("For more information on the benchmark, see the README.md file.")
    print("="*80 + "\n")

def run_verifier(task_name):
    """Runs the verifier for a task and returns the pytest output."""
    task_dir = get_task_dir(task_name)
    verifier_path = os.path.join(task_dir, "verifier")
    
    print("\nRunning verifier...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", verifier_path],
        capture_output=True,
        text=True
    )

    print("\n--- Pytest Output ---")
    print(result.stdout)
    if result.stderr:
        print("\n--- Pytest Errors ---")
        print(result.stderr)
    print("-----------------------\n")
    return result.stdout

def record_start_time(task_name):
    """Records the start time for a task."""
    task_dir = get_task_dir(task_name)
    start_time_path = os.path.join(task_dir, ".start_time")
    with open(start_time_path, 'w') as f:
        f.write(datetime.datetime.now(datetime.timezone.utc).isoformat())
    print(f"Start time for '{task_name}' recorded.")

def get_execution_time(task_name):
    """
    Calculates the execution time for a task by reading the start time 
    and deleting the start time file.
    """
    task_dir = get_task_dir(task_name)
    start_time_path = os.path.join(task_dir, ".start_time")
    execution_time = None
    if os.path.exists(start_time_path):
        with open(start_time_path, 'r') as f:
            start_time_str = f.read()
            start_time = datetime.datetime.fromisoformat(start_time_str)
            end_time = datetime.datetime.now(datetime.timezone.utc)
            execution_time = (end_time - start_time).total_seconds()
        os.remove(start_time_path)
    else:
        print("Warning: Start time not found. Could not calculate execution time.")
    return execution_time

def calculate_and_save_results(task_name, pytest_output, execution_time):
    """Calculates the scores and saves the results to a JSON file."""
    task_dir = get_task_dir(task_name)
    passed_tests, total_tests = 0, 0

    summary_match = re.search(r"(\d+)\s+passed", pytest_output)
    if summary_match:
        passed_tests = int(summary_match.group(1))

    failed_match = re.search(r"(\d+)\s+failed", pytest_output)
    errored_match = re.search(r"(\d+)\s+error", pytest_output)
    
    total_tests = passed_tests
    if failed_match:
        total_tests += int(failed_match.group(1))
    if errored_match:
        total_tests += int(errored_match.group(1))

    if total_tests == 0 and passed_tests == 0:
        if "no tests ran" not in pytest_output:
            print("Warning: Could not determine test results from pytest output. Assuming 0 tests passed.")
        correctness_score = 60 if "no tests ran" in pytest_output else 0
        task_completion_score = 0
    else:
        correctness_score = 60 * (passed_tests / total_tests)
        task_completion_score = 20 if passed_tests > 0 else 0

    results_data = {
        "task_name": task_name,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scores": {
            "correctness": round(correctness_score, 2),
            "task_completion": round(task_completion_score, 2),
        },
        "final_score_objective": round(correctness_score + task_completion_score, 2),
        "execution_time_seconds": execution_time,
        "pytest_output": pytest_output
    }

    results_path = os.path.join(task_dir, "results.json")
    with open(results_path, 'w') as f:
        json.dump(results_data, f, indent=4)

    print(f"Results for '{task_name}' saved to '{results_path}'")
    print(f"\n{'='*30} Finished Task: {task_name.upper()} {'='*30}\n")

def list_tasks():
    """Lists all available tasks."""
    tasks_dir = "tasks"
    if os.path.isdir(tasks_dir):
        tasks = [d for d in os.listdir(tasks_dir) if os.path.isdir(os.path.join(tasks_dir, d))]
        if tasks:
            print("Available tasks:")
            for task in tasks:
                print(f"- {task}")
        else:
            print("No tasks found in the 'tasks' directory.")
    else:
        print("'tasks' directory not found.")

def report_results():
    """Finds all results.json files and reports the scores in a markdown table."""
    tasks_dir = "tasks"
    all_results = []

    for task_name in sorted(os.listdir(tasks_dir)):
        task_dir = os.path.join(tasks_dir, task_name)
        if os.path.isdir(task_dir):
            results_path = os.path.join(task_dir, "results.json")
            if os.path.exists(results_path):
                try:
                    with open(results_path, 'r') as f:
                        data = json.load(f)
                        all_results.append(data)
                except (json.JSONDecodeError, KeyError):
                    print(f"Warning: Could not parse results.json for '{task_name}'")

    if not all_results:
        print("No results found. Run a task with 'evaluate' to generate results.")
        return

    # Sort results by task name for consistent output
    all_results.sort(key=lambda x: x.get("task_name", ""))

    # Print header
    print(f"| {'Task':<22} | {'Correct. (/60)':<15} | {'Complete (/20)':<15} | {'Score (/80)':<12} | {'Time (s)':<10} |")
    print(f"| {'-'*22} | {'-'*15} | {'-'*15} | {'-'*12} | {'-'*10} |")

    total_correctness = 0
    total_completion = 0
    total_score = 0
    total_time = 0

    for data in all_results:
        task_name = f"`{data.get('task_name', 'N/A')}`"
        correctness = data.get('scores', {}).get('correctness', 0)
        completion = data.get('scores', {}).get('task_completion', 0)
        score = data.get("final_score_objective", 0)
        time = data.get('execution_time_seconds', 0)

        total_correctness += correctness
        total_completion += completion
        total_score += score
        total_time += time

        print(f"| {task_name:<22} | {correctness:<15.2f} | {completion:<15.2f} | {score:<12.2f} | {time:<10.2f} |")

    # Print total
    print(f"| **{'Total':<22}** | **{total_correctness:<15.2f}** | **{total_completion:<15.2f}** | **{total_score:<12.2f}** | **{total_time:<10.2f}** |")

def main():
    """Main function to run and score benchmark tasks."""
    parser = argparse.ArgumentParser(
        description="Run and score benchmark tasks for a coding agent.",
        epilog="Please read the README.md for full instructions. You must run this script with '--confirm-i-have-viewed-entire-readme' once before you can use other commands."
    )
    parser.add_argument("--confirm-i-have-viewed-entire-readme", action="store_true", help="Confirm you have read the README.md.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'list' command
    subparsers.add_parser("list", help="List all available tasks.")

    # 'start' command
    start_parser = subparsers.add_parser("start", help="Start a task: prepare workspace and show prompt.")
    start_parser.add_argument("task", help="The name of the task to start.")

    # 'evaluate' command
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate the solution for a task.")
    evaluate_parser.add_argument("task", help="The name of the task to evaluate.")

    # 'report' command
    subparsers.add_parser("report", help="Report the results of all completed tasks.")

    args = parser.parse_args()

    # If --confirm-i-have-viewed-entire-readme is used, create the file.
    if args.confirm_i_have_viewed_entire_readme:
        with open(CONFIRMATION_FILE, "w") as f:
            f.write(datetime.datetime.now(datetime.timezone.utc).isoformat())
        print("README confirmation recorded. You can now use other commands.")
        # If ONLY --confirm-i-have-viewed-entire-readme was passed, exit.
        if not args.command:
            sys.exit(0)

    # For any command, require confirmation.
    if args.command and not os.path.exists(CONFIRMATION_FILE):
        print("Error: You must run --confirm-i-have-viewed-entire-readme once before using other commands.")
        print("Example: python runner.py --confirm-i-have-viewed-entire-readme")
        sys.exit(1)

    # What if no command is given?
    if not args.command:
        if not os.path.exists(CONFIRMATION_FILE):
            print("Welcome! To get started, please read the README.md file.")
            print("Then, run this command to confirm you have read it:")
            print("    python runner.py --confirm-i-have-viewed-entire-readme")
        else:
            # Already confirmed, show help.
            parser.print_help()
        sys.exit(0)

    if args.command == "list":
        list_tasks()
    elif args.command == "start":
        prepare_workspace(args.task)
        display_prompt(args.task)
        record_start_time(args.task)
    elif args.command == "evaluate":
        execution_time = get_execution_time(args.task)
        pytest_output = run_verifier(args.task)
        calculate_and_save_results(args.task, pytest_output, execution_time)
    elif args.command == "report":
        report_results()

if __name__ == "__main__":
    main() 