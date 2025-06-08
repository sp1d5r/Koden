import { RepoDownloadTask } from '@/types/repo'
import { Badge } from '@/components/atoms/badge'
import { Button } from '@/components/atoms/button'
import { useAPI } from '@/hooks/useAPI'
import { useState, useEffect } from 'react'

interface RepoDownloadTasksProps {
  repoId: number;
  tasks: RepoDownloadTask[];
  onUpdate: () => void;
}

interface TaskStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  output_path?: string;
  error_message?: string;
}

const statusColors = {
  pending: 'bg-yellow-500',
  processing: 'bg-blue-500',
  completed: 'bg-green-500',
  failed: 'bg-red-500'
}

const POLLING_INTERVAL = 2000; // 2 seconds

export function RepoDownloadTasks({ repoId, tasks, onUpdate }: RepoDownloadTasksProps) {
  const { post, get } = useAPI()
  const [isLoading, setIsLoading] = useState(false)
  const [activeTasks, setActiveTasks] = useState<Set<string>>(new Set())

  // Update active tasks set when tasks prop changes
  useEffect(() => {
    const newActiveTasks = new Set(
      tasks
        .filter(task => task.status === 'pending' || task.status === 'processing')
        .map(task => task.task_id)
    )
    setActiveTasks(newActiveTasks)
  }, [tasks])

  // Poll for task status updates
  useEffect(() => {
    if (activeTasks.size === 0) return

    const pollTasks = async () => {
      const updates = await Promise.all(
        Array.from(activeTasks).map(async (taskId) => {
          try {
            const response = await get<TaskStatus>(`/tasks/repos/${repoId}/download-tasks/${taskId}/status`)
            return { taskId, status: response.status }
          } catch (error) {
            console.error(`Failed to poll task ${taskId}:`, error)
            return { taskId, status: 'failed' as const }
          }
        })
      )

      // Check if any tasks are no longer active
      const stillActive = updates.filter(update => 
        update.status === 'pending' || update.status === 'processing'
      ).map(update => update.taskId)

      if (stillActive.length !== activeTasks.size) {
        // Some tasks completed or failed, trigger a full update
        onUpdate()
      }
    }

    const interval = setInterval(pollTasks, POLLING_INTERVAL)
    return () => clearInterval(interval)
  }, [activeTasks, get, onUpdate])

  const handleDownload = async () => {
    setIsLoading(true)
    try {
      await post(`/tasks/repos/${repoId}/download`, {})
      onUpdate()
    } catch (error) {
      console.error('Failed to start download:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Download Tasks</h3>
        <Button 
          onClick={handleDownload} 
          disabled={isLoading}
          variant="outline"
        >
          {isLoading ? 'Starting...' : 'Download Repository'}
        </Button>
      </div>
      
      {tasks.length === 0 ? (
        <p className="text-sm text-muted-foreground">No download tasks yet</p>
      ) : (
        <div className="space-y-2">
          {tasks.map((task) => (
            <div 
              key={task.task_id} 
              className="flex items-center justify-between p-3 bg-card rounded-lg border"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge className={statusColors[task.status]}>
                    {task.status}
                  </Badge>
                  <span className="text-sm text-muted-foreground">
                    {new Date(task.created_at).toLocaleString()}
                  </span>
                </div>
                {task.error_message && (
                  <p className="text-sm text-destructive">{task.error_message}</p>
                )}
              </div>
              {task.status === 'completed' && task.output_path && (
                <Button variant="link" size="sm">
                  View Files
                </Button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 