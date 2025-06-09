"use client"

import { useAuth } from '@/hooks/useAuth'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAPI } from '@/hooks/useAPI'
import { FullPageLoading } from '@/components/loading/full-page-loading'
import { ProfileCompletionModal } from '@/components/modals/profile-completion-modal'
import DashboardLayout from '@/components/templates/dashboard-layout'
import { ConnectRepoModal } from '@/components/modals/ConnectRepoModal'
import { RepoList } from '@/components/molecules/repo-list'
import { Repo, RepoListResponse, RepoDownloadTask } from '@/types/repo'
import { Button } from '@/components/atoms/button'
import { useQuery } from '@tanstack/react-query'
import { Skeleton } from '@/components/atoms/skeleton'

interface UserProfile {
  id: number;
  email: string;
  name: string;
  firebase_uid: string;
}

export default function AppPage() {
  const { user, loading: authLoading } = useAuth()
  const router = useRouter()
  const { get } = useAPI()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [showCompletionModal, setShowCompletionModal] = useState(false)
  const [showConnectRepo, setShowConnectRepo] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) {
      router.replace('/login')
    }
  }, [user, authLoading, router])

  const fetchProfile = async () => {
    if (!user) return
    
    try {
      const data = await get<UserProfile>('/users/me')
      setProfile(data)
    } catch (err: any) {
      if (err.response?.data?.detail === "User profile not found") {
        setShowCompletionModal(true)
      } else {
        console.error('Profile fetch error:', err)
      }
    }
  }

  const { data: reposData, isLoading: isLoadingRepos, refetch: refetchRepos } = useQuery({
    queryKey: ['repos'],
    queryFn: async () => {
      const data = await get<RepoListResponse>('/repos/')
      // Fetch tasks for each repo
      const reposWithTasks = await Promise.all(
        data.repos.map(async (repo) => {
          const tasks = await get<RepoDownloadTask[]>(`/tasks/repos/${repo.id}/download-tasks`)
          return { ...repo, download_tasks: tasks }
        })
      )
      return reposWithTasks
    },
    enabled: !!user,
  })

  useEffect(() => {
    if (user) {
      fetchProfile()
    }
  }, [user])

  const handleProfileComplete = async () => {
    setShowCompletionModal(false)
    try {
      const data = await get<UserProfile>('/users/me')
      setProfile(data)
    } catch (err) {
      console.error('Profile fetch error after completion:', err)
    }
  }

  if (authLoading || !user) {
    return <FullPageLoading />
  }

  return (
    <>
      <DashboardLayout onConnectRepo={() => setShowConnectRepo(true)}>
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Your Repositories</h1>
            <Button onClick={() => setShowConnectRepo(true)}>
              Connect Repository
            </Button>
          </div>
          
          {isLoadingRepos ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="p-6 border rounded-lg">
                  <Skeleton className="h-6 w-1/3 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              ))}
            </div>
          ) : reposData?.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-4">
                You haven't connected any repositories yet.
              </p>
              <Button onClick={() => setShowConnectRepo(true)}>
                Connect Your First Repository
              </Button>
            </div>
          ) : (
            <RepoList repos={reposData || []} onUpdate={refetchRepos} />
          )}
        </div>
      </DashboardLayout>
      <ConnectRepoModal
        open={showConnectRepo}
        onClose={() => setShowConnectRepo(false)}
        onConnect={refetchRepos}
      />
      <ProfileCompletionModal
        isOpen={showCompletionModal}
        onClose={() => setShowCompletionModal(false)}
        onComplete={handleProfileComplete}
      />
    </>
  )
} 