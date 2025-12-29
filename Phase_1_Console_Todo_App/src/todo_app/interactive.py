"""
Interactive menu-driven CLI for todo application.
"""
from todo_app.storage import TaskStore


# ANSI Color codes
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_menu():
    """Display main menu."""
    print("\n" + Colors.CYAN + "="*50 + Colors.END)
    print(Colors.BOLD + Colors.HEADER + "           TODO APPLICATION" + Colors.END)
    print(Colors.CYAN + "="*50 + Colors.END)
    print(f"\n{Colors.YELLOW}[1]{Colors.END} ➕ Add Task")
    print(f"{Colors.YELLOW}[2]{Colors.END} 📋 List Tasks")
    print(f"{Colors.YELLOW}[3]{Colors.END} ✅ Mark Complete")
    print(f"{Colors.YELLOW}[4]{Colors.END} ⭕ Mark Incomplete")
    print(f"{Colors.YELLOW}[5]{Colors.END} ✏️  Update Task")
    print(f"{Colors.YELLOW}[6]{Colors.END} 🗑️  Delete Task")
    print(f"{Colors.YELLOW}[7]{Colors.END} 🚪 Exit")
    print(Colors.CYAN + "-"*50 + Colors.END)


def add_task(store: TaskStore):
    """Add a new task."""
    title = input(f"\n{Colors.CYAN}Enter task title:{Colors.END} ").strip()
    if not title:
        print(f"{Colors.RED}❌ Error: Task title cannot be empty{Colors.END}")
        return

    description = input(f"{Colors.CYAN}Enter description (optional, press Enter to skip):{Colors.END} ").strip()
    description = description if description else None

    try:
        task_id = store.add_task(title, description)
        print(f"\n{Colors.GREEN}✓ Task added successfully!{Colors.END}")
        print(f"{Colors.BLUE}ID:{Colors.END} {task_id[:8]}")
        print(f"{Colors.BLUE}Title:{Colors.END} {title}")
        if description:
            print(f"{Colors.BLUE}Description:{Colors.END} {description}")
    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")


def list_tasks(store: TaskStore):
    """List all tasks."""
    tasks = store.list_tasks()

    if not tasks:
        print(f"\n{Colors.YELLOW}📭 No tasks found.{Colors.END}")
        return

    print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}Tasks ({len(tasks)}):{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}\n")

    for i, task in enumerate(tasks, 1):
        if task.completed:
            status = f"{Colors.GREEN}✓{Colors.END}"
            title = f"{Colors.GREEN}{task.title}{Colors.END}"
        else:
            status = f"{Colors.YELLOW}○{Colors.END}"
            title = task.title

        print(f"{Colors.BLUE}{i}.{Colors.END} [{status}] {Colors.CYAN}{task.id[:8]}...{Colors.END} {title}")
        if task.description:
            # Show truncated description
            desc = task.description[:40] + "..." if len(task.description) > 40 else task.description
            print(f"      └─ {Colors.CYAN}{desc}{Colors.END}")
    print()


def mark_complete(store: TaskStore):
    """Mark a task as complete."""
    task_id = input(f"\n{Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    try:
        task = store.mark_complete(task_id, True)
        print(f"\n{Colors.GREEN}✓ Task marked as complete{Colors.END}")
        print(f"{Colors.BLUE}ID:{Colors.END} {task.id[:8]}")
        print(f"{Colors.BLUE}Title:{Colors.END} {task.title}")
    except (KeyError, ValueError) as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")


def mark_incomplete(store: TaskStore):
    """Mark a task as incomplete."""
    task_id = input(f"\n{Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    try:
        task = store.mark_complete(task_id, False)
        print(f"\n{Colors.YELLOW}✓ Task marked as incomplete{Colors.END}")
        print(f"{Colors.BLUE}ID:{Colors.END} {task.id[:8]}")
        print(f"{Colors.BLUE}Title:{Colors.END} {task.title}")
    except (KeyError, ValueError) as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")


def update_task(store: TaskStore):
    """Update a task's title and/or description."""
    task_id = input(f"\n{Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    old_task = store.get_task(task_id)
    if old_task is None:
        print(f"{Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.END}")
        return

    # Save old values before updating
    old_title = old_task.title
    old_description = old_task.description

    print(f"\n{Colors.CYAN}Current Title:{Colors.END} {old_title}")
    if old_description:
        print(f"{Colors.CYAN}Current Description:{Colors.END} {old_description}")

    new_title = input(f"\n{Colors.CYAN}Enter new title (press Enter to keep current):{Colors.END} ").strip()
    new_title = new_title if new_title else None

    new_description = input(f"{Colors.CYAN}Enter new description (press Enter to keep, type 'clear' to remove):{Colors.END} ").strip()
    if new_description.lower() == 'clear':
        new_description = ""  # Empty string clears description
    elif not new_description:
        new_description = None  # None means don't update

    try:
        task = store.update_task(task_id, title=new_title, description=new_description)
        print(f"\n{Colors.GREEN}✓ Task updated successfully{Colors.END}")
        print(f"{Colors.BLUE}ID:{Colors.END} {task.id[:8]}")

        if new_title is not None:
            print(f"{Colors.BLUE}Old Title:{Colors.END} {old_title}")
            print(f"{Colors.BLUE}New Title:{Colors.END} {task.title}")
        else:
            print(f"{Colors.BLUE}Title:{Colors.END} {task.title}")

        if new_description is not None:
            if old_description:
                print(f"{Colors.BLUE}Old Description:{Colors.END} {old_description}")
            if task.description:
                print(f"{Colors.BLUE}New Description:{Colors.END} {task.description}")
            else:
                print(f"{Colors.BLUE}Description:{Colors.END} (cleared)")
    except (KeyError, ValueError) as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")


def delete_task(store: TaskStore):
    """Delete a task."""
    task_id = input(f"\n{Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    task = store.get_task(task_id)
    if task is None:
        print(f"{Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.END}")
        return

    title = task.title
    task_id_short = task.id[:8]

    try:
        store.delete_task(task_id)
        print(f"\n{Colors.GREEN}✓ Task deleted successfully{Colors.END}")
        print(f"{Colors.BLUE}ID:{Colors.END} {task_id_short}")
        print(f"{Colors.BLUE}Title:{Colors.END} {title}")
    except (KeyError, ValueError) as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")


def run_interactive():
    """Run interactive menu-driven CLI."""
    store = TaskStore()

    print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 Welcome to Todo Application!{Colors.END}")

    while True:
        print_menu()
        choice = input(f"{Colors.YELLOW}Select option (1-7):{Colors.END} ").strip()

        if choice == "1":
            add_task(store)
        elif choice == "2":
            list_tasks(store)
        elif choice == "3":
            mark_complete(store)
        elif choice == "4":
            mark_incomplete(store)
        elif choice == "5":
            update_task(store)
        elif choice == "6":
            delete_task(store)
        elif choice == "7":
            print(f"\n{Colors.BOLD}{Colors.GREEN}👋 Thank you for using Todo Application!{Colors.END}\n")
            break
        else:
            print(f"\n{Colors.RED}❌ Invalid choice. Please select 1-7.{Colors.END}")


if __name__ == "__main__":
    run_interactive()
