"use client";

import { Suspense, useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useAPI } from '@/hooks/useAPI';
import { FullPageLoading } from '@/components/loading/full-page-loading';
import { ProfileCompletionModal } from '@/components/modals/profile-completion-modal';

interface UserProfile {
  id: number;
  email: string;
  name: string;
  firebase_uid: string;
}

export default function ProfilePage() {
  const { user } = useAuth();
  const { get } = useAPI();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCompletionModal, setShowCompletionModal] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      if (!user) return;
      
      try {
        const data = await get<UserProfile>('/users/me');
        setProfile(data);
      } catch (err) {
        // If user doesn't exist, show completion modal
        if ((err as Error).message.includes('404')) {
          setShowCompletionModal(true);
        } else {
          console.log(err);
          setError('Failed to load profile');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [user, get]);

  const handleProfileComplete = async () => {
    setShowCompletionModal(false);
    setLoading(true);
    try {
      const data = await get<UserProfile>('/users/me');
      setProfile(data);
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <FullPageLoading />;
  }

  if (loading) {
    return <FullPageLoading />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-destructive mb-2">Error</h2>
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <Suspense fallback={<FullPageLoading />}>
      <div className="container max-w-2xl py-8">
        <div className="bg-card p-6 rounded-lg shadow-lg">
          <h1 className="text-2xl font-bold mb-6">Profile</h1>
          
          {profile ? (
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Name</label>
                <p className="text-lg">{profile.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Email</label>
                <p className="text-lg">{profile.email}</p>
              </div>
            </div>
          ) : (
            <p className="text-muted-foreground">No profile found</p>
          )}
        </div>
      </div>

      <ProfileCompletionModal
        isOpen={showCompletionModal}
        onClose={() => setShowCompletionModal(false)}
        onComplete={handleProfileComplete}
      />
    </Suspense>
  );
} 