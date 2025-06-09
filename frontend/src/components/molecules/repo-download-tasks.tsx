import { RepoDownloadTask } from '@/types/repo'
import { Badge } from '@/components/atoms/badge'
import { Button } from '@/components/atoms/button'
import { useAPI } from '@/hooks/useAPI'
import { useState, useEffect } from 'react'
import { toast } from 'sonner'
import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { Trash2 } from 'lucide-react'

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

interface TaskStatusResponse {
  taskId: string;
  status: TaskStatus | null;
}

const statusColors = {
  pending: 'bg-yellow-500',
  processing: 'bg-blue-500',
  completed: 'bg-green-500',
  failed: 'bg-red-500'
}

export function RepoDownloadTasks({ repoId, tasks, onUpdate }: RepoDownloadTasksProps) {
  const { post, get, delete: deleteTask } = useAPI()
  const queryClient = useQueryClient()
  const [isLoading, setIsLoading] = useState(false)

  // Get active tasks (only pending or processing)
  const activeTasks = tasks.filter(task => 
    task.status === 'pending' || task.status === 'processing'
  )

  // Single query for all active tasks
  const { data: taskStatuses, error } = useQuery<TaskStatusResponse[]>({
    queryKey: ['taskStatuses', activeTasks.map(t => t.task_id)],
    queryFn: async () => {
      const statuses = await Promise.all(
        activeTasks.map(async (task) => {
          try {
            const response = await get<TaskStatus>(`/tasks/${task.task_id}/status`)
            return { taskId: task.task_id, status: response }
          } catch (error: any) {
            // If task is not found (404), mark it as failed
            if (error?.response?.status === 404) {
              return { 
                taskId: task.task_id, 
                status: { 
                  status: 'failed', 
                  error_message: 'Task not found in queue' 
                } 
              }
            }
            console.error(`Failed to poll task ${task.task_id}:`, error)
            return { taskId: task.task_id, status: null }
          }
        })
      )
      return statuses
    },
    refetchInterval: activeTasks.length > 0 ? 2000 : false,
    enabled: activeTasks.length > 0,
    gcTime: 0,
    staleTime: 0
  })

  // Handle status updates
  useEffect(() => {
    if (taskStatuses) {
      const hasStatusChange = taskStatuses.some(({ taskId, status }) => {
        const task = tasks.find(t => t.task_id === taskId)
        return task && status && status.status !== task.status
      })
      
      if (hasStatusChange) {
        onUpdate()
      }
    }
  }, [taskStatuses, tasks, onUpdate])

  // Handle errors
  useEffect(() => {
    if (error) {
      console.error('Error polling tasks:', error)
      toast.error('Failed to get task statuses')
    }
  }, [error])

  // Mutation for creating new download task
  const createDownloadTask = useMutation({
    mutationFn: async () => {
      const response = await post<RepoDownloadTask>(`/tasks/repos/${repoId}/download`, {})
      return response
    },
    onSuccess: () => {
      toast.success('Download task started successfully')
      onUpdate()
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.detail || 'Failed to start download'
      toast.error(errorMessage)
    }
  })

  // Mutation for deleting a task
  const deleteTaskMutation = useMutation({
    mutationFn: async (taskId: string) => {
      await deleteTask(`/tasks/${taskId}`)
    },
    onSuccess: () => {
      toast.success('Task deleted successfully')
      onUpdate()
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.detail || 'Failed to delete task'
      toast.error(errorMessage)
    }
  })

  const handleDownload = async () => {
    setIsLoading(true)
    try {
      await createDownloadTask.mutateAsync()
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      await deleteTaskMutation.mutateAsync(taskId)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Download Tasks</h3>
        <Button 
          onClick={handleDownload} 
          disabled={isLoading || createDownloadTask.isPending}
          variant="outline"
        >
          {isLoading || createDownloadTask.isPending ? 'Starting...' : 'Download Repository'}
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
              <div className="flex items-center gap-2">
                {task.status === 'completed' && task.output_path && (
                  <Button variant="link" size="sm">
                    View Files
                  </Button>
                )}
                <Button 
                  variant="ghost" 
                  size="icon"
                  onClick={() => handleDelete(task.task_id)}
                  disabled={deleteTaskMutation.isPending}
                >
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 