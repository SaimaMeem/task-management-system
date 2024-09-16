import argparse
from task_manager import TaskManager
from storage import Storage


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

    # List tasks
    list_parser = subparsers.add_parser("list", help="List all pending tasks")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks")

    # Generate report
    subparsers.add_parser("report", help="Generate a report")

    args = parser.parse_args()

    if args.command == "add":
        task = manager.add_task(args.title, args.description)
        if task:
            print(f"Task '{task.title}' added successfully.")
        else:
            print(f"A task titled '{args.title}' already exists and is currently pending.")
    elif args.command == "update":
        if manager.edit_task(args.title, args.description):
            print(f"Task '{args.title}' updated successfully.")
        else:
            print(f"Task '{args.title}' not found.")
    elif args.command == "complete":
        if manager.complete_task(args.title):
            print(f"Task '{args.title}' marked as completed.")
        else:
            print(f"Task '{args.title}' not found.")
    elif args.command == "delete":
        if manager.delete_task(args.title):
            print(f"Task '{args.title}' deleted successfully.")
        else:
            print(f"Task '{args.title}' not found.")
    elif args.command == "list":
        tasks = manager.list_tasks(include_completed=args.all)
        if tasks:
            for task in tasks:
                status = "Completed" if task.completed else "Pending"
                print(f"{task.title} - {status}")
        else:
            print("No tasks found.")
    elif args.command == "report":
        print(manager.generate_report())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
