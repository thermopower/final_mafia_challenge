/**
 * AdminRoute - 관리자만 접근 가능한 라우트
 *
 * 책임:
 * - 관리자 권한 사용자만 접근 허용
 * - 일반 사용자는 403 페이지 표시
 */
import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/application/contexts/AuthContext'
import { Box, Typography } from '@mui/material'
import { Button } from '@/presentation/components/common/Button'

interface AdminRouteProps {
  children: React.ReactNode
}

export const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (user?.role !== 'admin') {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          p: 3,
        }}
      >
        <Typography variant="h4" gutterBottom>
          접근 권한이 없습니다
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          관리자만 접근할 수 있는 페이지입니다.
        </Typography>
        <Button onClick={() => window.history.back()} variant="outlined">
          돌아가기
        </Button>
      </Box>
    )
  }

  return <>{children}</>
}
