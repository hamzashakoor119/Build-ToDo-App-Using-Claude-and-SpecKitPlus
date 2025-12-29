'use client'

import { useState } from 'react'
import type { Task } from '@/types/task'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'

interface TaskItemProps {
  task: Task
  onToggleComplete: (taskId: number) => Promise<void>
  onEdit: (task: Task) => void
  onDelete: (taskId: number) => Promise<void>
}

export default function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const [loading, setLoading] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  const handleToggle = async () => {
    setLoading(true)
    try {
      await onToggleComplete(task.id)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    setLoading(true)
    try {
      await onDelete(task.id)
    } finally {
      setLoading(false)
      setShowDeleteConfirm(false)
    }
  }

  return (
    <Card variant="bordered" className="mb-3">
      <div className="flex flex-col sm:flex-row sm:items-start gap-3">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <button
            onClick={handleToggle}
            disabled={loading}
            aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
            className={`
              mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0
              transition-colors cursor-pointer
              ${
                task.completed
                  ? 'bg-primary-600 border-primary-600 text-white'
                  : 'border-gray-300 hover:border-primary-400'
              }
              ${loading ? 'opacity-50 cursor-wait' : ''}
            `}
          >
            {task.completed && (
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3
              className={`font-medium break-words ${
                task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p
                className={`text-sm mt-1 break-words ${
                  task.completed ? 'text-gray-300' : 'text-gray-600'
                }`}
              >
                {task.description}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-2">
              {new Date(task.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        <div className="flex gap-2 sm:flex-shrink-0 ml-8 sm:ml-0">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(task)}
            disabled={loading}
            aria-label="Edit task"
          >
            <svg className="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span className="hidden sm:inline">Edit</span>
          </Button>

          {showDeleteConfirm ? (
            <div className="flex gap-1">
              <Button
                variant="danger"
                size="sm"
                onClick={handleDelete}
                loading={loading}
              >
                Yes
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowDeleteConfirm(false)}
                disabled={loading}
              >
                No
              </Button>
            </div>
          ) : (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowDeleteConfirm(true)}
              disabled={loading}
              className="text-red-600 hover:bg-red-50"
              aria-label="Delete task"
            >
              <svg className="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span className="hidden sm:inline">Delete</span>
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}
