import { useState } from 'react';
import { useAPI } from '@/hooks/useAPI';
import { Button } from '@/components/atoms/button';
import { Input } from '@/components/atoms/input';
import { useAuth } from '@/hooks/useAuth';
import { Label } from '@/components/atoms/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/atoms/avatar';

interface ProfileCompletionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
}

interface UserResponse {
  id: number;
  email: string;
  name: string;
  firebase_uid: string;
}

export const ProfileCompletionModal = ({
  isOpen,
  onClose,
  onComplete,
}: ProfileCompletionModalProps) => {
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const { post } = useAPI();

  if (!isOpen || !user) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await post<UserResponse>('/users', {
        email: user.email,
        name,
      });
      onComplete();
    } catch (err: any) {
      console.error('Failed to create user profile:', err);
      setError(err.response?.data?.detail || 'Failed to create profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50">
      <div className="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] w-full max-w-md">
        <div className="bg-card p-6 rounded-lg shadow-lg">
          <div className="flex items-center gap-4 mb-6">
            <Avatar className="h-16 w-16">
              <AvatarImage src={user.photoURL || undefined} />
              <AvatarFallback>{getInitials(name || user.displayName || '')}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-2xl font-bold">Complete Your Profile</h2>
              <p className="text-muted-foreground">
                Just one more step to get started
              </p>
            </div>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                value={user.email || ''}
                disabled
                className="bg-muted"
              />
              <p className="text-sm text-muted-foreground">
                Your email is managed by your GitHub account
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                required
                disabled={loading}
              />
            </div>

            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
            
            <div className="flex justify-end gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={onClose}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Saving...' : 'Complete Profile'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}; 