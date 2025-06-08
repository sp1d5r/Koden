import { useState } from 'react';
import { useAPI } from '@/hooks/useAPI';
import { Repo, RepoUpdate } from '@/types/repo';
import { Button } from '@/components/atoms/button';
import { Badge } from '@/components/atoms/badge';
import { formatDistanceToNow } from 'date-fns';
import { Pencil, Trash2, ExternalLink } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/atoms/dialog';
import { Input } from '@/components/atoms/input';
import { Card } from '@/components/atoms/card';
import { RepoDownloadTasks } from './repo-download-tasks';

interface RepoListProps {
  repos: Repo[];
  onUpdate: () => void;
}

export function RepoList({ repos, onUpdate }: RepoListProps) {
  const { patch, delete: del } = useAPI();
  const [editingRepo, setEditingRepo] = useState<Repo | null>(null);
  const [editForm, setEditForm] = useState<RepoUpdate>({});

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

    try {
      await patch<Repo>(`/repos/${editingRepo.id}`, editForm);
      onUpdate();
      setEditingRepo(null);
    } catch (error) {
      console.error('Failed to update repo:', error);
    }
  };

  const handleDelete = async (repoId: number) => {
    if (!confirm('Are you sure you want to delete this repository?')) return;

    try {
      await del(`/repos/${repoId}`);
      const updatedRepos = repos.filter(repo => repo.id !== repoId);
      onUpdate();
    } catch (error) {
      console.error('Failed to delete repo:', error);
    }
  };

  return (
    <div className="grid gap-6">
      {repos.map((repo) => (
        <Card key={repo.id} className="p-6">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold">{repo.name}</h2>
              <p className="text-sm text-muted-foreground">
                {repo.github_url}
                {repo.branch && ` (${repo.branch})`}
              </p>
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
              />
            </div>
            <div>
              <label className="text-sm font-medium">GitHub URL</label>
              <Input
                value={editForm.github_url || ''}
                onChange={(e) => setEditForm({ ...editForm, github_url: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Branch</label>
              <Input
                value={editForm.branch || ''}
                onChange={(e) => setEditForm({ ...editForm, branch: e.target.value })}
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setEditingRepo(null)}>
                Cancel
              </Button>
              <Button onClick={handleSave}>Save Changes</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
} 