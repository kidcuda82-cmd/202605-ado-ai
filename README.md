# 202605-ado-ai

A simple Python command-line to-do list application.

This repository includes a CLI skeleton in `src/todo.py` that supports adding tasks and listing tasks using `argparse`, and stores tasks in JSON format in `tasks.json`.

## Usage

- `python src/todo.py add "Buy milk"`
- `python src/todo.py list`
- `python src/todo.py complete <task_number>`

## Files

- `src/todo.py`: Python CLI application entry point.
- `tasks.json`: JSON storage for tasks.
- `requirements.txt`: Notes dependencies; this app uses the Python standard library.
