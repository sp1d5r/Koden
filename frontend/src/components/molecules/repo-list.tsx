import { useState } from 'react';
import { useAPI } from '@/hooks/useAPI';
import { Repo, RepoUpdate } from '@/types/repo';
import { Button } from '@/components/atoms/button';
import { Badge } from '@/components/atoms/badge';
import { formatDistanceToNow } from 'date-fns';
import { Pencil, Trash2, ExternalLink } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/atoms/dialog';
import { Input } from '@/components/atoms/input';

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
    <div className="space-y-4">
      {repos.map((repo) => (
        <div
          key={repo.id}
          className="flex flex-col p-4 rounded-lg border hover:border-primary/50 transition-colors"
        >
          <div className="flex justify-between items-start gap-4">
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-lg truncate">
                <a
                  href={repo.github_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:underline flex items-center gap-1"
                >
                  {repo.name}
                  <ExternalLink className="h-4 w-4" />
                </a>
              </h3>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="secondary" className="text-xs">
                  {repo.branch}
                </Badge>
                <span className="text-xs text-muted-foreground">
                  Updated {formatDistanceToNow(new Date(repo.updated_at))} ago
                </span>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleEdit(repo)}
              >
                <Pencil className="h-4 w-4" />
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(repo.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
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