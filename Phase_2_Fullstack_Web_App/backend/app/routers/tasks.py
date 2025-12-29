"""Task API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..middleware.auth import verify_token, verify_user_access, TokenPayload
from ..schemas.task import TaskCreate, TaskUpdate, TaskRead
from ..services import task_service

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=list[TaskRead])
async def list_tasks(
    user_id: str,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """List all tasks for a user."""
    verify_user_access(user_id, token)
    tasks = await task_service.get_tasks(session, user_id)
    return tasks


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    task_id: int,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific task."""
    verify_user_access(user_id, token)
    task = await task_service.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.post(
    "/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """Create a new task."""
    verify_user_access(user_id, token)
    task = await task_service.create_task(session, user_id, task_data)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """Update an existing task."""
    verify_user_access(user_id, token)
    task = await task_service.update_task(session, user_id, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """Toggle task completion status."""
    verify_user_access(user_id, token)
    task = await task_service.toggle_complete(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    token: TokenPayload = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
):
    """Delete a task."""
    verify_user_access(user_id, token)
    deleted = await task_service.delete_task(session, user_id, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
