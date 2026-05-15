import argparse
import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "completed": False})
    save_tasks(tasks)
    print(f"Added task: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task.get("completed") else "[ ]"
        print(f"{index}. {status} {task.get('description')}")


def complete_task(task_id):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    if task_id < 1 or task_id > len(tasks):
        print(f"Task {task_id} does not exist.")
        return

    task = tasks[task_id - 1]

    if task.get("completed"):
        print(f"Task {task_id} is already complete.")
        return

    task["completed"] = True
    save_tasks(tasks)
    print(f"Marked task {task_id} complete.")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Simple todo list CLI app using JSON storage."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    complete_parser = subparsers.add_parser("complete", help="Mark a task complete")
    complete_parser.add_argument("task_id", type=int, help="Task number to mark complete")

    subparsers.add_parser("list", help="List all tasks")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.task_id)


if __name__ == "__main__":
    main()
