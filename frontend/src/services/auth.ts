import { GithubAuthProvider, signInWithPopup, signOut } from 'firebase/auth'
import { auth } from './firebase'

export const loginWithGitHub = async () => {
  const provider = new GithubAuthProvider()
  return signInWithPopup(auth, provider)
}

export const logout = async () => {
  return signOut(auth)
} 