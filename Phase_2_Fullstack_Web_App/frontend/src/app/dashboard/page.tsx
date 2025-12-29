'use client'

import { useState } from 'react'
import TaskList from '@/components/tasks/TaskList'
import TaskForm from '@/components/tasks/TaskForm'

export default function DashboardPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleTaskAdded = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">My Tasks</h1>
        <p className="text-gray-600">Manage your todo list</p>
      </div>

      <TaskForm onTaskAdded={handleTaskAdded} />

      <TaskList refreshTrigger={refreshTrigger} />
    </div>
  )
}
