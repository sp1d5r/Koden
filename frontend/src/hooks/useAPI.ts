import { useCallback } from 'react';
import { useAuth } from './useAuth';

// For Next.js, we can use process.env
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface RequestOptions extends RequestInit {
  requiresAuth?: boolean;
}

interface HeadersInit {
  [key: string]: string;
}

export function useAPI() {
  const { user } = useAuth();

  const getAuthHeaders = useCallback(async (): Promise<Record<string, string>> => {
    if (!user) return {};
    return {
      Authorization: `Bearer ${await user.getIdToken()}`,
    };
  }, [user]);

  const handleResponse = async (response: Response) => {
    if (!response.ok) {
      const error = await response.json().catch(() => null);
      throw { response: { data: error } };
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
      return null;
    }
    
    const data = await response.json();
    console.log('[useAPI] Response data:', data);
    return data;
  };

  const get = useCallback(async <T>(endpoint: string): Promise<T> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      headers,
    });
    return handleResponse(response);
  }, [getAuthHeaders]);

  const post = useCallback(async <T>(endpoint: string, data: any): Promise<T> => {
    const authHeaders = await getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  }, [getAuthHeaders]);

  const patch = useCallback(async <T>(endpoint: string, data: any): Promise<T> => {
    const authHeaders = await getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  }, [getAuthHeaders]);

  const del = useCallback(async (endpoint: string): Promise<void> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: 'DELETE',
      headers,
    });
    return handleResponse(response);
  }, [getAuthHeaders]);

  return { get, post, patch, delete: del };
} 