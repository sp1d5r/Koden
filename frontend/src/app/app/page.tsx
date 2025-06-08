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
  const [repos, setRepos] = useState<Repo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
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
        setError('Failed to load profile')
        console.error('Profile fetch error:', err)
      }
    }
  }

  const fetchRepos = async () => {
    try {
      const data = await get<RepoListResponse>('/repos/')
      // Fetch tasks for each repo
      const reposWithTasks = await Promise.all(
        data.repos.map(async (repo) => {
          const tasks = await get<RepoDownloadTask[]>(`/tasks/repos/${repo.id}/download-tasks`)
          return { ...repo, download_tasks: tasks }
        })
      )
      setRepos(reposWithTasks)
    } catch (err) {
      console.error('Failed to fetch repos:', err)
    }
  }

  useEffect(() => {
    const initialize = async () => {
      if (user) {
        await Promise.all([fetchProfile(), fetchRepos()])
      }
      setLoading(false)
    }

    initialize()
  }, [user])

  const handleProfileComplete = async () => {
    setShowCompletionModal(false)
    setLoading(true)
    try {
      const data = await get<UserProfile>('/users/me')
      setProfile(data)
    } catch (err) {
      setError('Failed to load profile')
      console.error('Profile fetch error after completion:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleRepoUpdate = async () => {
    try {
      const data = await get<RepoListResponse>('/repos/');
      setRepos(data.repos);
    } catch (err) {
      console.error('Failed to fetch repos:', err);
    }
  };

  if (authLoading || loading || !user) {
    return <FullPageLoading />
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-destructive mb-2">Error</h2>
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    )
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
          {repos.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-4">
                You haven't connected any repositories yet.
              </p>
              <Button onClick={() => setShowConnectRepo(true)}>
                Connect Your First Repository
              </Button>
            </div>
          ) : (
            <RepoList repos={repos} onUpdate={handleRepoUpdate} />
          )}
        </div>
      </DashboardLayout>
      <ConnectRepoModal
        open={showConnectRepo}
        onClose={() => setShowConnectRepo(false)}
        onConnect={handleRepoUpdate}
      />
      <ProfileCompletionModal
        isOpen={showCompletionModal}
        onClose={() => setShowCompletionModal(false)}
        onComplete={handleProfileComplete}
      />
    </>
  )
} 