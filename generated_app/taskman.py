#!/usr/bin/env python3
"""
taskman.py - Simple single-file CLI task manager using sqlite3.

Usage:
    taskman.py add "Title" [-n "Notes"]
    taskman.py list [--all | --done | --pending] [-v]
    taskman.py done ID [ID ...]
    taskman.py undone ID [ID ...]
    taskman.py edit ID [-t "New Title"] [-n "New Notes"]
    taskman.py delete ID [ID ...]
    taskman.py clear [--completed]
    taskman.py export FILE [-f json|csv] [--all | --done | --pending]

The database is stored in tasks.db in the current working directory.
"""

from __future__ import print_function
import argparse
import sqlite3
import sys
import os
import json
import csv
from datetime import datetime

DB_FILENAME = "tasks.db"

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT
);
"""

def get_conn():
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    with conn:
        conn.execute(SQL_CREATE)
    conn.close()

def add_task(title, notes=None):
    now = datetime.utcnow().isoformat() + "Z"
    conn = get_conn()
    with conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, notes, created_at, completed) VALUES (?, ?, ?, 0)",
            (title, notes, now)
        )
        task_id = cur.lastrowid
    conn.close()
    print("Added task", task_id)

def list_tasks(show_all=False, show_done=False, show_pending=False, verbose=False):
    conn = get_conn()
    q = "SELECT id, title, notes, created_at, completed, completed_at FROM tasks"
    params = ()
    if show_all:
        q += " ORDER BY completed, created_at"
    elif show_done:
        q += " WHERE completed = 1 ORDER BY completed_at DESC"
    elif show_pending:
        q += " WHERE completed = 0 ORDER BY created_at"
    else:
        # default: pending first then completed
        q += " ORDER BY completed, created_at"
    cur = conn.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("No tasks found.")
        return
    if verbose:
        for r in rows:
            print("ID:     ", r["id"])
            print("Title:  ", r["title"])
            print("Notes:  ", r["notes"] or "")
            print("Created:", r["created_at"])
            print("Done:   ", "Yes" if r["completed"] else "No")
            if r["completed_at"]:
                print("Done at:", r["completed_at"])
            print("-" * 40)
    else:
        # print compact table
        idw = 4
        titlew = 40
        statusw = 6
        createdw = 20
        header = "{:<{idw}}  {:<{titlew}}  {:<{statusw}}  {:<{createdw}}".format(
            "ID", "Title", "State", "Created", idw=idw, titlew=titlew, statusw=statusw, createdw=createdw
        )
        print(header)
        print("-" * len(header))
        for r in rows:
            tid = str(r["id"])
            title = (r["title"][:titlew-3] + "...") if len(r["title"]) > titlew else r["title"]
            state = "Done" if r["completed"] else "Todo"
            created = r["created_at"][:createdw]
            print("{:<{idw}}  {:<{titlew}}  {:<{statusw}}  {:<{createdw}}".format(
                tid, title, state, created, idw=idw, titlew=titlew, statusw=statusw, createdw=createdw
            ))

def _parse_ids(id_list):
    ids = []
    for token in id_list:
        # allow comma separated inside tokens
        parts = token.split(",")
        for p in parts:
            p = p.strip()
            if not p:
                continue
            try:
                ids.append(int(p))
            except ValueError:
                print("Invalid id:", p, file=sys.stderr)
                sys.exit(2)
    if not ids:
        print("No ids provided.", file=sys.stderr)
        sys.exit(2)
    return ids

def mark_done(ids):
    now = datetime.utcnow().isoformat() + "Z"
    conn = get_conn()
    with conn:
        for tid in ids:
            conn.execute(
                "UPDATE tasks SET completed = 1, completed_at = ? WHERE id = ?",
                (now, tid)
            )
    conn.close()
    print("Marked done:", " ".join(str(i) for i in ids))

def mark_undone(ids):
    conn = get_conn()
    with conn:
        for tid in ids:
            conn.execute(
                "UPDATE tasks SET completed = 0, completed_at = NULL WHERE id = ?",
                (tid,)
            )
    conn.close()
    print("Marked undone:", " ".join(str(i) for i in ids))

def edit_task(tid, title=None, notes=None):
    conn = get_conn()
    with conn:
        cur = conn.execute("SELECT id FROM tasks WHERE id = ?", (tid,))
        row = cur.fetchone()
        if not row:
            print("Task not found:", tid, file=sys.stderr)
            conn.close()
            sys.exit(2)
        if title is not None and notes is not None:
            conn.execute("UPDATE tasks SET title = ?, notes = ? WHERE id = ?", (title, notes, tid))
        elif title is not None:
            conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, tid))
        elif notes is not None:
            conn.execute("UPDATE tasks SET notes = ? WHERE id = ?", (notes, tid))
        else:
            print("Nothing to update.", file=sys.stderr)
            conn.close()
            sys.exit(2)
    conn.close()
    print("Updated task", tid)

def delete_tasks(ids):
    conn = get_conn()
    with conn:
        for tid in ids:
            conn.execute("DELETE FROM tasks WHERE id = ?", (tid,))
    conn.close()
    print("Deleted:", " ".join(str(i) for i in ids))

def clear_tasks(completed_only=False):
    if completed_only:
        prompt = "Delete all completed tasks? (y/N): "
    else:
        prompt = "Delete ALL tasks? This cannot be undone. (y/N): "
    ans = input(prompt).strip().lower()
    if ans != "y":
        print("Aborted.")
        return
    conn = get_conn()
    with conn:
        if completed_only:
            conn.execute("DELETE FROM tasks WHERE completed = 1")
            print("Deleted completed tasks.")
        else:
            conn.execute("DELETE FROM tasks")
            print("Deleted all tasks.")
    conn.close()

def export_tasks(path, fmt="json", show_all=False, show_done=False, show_pending=False):
    conn = get_conn()
    q = "SELECT id, title, notes, created_at, completed, completed_at FROM tasks"
    if show_done:
        q += " WHERE completed = 1"
    elif show_pending:
        q += " WHERE completed = 0"
    q += " ORDER BY created_at"
    cur = conn.execute(q)
    rows = cur.fetchall()
    conn.close()
    data = []
    for r in rows:
        data.append({
            "id": r["id"],
            "title": r["title"],
            "notes": r["notes"],
            "created_at": r["created_at"],
            "completed": bool(r["completed"]),
            "completed_at": r["completed_at"]
        })
    if fmt == "json":
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=True)
            print("Exported", len(data), "tasks to", path)
        except Exception as e:
            print("Error exporting to json:", e, file=sys.stderr)
            sys.exit(1)
    elif fmt == "csv":
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "title", "notes", "created_at", "completed", "completed_at"])
                for item in data:
                    writer.writerow([item["id"], item["title"], item["notes"], item["created_at"], int(item["completed"]), item["completed_at"]])
            print("Exported", len(data), "tasks to", path)
        except Exception as e:
            print("Error exporting to csv:", e, file=sys.stderr)
            sys.exit(1)
    else:
        print("Unsupported format:", fmt, file=sys.stderr)
        sys.exit(2)

def parse_args(argv):
    parser = argparse.ArgumentParser(prog="taskman", description="Simple task manager using sqlite3")
    sub = parser.add_subparsers(dest="cmd")

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("-n", "--notes", help="Task notes", default=None)

    # list
    p_list = sub.add_parser("list", help="List tasks")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Show all tasks")
    group.add_argument("--done", action="store_true", help="Show only completed tasks")
    group.add_argument("--pending", action="store_true", help="Show only pending tasks")
    p_list.add_argument("-v", "--verbose", action="store_true", help="Verbose output with notes")

    # done
    p_done = sub.add_parser("done", help="Mark tasks as done")
    p_done.add_argument("ids", nargs="+", help="Task id or ids (comma or space separated)")

    # undone
    p_undone = sub.add_parser("undone", help="Mark tasks as not done")
    p_undone.add_argument("ids", nargs="+", help="Task id or ids (comma or space separated)")

    # edit
    p_edit = sub.add_parser("edit", help="Edit a task")
    p_edit.add_argument("id", type=int, help="Task id")
    p_edit.add_argument("-t", "--title", help="New title", default=None)
    p_edit.add_argument("-n", "--notes", help="New notes", default=None)

    # delete
    p_delete = sub.add_parser("delete", help="Delete tasks")
    p_delete.add_argument("ids", nargs="+", help="Task id or ids (comma or space separated)")

    # clear
    p_clear = sub.add_parser("clear", help="Clear tasks")
    p_clear.add_argument("--completed", action="store_true", help="Clear only completed tasks")

    # export
    p_export = sub.add_parser("export", help="Export tasks to a file")
    p_export.add_argument("file", help="Destination file path")
    p_export.add_argument("-f", "--format", choices=["json", "csv"], default="json", help="Export format")
    group2 = p_export.add_mutually_exclusive_group()
    group2.add_argument("--all", action="store_true", help="Export all tasks")
    group2.add_argument("--done", action="store_true", help="Export only completed tasks")
    group2.add_argument("--pending", action="store_true", help="Export only pending tasks")

    return parser.parse_args(argv)

def main(argv):
    init_db()
    args = parse_args(argv)
    if not args.cmd:
        print(__doc__)
        return
    try:
        if args.cmd == "add":
            add_task(args.title, args.notes)
        elif args.cmd == "list":
            list_tasks(show_all=args.all, show_done=args.done, show_pending=args.pending, verbose=args.verbose)
        elif args.cmd == "done":
            ids = _parse_ids(args.ids)
            mark_done(ids)
        elif args.cmd == "undone":
            ids = _parse_ids(args.ids)
            mark_undone(ids)
        elif args.cmd == "edit":
            edit_task(args.id, title=args.title, notes=args.notes)
        elif args.cmd == "delete":
            ids = _parse_ids(args.ids)
            delete_tasks(ids)
        elif args.cmd == "clear":
            clear_tasks(completed_only=args.completed)
        elif args.cmd == "export":
            export_tasks(args.file, fmt=args.format, show_all=args.all, show_done=args.done, show_pending=args.pending)
        else:
            print("Unknown command:", args.cmd, file=sys.stderr)
            sys.exit(2)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])