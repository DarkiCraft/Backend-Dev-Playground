import json
import sys
from typing import TypedDict, Literal, List
from datetime import datetime

DB_FILE = "tasks.json"

STATUS_TODO     = "todo"
STATUS_PROGRESS = "in-progress"
STATUS_DONE     = "done"

class Task(TypedDict):
  id: str
  description: str
  status: Literal["todo", "in-progress", "done"]
  createdAt: str
  updatedAt: str

# ---------- I/O ----------
def load_tasks() -> List[Task]:
  try:
    with open(DB_FILE, "r") as file:
      return [Task(**item) for item in json.load(file)]
  except FileNotFoundError:
    return []
  except json.JSONDecodeError:
    print("JSON corrupted. Starting fresh.")
    return []

def save_tasks(tasks: List[Task]) -> None:
  with open(DB_FILE, "w") as file:
    json.dump(tasks, file, indent=2)

# ---------- Commands ----------
def add_task(tasks: List[Task], desc: str):
  new_task: Task = {
    "id": str(max(int(task["id"]) for task in tasks) + 1 if tasks else 1),
    "description": desc,
    "status": STATUS_TODO,
    "createdAt": datetime.now().isoformat(),
    "updatedAt": datetime.now().isoformat()
  }
  tasks.append(new_task)
  save_tasks(tasks)
  print(f"Task added: {desc}")

def update_description(tasks: List[Task], task_id: str, new_desc: str):
  for task in tasks:
    if task["id"] == task_id:
      task["description"] = new_desc
      task["updatedAt"] = datetime.now().isoformat()
      save_tasks(tasks)
      print("Description updated.")
      return
  print("Task not found.")

def delete_task(tasks: List[Task], task_id: str):
  new_tasks = [task for task in tasks if task["id"] != task_id]
  if len(new_tasks) == len(tasks):
    print("Task not found.")
  else:
    save_tasks(new_tasks)
    print("Task deleted.")

def change_status(tasks: List[Task], task_id: str, status: Literal["in-progress", "done"]):
  for task in tasks:
    if task["id"] == task_id:
      task["status"] = status
      task["updatedAt"] = datetime.now().isoformat()
      save_tasks(tasks)
      print(f"Marked as {status}")
      return
  print("Task not found.")

def show_help():
  print("Available commands:")
  print("  add <description>         - Add a new task")
  print("  update <id> <desc>        - Update description of a task")
  print("  delete <id>               - Delete a task")
  print("  mark-in-progress <id>     - Mark task as in-progress")
  print("  mark-done <id>            - Mark task as done")
  print("  help                      - Show this message")

# ---------- Main ----------
def main():
  if len(sys.argv) < 2:
    show_help()
    return

  tasks = load_tasks()

  cmd = sys.argv[1]

  if cmd == "add" and len(sys.argv) == 3:
    add_task(tasks, sys.argv[2])
  elif cmd == "update" and len(sys.argv) == 4:
    update_description(tasks, sys.argv[2], sys.argv[3])
  elif cmd == "delete" and len(sys.argv) == 3:
    delete_task(tasks, sys.argv[2])
  elif cmd == "mark-in-progress" and len(sys.argv) == 3:
    change_status(tasks, sys.argv[2], STATUS_PROGRESS)
  elif cmd == "mark-done" and len(sys.argv) == 3:
    change_status(tasks, sys.argv[2], STATUS_DONE)
  elif cmd == "help":
    show_help()
  else:
    print("Invalid command or arguments.")
    show_help()

if __name__ == "__main__":
  main()