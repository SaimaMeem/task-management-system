import argparse
from task_manager import TaskManager
from storage import Storage

def handle_add(manager, title, description):
    if manager.add_task(title, description):
        print(f"Task '{title}' added successfully.")
    else:
        print(f"A task titled '{title}' already exists and is currently pending.")

def handle_update(manager, title, description):
    if manager.edit_task(title, description):
        print(f"Task '{title}' updated successfully.")
    else:
        print(f"Task '{title}' not found.")

def handle_complete(manager, title):
    if manager.complete_task(title):
        print(f"Task '{title}' marked as completed.")
    else:
        print(f"Task '{title}' not found.")

def handle_delete(manager, title):
    if manager.delete_task(title):
        print(f"Task '{title}' deleted successfully.")
    else:
        print(f"Task '{title}' not found.")

def handle_clear(manager):
    if manager.delete_all_tasks():
        print("The task list cleared successfully.")
    else:
        print("No tasks available.")

def handle_list(manager, include_completed, only_completed):
    tasks = manager.list_tasks(include_completed=include_completed, only_completed=only_completed)
    sorted_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
    if tasks:
        for task in sorted_tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"{task.title} - {status}")
    else:
        print("No tasks found.")

def handle_search(manager, title):
    result = manager.search_task(title)
    if result:
        task, formatted_task_creation_time = result
        print(f"""Title: {task.title} \nDescription: {task.description} \nCreated At: {formatted_task_creation_time}""")
    else:
        print(f"Task '{title}' not found.")

def handle_report(manager):
    print(manager.generate_report())

def main():
    storage = Storage()
    manager = TaskManager(storage)

    parser = argparse.ArgumentParser(description="Task Management System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("description", help="Task description")

    # Update task
    update_parser = subparsers.add_parser("update", help="Update description of a pending task")
    update_parser.add_argument("title", help="Task title")
    update_parser.add_argument("description", help="Task description")

    # Complete task
    complete_parser = subparsers.add_parser("complete", help="Mark a pending task as completed")
    complete_parser.add_argument("title", help="Task title")

    # Delete task
    delete_parser = subparsers.add_parser("delete", help="Delete a pending task")
    delete_parser.add_argument("title", help="Task title")

    # Clear task list
    subparsers.add_parser("clear", help="Clear task list")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List all pending tasks")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks")
    list_parser.add_argument("--completed", action="store_true", help="Show only completed tasks")

    # Search task and show details
    search_parser = subparsers.add_parser("search", help="Search a pending task and show details")
    search_parser.add_argument("title", help="Task title")

    # Generate report
    subparsers.add_parser("report", help="Generate a report")

    args = parser.parse_args()

    command_handlers = {
        "add": lambda: handle_add(manager, args.title, args.description),
        "update": lambda: handle_update(manager, args.title, args.description),
        "complete": lambda: handle_complete(manager, args.title),
        "delete": lambda: handle_delete(manager, args.title),
        "clear": lambda: handle_clear(manager),
        "list": lambda: handle_list(manager, args.all, args.completed),
        "search": lambda: handle_search(manager, args.title),
        "report": lambda: handle_report(manager)
    }

    if args.command in command_handlers:
        command_handlers[args.command]()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
