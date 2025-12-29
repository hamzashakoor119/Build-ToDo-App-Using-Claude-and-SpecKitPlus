'use client'

import { useState, useEffect, useCallback } from 'react'
import type { Task } from '@/types/task'
import { api } from '@/lib/api'
import { useSession } from '@/lib/auth-client'
import TaskItem from './TaskItem'
import TaskEditModal from './TaskEditModal'

interface TaskListProps {
  refreshTrigger?: number
  onTasksLoaded?: (tasks: Task[]) => void
}

export default function TaskList({
  refreshTrigger = 0,
  onTasksLoaded,
}: TaskListProps) {
  const { data: session } = useSession()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  const fetchTasks = useCallback(async () => {
    if (!session?.user?.id) return

    setLoading(true)
    setError('')

    try {
      const fetchedTasks = await api.tasks.list(session.user.id)
      setTasks(fetchedTasks)
      onTasksLoaded?.(fetchedTasks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }, [session?.user?.id, onTasksLoaded])

  useEffect(() => {
    if (session?.user?.id) {
      fetchTasks()
    }
  }, [fetchTasks, refreshTrigger, session?.user?.id])

  const handleToggleComplete = async (taskId: number) => {
    if (!session?.user?.id) return

    try {
      const updatedTask = await api.tasks.toggleComplete(session.user.id, taskId)
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? updatedTask : t))
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
    }
  }

  const handleEdit = (task: Task) => {
    setEditingTask(task)
  }

  const handleEditSave = async (taskId: number, title: string, description: string) => {
    if (!session?.user?.id) return

    try {
      const updatedTask = await api.tasks.update(session.user.id, taskId, {
        title,
        description: description || undefined,
      })
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? updatedTask : t))
      )
      setEditingTask(null)
    } catch (err) {
      throw err
    }
  }

  const handleDelete = async (taskId: number) => {
    if (!session?.user?.id) return

    try {
      await api.tasks.delete(session.user.id, taskId)
      setTasks((prev) => prev.filter((t) => t.id !== taskId))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
    }
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        <p className="text-gray-500 mt-2">Loading tasks...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
        {error}
        <button
          onClick={fetchTasks}
          className="ml-2 underline hover:no-underline"
        >
          Retry
        </button>
      </div>
    )
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <svg
          className="w-16 h-16 text-gray-300 mx-auto mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-gray-500">Add your first task using the form above!</p>
      </div>
    )
  }

  const pendingTasks = tasks.filter((t) => !t.completed)
  const completedTasks = tasks.filter((t) => t.completed)

  return (
    <>
      <div className="space-y-6">
        {pendingTasks.length > 0 && (
          <div>
            <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">
              Pending ({pendingTasks.length})
            </h2>
            {pendingTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}

        {completedTasks.length > 0 && (
          <div>
            <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">
              Completed ({completedTasks.length})
            </h2>
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>

      {editingTask && (
        <TaskEditModal
          task={editingTask}
          onSave={handleEditSave}
          onClose={() => setEditingTask(null)}
        />
      )}
    </>
  )
}
