#!/usr/bin/env python3
"""
Create a README.md file describing a minimal CLI Task Manager and how to run and use it.

This script writes a README.md file to the current directory.
"""

README = """# Minimal CLI Task Manager

A minimal command line task manager that lets you add, list, mark done, edit, and remove tasks.
This README describes the basic features and provides examples of how to run and use the tool.

Requirements
- Python 3.7 or newer

Installing
1. Clone or copy the project files to a directory.
2. Ensure the main script (for example, taskmgr.py) is executable or invoke it with Python:
   python taskmgr.py <command> [options]

Basic concepts
- Tasks are simple text items with optional metadata such as status, due date, and priority.
- Tasks are stored in a local data file (for example, tasks.json) in the project directory or in the user's home directory.
- The CLI supports basic commands: add, list, done, remove, edit, clear, export, import, and help.

Common commands and examples

1) Add a new task
- Add a simple task:
  python taskmgr.py add "Buy milk"

- Add with a due date and priority (if supported):
  python taskmgr.py add "Finish report" --due 2026-04-20 --priority high

2) List tasks
- List all tasks:
  python taskmgr.py list

- Show only pending tasks:
  python taskmgr.py list --pending

- Show only completed tasks:
  python taskmgr.py list --completed

3) Mark a task as done
- Mark task with id 3 as completed:
  python taskmgr.py done 3

4) Edit a task
- Edit the text of task with id 4:
  python taskmgr.py edit 4 "Finish the quarterly report"

- Edit fields like due date or priority (if supported):
  python taskmgr.py edit 4 --due 2026-04-22 --priority medium

5) Remove a task
- Remove task with id 2:
  python taskmgr.py remove 2

- Remove multiple tasks by id (if supported):
  python taskmgr.py remove 2 5 7

6) Clear tasks
- Remove all completed tasks:
  python taskmgr.py clear --completed

- Remove all tasks (use with caution):
  python taskmgr.py clear --all

7) Import and export
- Export tasks to a JSON file:
  python taskmgr.py export tasks.json

- Import tasks from a JSON file:
  python taskmgr.py import tasks.json

8) Search tasks
- Search tasks containing a phrase:
  python taskmgr.py search "milk"

9) Help
- Show help and available commands:
  python taskmgr.py help
  python taskmgr.py --help

Example session
1) Add tasks:
   $ python taskmgr.py add "Buy milk"
   Added task 1: Buy milk

   $ python taskmgr.py add "Call Alice about the meeting"
   Added task 2: Call Alice about the meeting

2) List tasks:
   $ python taskmgr.py list
   ID  Status  Task
   1   [ ]     Buy milk
   2   [ ]     Call Alice about the meeting

3) Mark a task done:
   $ python taskmgr.py done 1
   Task 1 marked as completed.

4) List pending tasks:
   $ python taskmgr.py list --pending
   ID  Status  Task
   2   [ ]     Call Alice about the meeting

Data storage
- The tool stores tasks in a small local file (for example tasks.json). Check the project configuration or source code to determine the exact location.
- Back up the data file before using import or clear commands.

Extending and customizing
- This minimal manager is intentionally simple. You can extend it by adding:
  - Tags or categories for tasks
  - Recurring tasks
  - Reminders and notifications
  - Integration with calendars or external services
  - A more advanced filtering and sorting system

Contributing
- Contributions are welcome. Open an issue or submit a pull request with improvements or bug fixes.

License
- This project is distributed under a permissive license. Check the LICENSE file for details.
"""

def write_readme(path="README.md", content=README):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    write_readme()
    print("README.md written.")

if __name__ == "__main__":
    main()