"""
Interactive menu-driven CLI for todo application.
"""
import os
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


# App box width (30% larger than original 50)
APP_WIDTH = 65


def get_terminal_width():
    """Get terminal width for centering."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 120  # Default width


def get_left_padding():
    """Calculate left padding to center the app box."""
    terminal_width = get_terminal_width()
    padding = (terminal_width - APP_WIDTH) // 2
    return " " * max(0, padding)


def cprint(text="", center_text_inside=False):
    """Print text inside centered app box."""
    pad = get_left_padding()
    if center_text_inside:
        # Center the text within the app box
        visible_text = text
        for code in [Colors.HEADER, Colors.BLUE, Colors.CYAN, Colors.GREEN,
                     Colors.YELLOW, Colors.RED, Colors.BOLD, Colors.UNDERLINE, Colors.END]:
            visible_text = visible_text.replace(code, '')
        inner_padding = (APP_WIDTH - len(visible_text)) // 2
        print(pad + " " * max(0, inner_padding) + text)
    else:
        # Left-align text within the app box
        print(pad + text)


def cinput(prompt):
    """Input with prompt inside centered app box."""
    pad = get_left_padding()
    return input(pad + prompt)


def print_header():
    """Print app header."""
    cprint()
    cprint(Colors.CYAN + "=" * APP_WIDTH + Colors.END)
    cprint(Colors.BOLD + Colors.HEADER + "TODO APPLICATION" + Colors.END, center_text_inside=True)
    cprint(Colors.CYAN + "=" * APP_WIDTH + Colors.END)


def print_menu():
    """Display main menu."""
    print_header()
    cprint()
    cprint(f"  {Colors.YELLOW}[1]{Colors.END} ➕ Add Task")
    cprint(f"  {Colors.YELLOW}[2]{Colors.END} 📋 List Tasks")
    cprint(f"  {Colors.YELLOW}[3]{Colors.END} ✅ Mark Complete")
    cprint(f"  {Colors.YELLOW}[4]{Colors.END} ⭕ Mark Incomplete")
    cprint(f"  {Colors.YELLOW}[5]{Colors.END} ✏️  Update Task")
    cprint(f"  {Colors.YELLOW}[6]{Colors.END} 🗑️  Delete Task")
    cprint(f"  {Colors.YELLOW}[7]{Colors.END} 🚪 Exit")
    cprint()
    cprint(Colors.CYAN + "-" * APP_WIDTH + Colors.END)


def add_task(store: TaskStore):
    """Add a new task."""
    cprint()
    title = cinput(f"  {Colors.CYAN}Enter task title:{Colors.END} ").strip()
    if not title:
        cprint(f"  {Colors.RED}❌ Error: Task title cannot be empty{Colors.END}")
        return

    description = cinput(f"  {Colors.CYAN}Enter description (optional, press Enter to skip):{Colors.END} ").strip()
    description = description if description else None

    try:
        task_id = store.add_task(title, description)
        cprint()
        cprint(f"  {Colors.GREEN}✓ Task added successfully!{Colors.END}")
        cprint(f"  {Colors.BLUE}ID:{Colors.END} {task_id[:8]}")
        cprint(f"  {Colors.BLUE}Title:{Colors.END} {title}")
        if description:
            cprint(f"  {Colors.BLUE}Description:{Colors.END} {description}")
    except ValueError as e:
        cprint(f"  {Colors.RED}❌ Error: {e}{Colors.END}")


def list_tasks(store: TaskStore):
    """List all tasks."""
    tasks = store.list_tasks()

    if not tasks:
        cprint()
        cprint(f"  {Colors.YELLOW}📭 No tasks found.{Colors.END}")
        return

    cprint()
    cprint(Colors.CYAN + "=" * APP_WIDTH + Colors.END)
    cprint(f"{Colors.BOLD}{Colors.HEADER}  Tasks ({len(tasks)}):{Colors.END}")
    cprint(Colors.CYAN + "=" * APP_WIDTH + Colors.END)
    cprint()

    for i, task in enumerate(tasks, 1):
        if task.completed:
            status = f"{Colors.GREEN}✓{Colors.END}"
            title = f"{Colors.GREEN}{task.title}{Colors.END}"
        else:
            status = f"{Colors.YELLOW}○{Colors.END}"
            title = task.title

        cprint(f"  {Colors.BLUE}{i}.{Colors.END} [{status}] {Colors.CYAN}{task.id[:8]}...{Colors.END} {title}")
        if task.description:
            # Show truncated description
            desc = task.description[:45] + "..." if len(task.description) > 45 else task.description
            cprint(f"       └─ {Colors.CYAN}{desc}{Colors.END}")
    cprint()


def mark_complete(store: TaskStore):
    """Mark a task as complete."""
    cprint()
    task_id = cinput(f"  {Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    try:
        task = store.mark_complete(task_id, True)
        cprint()
        cprint(f"  {Colors.GREEN}✓ Task marked as complete{Colors.END}")
        cprint(f"  {Colors.BLUE}ID:{Colors.END} {task.id[:8]}")
        cprint(f"  {Colors.BLUE}Title:{Colors.END} {task.title}")
    except (KeyError, ValueError) as e:
        cprint(f"  {Colors.RED}❌ Error: {e}{Colors.END}")


def mark_incomplete(store: TaskStore):
    """Mark a task as incomplete."""
    cprint()
    task_id = cinput(f"  {Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    try:
        task = store.mark_complete(task_id, False)
        cprint()
        cprint(f"  {Colors.YELLOW}✓ Task marked as incomplete{Colors.END}")
        cprint(f"  {Colors.BLUE}ID:{Colors.END} {task.id[:8]}")
        cprint(f"  {Colors.BLUE}Title:{Colors.END} {task.title}")
    except (KeyError, ValueError) as e:
        cprint(f"  {Colors.RED}❌ Error: {e}{Colors.END}")


def update_task(store: TaskStore):
    """Update a task's title and/or description."""
    cprint()
    task_id = cinput(f"  {Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    old_task = store.get_task(task_id)
    if old_task is None:
        cprint(f"  {Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.END}")
        return

    # Save old values before updating
    old_title = old_task.title
    old_description = old_task.description

    cprint()
    cprint(f"  {Colors.CYAN}Current Title:{Colors.END} {old_title}")
    if old_description:
        cprint(f"  {Colors.CYAN}Current Description:{Colors.END} {old_description}")

    cprint()
    new_title = cinput(f"  {Colors.CYAN}Enter new title (press Enter to keep current):{Colors.END} ").strip()
    new_title = new_title if new_title else None

    new_description = cinput(f"  {Colors.CYAN}Enter new description (Enter to keep, 'clear' to remove):{Colors.END} ").strip()
    if new_description.lower() == 'clear':
        new_description = ""  # Empty string clears description
    elif not new_description:
        new_description = None  # None means don't update

    try:
        task = store.update_task(task_id, title=new_title, description=new_description)
        cprint()
        cprint(f"  {Colors.GREEN}✓ Task updated successfully{Colors.END}")
        cprint(f"  {Colors.BLUE}ID:{Colors.END} {task.id[:8]}")

        if new_title is not None:
            cprint(f"  {Colors.BLUE}Old Title:{Colors.END} {old_title}")
            cprint(f"  {Colors.BLUE}New Title:{Colors.END} {task.title}")
        else:
            cprint(f"  {Colors.BLUE}Title:{Colors.END} {task.title}")

        if new_description is not None:
            if old_description:
                cprint(f"  {Colors.BLUE}Old Description:{Colors.END} {old_description}")
            if task.description:
                cprint(f"  {Colors.BLUE}New Description:{Colors.END} {task.description}")
            else:
                cprint(f"  {Colors.BLUE}Description:{Colors.END} (cleared)")
    except (KeyError, ValueError) as e:
        cprint(f"  {Colors.RED}❌ Error: {e}{Colors.END}")


def delete_task(store: TaskStore):
    """Delete a task."""
    cprint()
    task_id = cinput(f"  {Colors.CYAN}Enter task ID (min 8 chars):{Colors.END} ").strip()

    task = store.get_task(task_id)
    if task is None:
        cprint(f"  {Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.END}")
        return

    title = task.title
    task_id_short = task.id[:8]

    try:
        store.delete_task(task_id)
        cprint()
        cprint(f"  {Colors.GREEN}✓ Task deleted successfully{Colors.END}")
        cprint(f"  {Colors.BLUE}ID:{Colors.END} {task_id_short}")
        cprint(f"  {Colors.BLUE}Title:{Colors.END} {title}")
    except (KeyError, ValueError) as e:
        cprint(f"  {Colors.RED}❌ Error: {e}{Colors.END}")


def run_interactive():
    """Run interactive menu-driven CLI."""
    store = TaskStore()

    cprint()
    cprint(f"{Colors.BOLD}{Colors.GREEN}🎯 Welcome to Todo Application!{Colors.END}", center_text_inside=True)
    cprint(f"{Colors.BLUE}Build By CodeWithHamza{Colors.END}", center_text_inside=True)

    while True:
        print_menu()
        choice = cinput(f"  {Colors.YELLOW}Select option (1-7):{Colors.END} ").strip()

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
            cprint()
            cprint(f"{Colors.BOLD}{Colors.GREEN}👋 Thank you for using Todo Application!{Colors.END}", center_text_inside=True)
            cprint()
            break
        else:
            cprint()
            cprint(f"  {Colors.RED}❌ Invalid choice. Please select 1-7.{Colors.END}")


if __name__ == "__main__":
    run_interactive()
