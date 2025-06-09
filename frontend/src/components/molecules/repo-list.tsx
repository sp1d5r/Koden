import { useState } from 'react';
import { useAPI } from '@/hooks/useAPI';
import { Repo, RepoUpdate } from '@/types/repo';
import { Button } from '@/components/atoms/button';
import { Badge } from '@/components/atoms/badge';
import { formatDistanceToNow } from 'date-fns';
import { Pencil, Trash2, ExternalLink, Loader2 } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/atoms/dialog';
import { Input } from '@/components/atoms/input';
import { Card } from '@/components/atoms/card';
import { RepoDownloadTasks } from './repo-download-tasks';
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface RepoListProps {
  repos: Repo[];
  onUpdate: () => void;
}

export function RepoList({ repos, onUpdate }: RepoListProps) {
  const { patch, delete: del } = useAPI();
  const queryClient = useQueryClient();
  const [editingRepo, setEditingRepo] = useState<Repo | null>(null);
  const [editForm, setEditForm] = useState<RepoUpdate>({});

  const updateRepoMutation = useMutation({
    mutationFn: async ({ repoId, data }: { repoId: number; data: RepoUpdate }) => {
      return patch<Repo>(`/repos/${repoId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repos'] });
      setEditingRepo(null);
    },
  });

  const deleteRepoMutation = useMutation({
    mutationFn: async (repoId: number) => {
      return del(`/repos/${repoId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repos'] });
    },
  });

  const handleEdit = (repo: Repo) => {
    setEditingRepo(repo);
    setEditForm({
      name: repo.name,
      github_url: repo.github_url,
      branch: repo.branch,
    });
  };

  const handleSave = async () => {
    if (!editingRepo) return;
    updateRepoMutation.mutate({ repoId: editingRepo.id, data: editForm });
  };

  const handleDelete = async (repoId: number) => {
    if (!confirm('Are you sure you want to delete this repository?')) return;
    deleteRepoMutation.mutate(repoId);
  };

  return (
    <div className="grid gap-6">
      {repos.map((repo) => (
        <Card key={repo.id} className="p-6">
          <div className="space-y-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-semibold">{repo.name}</h2>
                <p className="text-sm text-muted-foreground">
                  {repo.github_url}
                  {repo.branch && ` (${repo.branch})`}
                </p>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => handleEdit(repo)}
                  disabled={updateRepoMutation.isPending || deleteRepoMutation.isPending}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => handleDelete(repo.id)}
                  disabled={updateRepoMutation.isPending || deleteRepoMutation.isPending}
                >
                  {deleteRepoMutation.isPending && deleteRepoMutation.variables === repo.id ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
            
            <RepoDownloadTasks 
              repoId={repo.id}
              tasks={repo.download_tasks || []}
              onUpdate={onUpdate}
            />
          </div>
        </Card>
      ))}

      <Dialog open={!!editingRepo} onOpenChange={() => setEditingRepo(null)}>
        <DialogContent>
          <DialogTitle>Edit Repository</DialogTitle>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Name</label>
              <Input
                value={editForm.name || ''}
                onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                disabled={updateRepoMutation.isPending}
              />
            </div>
            <div>
              <label className="text-sm font-medium">GitHub URL</label>
              <Input
                value={editForm.github_url || ''}
                onChange={(e) => setEditForm({ ...editForm, github_url: e.target.value })}
                disabled={updateRepoMutation.isPending}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Branch</label>
              <Input
                value={editForm.branch || ''}
                onChange={(e) => setEditForm({ ...editForm, branch: e.target.value })}
                disabled={updateRepoMutation.isPending}
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button 
                variant="outline" 
                onClick={() => setEditingRepo(null)}
                disabled={updateRepoMutation.isPending}
              >
                Cancel
              </Button>
              <Button 
                onClick={handleSave}
                disabled={updateRepoMutation.isPending}
              >
                {updateRepoMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Saving...
                  </>
                ) : (
                  'Save Changes'
                )}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
} 