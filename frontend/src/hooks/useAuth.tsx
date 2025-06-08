"use client"
import React, { createContext, useContext, useEffect, useState } from 'react'
import { User, signInWithPopup, GithubAuthProvider, signOut } from 'firebase/auth'
import { auth } from '@/services/firebase'

interface AuthContextProps {
  user: User | null
  loading: boolean
  githubToken: string | null
  login: () => Promise<{ user: User; token: string }>
  logout: () => Promise<void>
  getIdToken: () => Promise<string>
}

const AuthContext = createContext<AuthContextProps>({
  user: null,
  loading: true,
  githubToken: null,
  login: async () => ({ user: null as unknown as User, token: '' }),
  logout: async () => {},
  getIdToken: async () => '',
})

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [githubToken, setGithubToken] = useState<string | null>(null)

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((_user) => {
      console.log('[Auth] Auth state changed:', { 
        user: _user?.uid,
        email: _user?.email 
      })
      setUser(_user)
      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  const login = async (): Promise<{ user: User; token: string }> => {
    const provider = new GithubAuthProvider()
    provider.addScope('repo')
    provider.addScope('read:user')
    provider.addScope('user:email')
    
    try {
      const result = await signInWithPopup(auth, provider)
      const credential = GithubAuthProvider.credentialFromResult(result)
      const token = credential?.accessToken
      
      console.log('[Auth] GitHub login result:', { 
        hasUser: !!result.user,
        hasToken: !!token,
        userEmail: result.user?.email
      })
      
      if (!token) {
        throw new Error('No GitHub token received')
      }

      if (!result.user) {
        throw new Error('No user received from login')
      }

      setGithubToken(token)

      // Get a fresh ID token
      const idToken = await result.user.getIdToken(true)
      
      // Make the claims update request directly
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/github/store-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({ token })
      })

      if (!response.ok) {
        throw new Error('Failed to update GitHub claims')
      }

      return { user: result.user, token }
    } catch (error) {
      console.error('[Auth] Error during GitHub login:', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      await signOut(auth)
      setGithubToken(null)
    } catch (error) {
      console.error('[Auth] Error signing out:', error)
    }
  }

  const getIdToken = async () => {
    if (!user) throw new Error('No user logged in')
    return user.getIdToken()
  }

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        loading, 
        githubToken,
        login, 
        logout, 
        getIdToken
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 