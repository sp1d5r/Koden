"use client"

import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/atoms/button'
import { useState } from 'react'

export default function LoginPage() {
  const { login, loading } = useAuth()
  const [isRedirecting, setIsRedirecting] = useState(false)
  const [loginError, setLoginError] = useState<string | null>(null)

  const handleLogin = async () => {
    try {
      setLoginError(null)
      await login()
      setIsRedirecting(true)
      if (typeof window !== 'undefined') {
        window.location.href = '/app'
      }
    } catch (error) {
      console.error('Login error:', error)
      setLoginError('Failed to sign in. Please try again.')
    }
  }

  if (isRedirecting) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="bg-card p-8 rounded-xl shadow-lg flex flex-col items-center gap-6">
          <h1 className="text-2xl font-bold">Setting up your account...</h1>
          <p className="text-muted-foreground">
            Please wait while we configure your access.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="bg-card p-8 rounded-xl shadow-lg flex flex-col items-center gap-6">
        <h1 className="text-2xl font-bold">Sign in to Koden</h1>
        <Button size="lg" onClick={handleLogin} disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in with GitHub'}
        </Button>
        {loginError && (
          <p className="text-red-500 text-sm">{loginError}</p>
        )}
      </div>
    </div>
  )
} 