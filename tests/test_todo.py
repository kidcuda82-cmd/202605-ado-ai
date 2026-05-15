import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import todo


def test_add_task_creates_task_file_and_prints(tmp_path, capsys):
    task_file = tmp_path / "tasks.json"
    todo.TASKS_FILE = task_file

    todo.add_task("Buy milk")

    captured = capsys.readouterr()
    assert "Added task: Buy milk" in captured.out

    assert task_file.exists()
    with task_file.open("r", encoding="utf-8") as file:
        tasks = json.load(file)

    assert tasks == [{"description": "Buy milk", "completed": False}]


def test_list_tasks_prints_all_tasks(tmp_path, capsys):
    task_file = tmp_path / "tasks.json"
    todo.TASKS_FILE = task_file

    tasks = [
        {"description": "Write tests", "completed": False},
        {"description": "Review PR", "completed": True},
    ]
    task_file.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

    todo.list_tasks()

    captured = capsys.readouterr()
    assert "1. [ ] Write tests" in captured.out
    assert "2. [x] Review PR" in captured.out


def test_complete_task_marks_task_complete_and_saves(tmp_path, capsys):
    task_file = tmp_path / "tasks.json"
    todo.TASKS_FILE = task_file

    tasks = [{"description": "Learn pytest", "completed": False}]
    task_file.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

    todo.complete_task(1)

    captured = capsys.readouterr()
    assert "Marked task 1 complete." in captured.out

    with task_file.open("r", encoding="utf-8") as file:
        saved_tasks = json.load(file)

    assert saved_tasks[0]["completed"] is True


def test_complete_task_invalid_id_reports_error(tmp_path, capsys):
    task_file = tmp_path / "tasks.json"
    todo.TASKS_FILE = task_file

    tasks = [{"description": "Sample task", "completed": False}]
    task_file.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

    todo.complete_task(2)

    captured = capsys.readouterr()
    assert "Task 2 does not exist." in captured.out

    with task_file.open("r", encoding="utf-8") as file:
        saved_tasks = json.load(file)

    assert saved_tasks == tasks
