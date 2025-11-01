/**
 * PublicRoute - 공개 라우트 (로그인 페이지 등)
 *
 * 책임:
 * - 로그인하지 않은 사용자만 접근 허용
 * - 이미 로그인한 사용자는 대시보드로 리다이렉트
 */
import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/application/contexts/AuthContext'
import { Loading } from '@/presentation/components/common/Loading'

interface PublicRouteProps {
  children: React.ReactNode
}

export const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <Loading message="로딩 중..." />
  }

  if (isAuthenticated) {
    // 이미 로그인된 사용자는 대시보드로 리다이렉트
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}
