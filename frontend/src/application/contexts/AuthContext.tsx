/**
 * AuthContext - 전역 인증 상태 관리
 *
 * 책임:
 * - 전역 인증 상태 관리
 * - 사용자 정보 저장
 * - 로그인/로그아웃 함수 제공
 * - 비활성 타임아웃 관리
 */
import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '@/infrastructure/external/authService'
import { User } from '@/domain/models/User'
import { useInactivityTimeout } from '@/application/hooks/useInactivityTimeout'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, fullName?: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
  showInactivityWarning: boolean
  dismissInactivityWarning: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()

  // logout 함수를 먼저 정의 (useInactivityTimeout에 전달하기 위해)
  const logout = useCallback(async () => {
    setIsLoading(true)
    try {
      await authService.signOut()
      setUser(null)
      navigate('/login')
    } catch (error) {
      console.error('로그아웃 실패:', error)
    } finally {
      setIsLoading(false)
    }
  }, [navigate])

  // 비활성 타임아웃 (로그인된 사용자만)
  const { showWarning, setShowWarning } = useInactivityTimeout(30 * 60 * 1000, logout)
  const showInactivityWarning = !!user && showWarning

  // 초기 로드 시 현재 사용자 조회
  useEffect(() => {
    const loadUser = async () => {
      try {
        const currentUser = await authService.getCurrentUser()
        if (currentUser) {
          setUser({
            id: currentUser.id,
            email: currentUser.email || '',
            full_name: currentUser.user_metadata?.full_name || '',
            role: currentUser.user_metadata?.role || 'user',
          })
        }
      } catch (error) {
        console.error('사용자 정보 로드 실패:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadUser()
  }, [])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const { data, error } = await authService.signIn(email, password)

      if (error) {
        throw new Error(error.message || '로그인에 실패했습니다')
      }

      if (data?.user) {
        setUser({
          id: data.user.id,
          email: data.user.email || '',
          full_name: data.user.user_metadata?.full_name || '',
          role: data.user.user_metadata?.role || 'user',
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  const signup = async (email: string, password: string, fullName?: string) => {
    setIsLoading(true)
    try {
      const { data, error } = await authService.signUp(email, password, fullName)

      if (error) {
        throw new Error(error.message || '회원가입에 실패했습니다')
      }

      // Supabase는 기본적으로 이메일 확인을 요구하므로,
      // 회원가입 후 자동 로그인되지 않을 수 있습니다.
      if (data?.user) {
        setUser({
          id: data.user.id,
          email: data.user.email || '',
          full_name: data.user.user_metadata?.full_name || '',
          role: data.user.user_metadata?.role || 'user',
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  const refreshUser = async () => {
    try {
      const currentUser = await authService.getCurrentUser()
      if (currentUser) {
        setUser({
          id: currentUser.id,
          email: currentUser.email || '',
          full_name: currentUser.user_metadata?.full_name || '',
          role: currentUser.user_metadata?.role || 'user',
        })
      }
    } catch (error) {
      console.error('사용자 정보 갱신 실패:', error)
    }
  }

  const dismissInactivityWarning = () => {
    setShowWarning(false)
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    signup,
    logout,
    refreshUser,
    showInactivityWarning,
    dismissInactivityWarning,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
