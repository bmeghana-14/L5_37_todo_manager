"""A simple task manager with JSON persistence and task suggestions."""

import json
import secrets
import smtplib
from datetime import datetime
from email.message import EmailMessage
from email.utils import parseaddr
from pathlib import Path
from typing import Any


TASKS: dict[int, dict[str, Any]] = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(
    title: str,
    priority: str = "medium",
    labels: list[str] | None = None,
) -> int:
    """Add a task and return its ID."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    if priority not in PRIORITY_ORDER:
        raise ValueError("Priority must be high, medium, or low.")

    task_id = max(TASKS, default=0) + 1
    task_labels = list(labels) if labels is not None else []
    if priority not in task_labels:
        task_labels.append(priority)

    TASKS[task_id] = {
        "title": title,
        "priority": priority,
        "labels": task_labels,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    return task_id


def complete_task(task_id: int) -> bool:
    """Mark a task as complete, returning whether it exists."""
    if task_id not in TASKS:
        print(f"No task with id {task_id}")
        return False

    TASKS[task_id]["done"] = True
    return True


def pending_tasks() -> list[str]:
    """Return pending task titles ordered by priority."""
    pending = [
        task for task in TASKS.values() if not task["done"]
    ]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword: str) -> int | None:
    """Find the first task whose title contains the keyword."""
    keyword = keyword.strip().casefold()
    for task_id, task in TASKS.items():
        if keyword in task["title"].casefold():
            return task_id
    return None


def save_tasks(file_name: str = "tasks.json") -> None:
    """Save tasks as JSON."""
    with Path(file_name).open("w", encoding="utf-8") as file:
        json.dump(TASKS, file, indent=2)


def load_tasks(file_name: str = "tasks.json") -> dict[int, dict[str, Any]]:
    """Load tasks from JSON without deserializing executable objects."""
    with Path(file_name).open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Task data must be a JSON object.")

    restored: dict[int, dict[str, Any]] = {}
    for key, task in data.items():
        if not key.isdigit() or not isinstance(task, dict):
            raise ValueError("Invalid task record.")
        if not isinstance(task.get("title"), str):
            raise ValueError("Each task must have a string title.")
        if task.get("priority") not in PRIORITY_ORDER:
            raise ValueError("Each task must have a valid priority.")
        if not isinstance(task.get("done"), bool):
            raise ValueError("Each task must have a boolean done field.")
        restored[int(key)] = task

    return restored


def export_json(file_name: str = "tasks.json") -> None:
    """Export the current tasks to a JSON file."""
    save_tasks(file_name)


def remind_by_email(address: str) -> None:
    """Send pending-task reminders through a local SMTP server."""

    if parseaddr(address)[1] != address or "@" not in address:
        raise ValueError("Enter a valid email address.")

    message = EmailMessage()
    message["Subject"] = "Pending tasks"
    message["From"] = "todo-manager@localhost"
    message["To"] = address
    message.set_content("\n".join(pending_tasks()) or "No pending tasks.")

    with smtplib.SMTP("localhost") as server:
        server.send_message(message)


def main() -> None:
    """Run a demonstration of the task manager."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)

    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))

    pending = pending_tasks()
    if pending:
        suggestion = secrets.choice(pending)
        print("Try this next:", suggestion)
    else:
        print("No pending tasks to suggest.")

    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))
    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
