"""
Interactive menu-driven CLI for todo application.
Professional UI using Rich library.
Built by CodeWithHamza
"""
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from todo_app.storage import TaskStore


# Initialize Rich console
console = Console()


def format_date(iso_string: str) -> str:
    """Format ISO datetime to readable format."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return iso_string[:16]


def print_header():
    """Print application header."""
    console.print()
    console.print("=" * 60, style="bold magenta")
    console.print()

    title = Text()
    title.append("       ✨ ", style="yellow")
    title.append("TODO APPLICATION", style="bold magenta")
    title.append(" ✨", style="yellow")
    console.print(title)

    console.print()
    console.print("=" * 60, style="bold magenta")

    # Branding
    console.print()
    branding = Text()
    branding.append("       Built with ❤️  by ", style="dim")
    branding.append("CodeWithHamza", style="bold cyan")
    console.print(branding)
    console.print()


def print_menu():
    """Display main menu."""
    console.print()
    console.print("─" * 60, style="dim")
    console.print()

    menu_items = [
        ("[1]", "➕", "Add Task", "green"),
        ("[2]", "📋", "List Tasks", "blue"),
        ("[3]", "✅", "Mark Complete", "green"),
        ("[4]", "⭕", "Mark Incomplete", "yellow"),
        ("[5]", "🖋️ ", "Update Task", "cyan"),
        ("[6]", "🗑️ ", "Delete Task", "red"),
        ("[7]", "🚪", "Exit", "dim"),
    ]

    for key, icon, label, color in menu_items:
        line = Text()
        line.append(f"    {key}  ", style=f"bold {color}")
        line.append(f"{icon}  ", style="")
        line.append(label, style="bold white")
        console.print(line)

    console.print()
    console.print("─" * 60, style="dim")
    console.print()


def print_tasks(tasks: list):
    """Print tasks in a professional table format."""
    if not tasks:
        console.print()
        console.print("    📭 No tasks found. Add your first task!", style="yellow italic")
        console.print()
        return

    # Create table
    table = Table(
        show_header=True,
        header_style="bold white",
        box=box.SIMPLE_HEAD,
        padding=(0, 1),
        expand=False,
    )

    table.add_column("#", style="cyan", width=4)
    table.add_column("Status", width=12)
    table.add_column("Title", style="white", width=30)
    table.add_column("Description", style="dim", width=25)
    table.add_column("Created", style="dim", width=20)
    table.add_column("ID", style="cyan dim", width=10)

    for i, task in enumerate(tasks, 1):
        # Status
        if task.completed:
            status = Text("✓ Done", style="green")
        else:
            status = Text("○ Pending", style="yellow")

        # Title (truncate if needed)
        title = task.title[:28] + ".." if len(task.title) > 30 else task.title
        title_style = "dim" if task.completed else "bold white"

        # Description
        desc = ""
        if task.description:
            desc = task.description[:23] + ".." if len(task.description) > 25 else task.description

        # Date
        date = format_date(task.created_at)

        # ID
        task_id = task.id[:8]

        table.add_row(
            str(i),
            status,
            Text(title, style=title_style),
            desc,
            date,
            task_id
        )

    console.print()
    console.print(table)
    console.print()

    # Stats
    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed

    stats = Text()
    stats.append("    📊 ", style="")
    stats.append(f"✓ {completed} done", style="green")
    stats.append("  •  ", style="dim")
    stats.append(f"○ {pending} pending", style="yellow")
    stats.append("  •  ", style="dim")
    stats.append(f"Total: {len(tasks)}", style="cyan")
    console.print(stats)
    console.print()


def print_task_details(task, title: str = "Task Details"):
    """Print single task details."""
    console.print()
    console.print(f"    {title}", style="bold")
    console.print("    " + "─" * 40, style="dim")

    console.print(f"    [cyan]ID:[/cyan]          {task.id[:8]}")
    console.print(f"    [cyan]Title:[/cyan]       {task.title}")

    if task.description:
        console.print(f"    [cyan]Description:[/cyan] {task.description}")

    status = "[green]✓ Completed[/green]" if task.completed else "[yellow]○ Pending[/yellow]"
    console.print(f"    [cyan]Status:[/cyan]      {status}")
    console.print(f"    [cyan]Created:[/cyan]     {format_date(task.created_at)}")
    console.print()


def add_task(store: TaskStore):
    """Add a new task."""
    console.print()
    console.print("    [bold green]➕ ADD NEW TASK[/bold green]")
    console.print("    " + "─" * 30, style="dim")
    console.print()

    title = Prompt.ask("    [cyan]Title[/cyan]")
    if not title.strip():
        console.print("    [red]✗ Title cannot be empty[/red]")
        return

    desc = Prompt.ask("    [cyan]Description[/cyan] [dim](optional)[/dim]", default="")
    desc = desc.strip() if desc.strip() else None

    try:
        task_id = store.add_task(title.strip(), desc)
        task = store.get_task(task_id)

        console.print()
        console.print("    [green]✓ Task added successfully![/green]")
        print_task_details(task)
    except ValueError as e:
        console.print(f"    [red]✗ Error: {e}[/red]")


def list_tasks(store: TaskStore):
    """List all tasks."""
    tasks = store.list_tasks()

    console.print()
    console.print(f"    [bold blue]📋 ALL TASKS ({len(tasks)})[/bold blue]")
    console.print("    " + "─" * 30, style="dim")

    print_tasks(tasks)


def mark_complete(store: TaskStore):
    """Mark task as complete."""
    console.print()
    console.print("    [bold green]✅ MARK COMPLETE[/bold green]")
    console.print("    " + "─" * 30, style="dim")
    console.print()

    task_id = Prompt.ask("    [cyan]Task ID[/cyan]")

    try:
        task = store.mark_complete(task_id.strip(), True)
        console.print()
        console.print("    [green]✓ Task marked as complete![/green]")
        print_task_details(task)
    except (KeyError, ValueError) as e:
        console.print(f"    [red]✗ Error: {e}[/red]")


def mark_incomplete(store: TaskStore):
    """Mark task as incomplete."""
    console.print()
    console.print("    [bold yellow]⭕ MARK INCOMPLETE[/bold yellow]")
    console.print("    " + "─" * 30, style="dim")
    console.print()

    task_id = Prompt.ask("    [cyan]Task ID[/cyan]")

    try:
        task = store.mark_complete(task_id.strip(), False)
        console.print()
        console.print("    [yellow]○ Task marked as incomplete[/yellow]")
        print_task_details(task)
    except (KeyError, ValueError) as e:
        console.print(f"    [red]✗ Error: {e}[/red]")


def update_task(store: TaskStore):
    """Update a task."""
    console.print()
    console.print("    [bold cyan]🖋️  UPDATE TASK[/bold cyan]")
    console.print("    " + "─" * 30, style="dim")
    console.print()

    task_id = Prompt.ask("    [cyan]Task ID[/cyan]")

    old_task = store.get_task(task_id.strip())
    if old_task is None:
        console.print("    [red]✗ Task not found[/red]")
        return

    print_task_details(old_task, "Current Details")

    console.print("    [dim]Press Enter to keep current value[/dim]")
    console.print()

    new_title = Prompt.ask("    [cyan]New title[/cyan]", default="")
    new_title = new_title.strip() if new_title.strip() else None

    new_desc = Prompt.ask("    [cyan]New description[/cyan] [dim](type 'clear' to remove)[/dim]", default="")
    if new_desc.lower() == 'clear':
        new_desc = ""
    elif not new_desc.strip():
        new_desc = None
    else:
        new_desc = new_desc.strip()

    try:
        task = store.update_task(task_id.strip(), title=new_title, description=new_desc)
        console.print()
        console.print("    [green]✓ Task updated![/green]")
        print_task_details(task)
    except (KeyError, ValueError) as e:
        console.print(f"    [red]✗ Error: {e}[/red]")


def delete_task(store: TaskStore):
    """Delete a task."""
    console.print()
    console.print("    [bold red]🗑️  DELETE TASK[/bold red]")
    console.print("    " + "─" * 30, style="dim")
    console.print()

    task_id = Prompt.ask("    [cyan]Task ID[/cyan]")

    task = store.get_task(task_id.strip())
    if task is None:
        console.print("    [red]✗ Task not found[/red]")
        return

    print_task_details(task, "⚠️  Task to Delete")

    confirm = Prompt.ask("    [red]Delete this task?[/red]", choices=["y", "n"], default="n")

    if confirm == "y":
        try:
            store.delete_task(task_id.strip())
            console.print()
            console.print("    [green]✓ Task deleted[/green]")
        except (KeyError, ValueError) as e:
            console.print(f"    [red]✗ Error: {e}[/red]")
    else:
        console.print("    [dim]Cancelled[/dim]")


def print_goodbye():
    """Print goodbye message."""
    console.print()
    console.print("=" * 60, style="bold magenta")
    console.print()

    console.print("       👋 [bold green]Goodbye![/bold green]")
    console.print()
    console.print("       [yellow]Thanks for using Todo App[/yellow]")

    branding = Text()
    branding.append("       Built by ", style="dim")
    branding.append("CodeWithHamza", style="bold cyan")
    console.print(branding)

    console.print()
    console.print("=" * 60, style="bold magenta")
    console.print()


def run_interactive():
    """Run interactive CLI."""
    store = TaskStore()

    # Welcome
    print_header()

    while True:
        print_menu()

        choice = Prompt.ask("    [bold yellow]Select option (1-7)[/bold yellow]")

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
            print_goodbye()
            break
        else:
            console.print("    [red]Invalid choice. Enter 1-7[/red]")

        console.print()
        Prompt.ask("    [dim]Press Enter to continue[/dim]", default="")


if __name__ == "__main__":
    run_interactive()
