/**
 * PrivateRoute - 인증된 사용자만 접근 가능한 라우트
 *
 * 책임:
 * - 로그인 사용자만 접근 허용
 * - 비로그인 시 로그인 페이지로 리다이렉트
 */
import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/application/contexts/AuthContext'
import { Loading } from '@/presentation/components/common/Loading'

interface PrivateRouteProps {
  children: React.ReactNode
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <Loading message="인증 확인 중..." />
  }

  if (!isAuthenticated) {
    // 로그인 페이지로 리다이렉트하고, 로그인 후 원래 페이지로 돌아갈 수 있도록 state에 현재 위치 저장
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
