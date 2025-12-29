"""Task business logic service."""

from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


async def get_tasks(session: AsyncSession, user_id: str) -> list[Task]:
    """Get all tasks for a user."""
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return list(result.scalars().all())


async def get_task(
    session: AsyncSession, user_id: str, task_id: int
) -> Optional[Task]:
    """Get a single task by ID for a user."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_task(
    session: AsyncSession, user_id: str, task_data: TaskCreate
) -> Task:
    """Create a new task for a user."""
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession, user_id: str, task_id: int, task_data: TaskUpdate
) -> Optional[Task]:
    """Update an existing task."""
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def toggle_complete(
    session: AsyncSession, user_id: str, task_id: int
) -> Optional[Task]:
    """Toggle task completion status."""
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession, user_id: str, task_id: int
) -> bool:
    """Delete a task. Returns True if deleted, False if not found."""
    task = await get_task(session, user_id, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
