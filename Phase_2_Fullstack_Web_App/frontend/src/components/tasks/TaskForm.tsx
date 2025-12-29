'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { useSession } from '@/lib/auth-client'
import { getErrorMessage } from '@/lib/errors'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import Card from '@/components/ui/Card'

interface TaskFormProps {
  onTaskAdded: () => void
}

export default function TaskForm({ onTaskAdded }: TaskFormProps) {
  const { data: session } = useSession()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const titleRemaining = 200 - title.length
  const descRemaining = 1000 - description.length

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess(false)

    if (!title.trim()) {
      setError('Please enter a title for your task')
      return
    }

    if (title.length > 200) {
      setError('Title is too long. Please keep it under 200 characters.')
      return
    }

    if (description.length > 1000) {
      setError('Description is too long. Please keep it under 1000 characters.')
      return
    }

    if (!session?.user?.id) {
      setError('Please log in to add tasks')
      return
    }

    setLoading(true)
    try {
      await api.tasks.create(session.user.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      })

      setTitle('')
      setDescription('')
      setSuccess(true)
      onTaskAdded()

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <h2 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Add New Task</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex items-start gap-2">
            <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex items-center gap-2">
            <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Task added successfully!</span>
          </div>
        )}

        <div>
          <Input
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            maxLength={200}
            required
            error={titleRemaining < 0 ? 'Title is too long' : undefined}
          />
          <p className={`text-xs mt-1 ${titleRemaining < 20 ? 'text-orange-500' : 'text-gray-400'}`}>
            {titleRemaining} characters remaining
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details..."
            maxLength={1000}
            rows={2}
            className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm sm:text-base ${
              descRemaining < 0 ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          <p className={`text-xs mt-1 ${descRemaining < 50 ? 'text-orange-500' : 'text-gray-400'}`}>
            {descRemaining} characters remaining
          </p>
        </div>

        <Button
          type="submit"
          loading={loading}
          disabled={titleRemaining < 0 || descRemaining < 0}
          className="w-full sm:w-auto"
        >
          Add Task
        </Button>
      </form>
    </Card>
  )
}
