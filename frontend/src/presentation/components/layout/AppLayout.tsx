/**
 * AppLayout - 메인 레이아웃 컴포넌트
 *
 * 책임:
 * - 공통 레이아웃 제공
 * - Navbar, Sidebar, Footer 포함
 * - 비활성 경고 다이얼로그 표시
 */
import React, { ReactNode } from 'react'
import { Box } from '@mui/material'
import { Navbar } from './Navbar'
import { Sidebar } from './Sidebar'
import { InactivityWarningDialog } from '@/presentation/components/common/InactivityWarningDialog'
import { useAuth } from '@/application/contexts/AuthContext'

interface AppLayoutProps {
  children: ReactNode
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { showInactivityWarning, dismissInactivityWarning } = useAuth()

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Navbar />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8, // Navbar 높이만큼 여백
          ml: { sm: '240px' }, // Sidebar 너비만큼 왼쪽 여백
        }}
      >
        {children}
      </Box>

      {/* 비활성 경고 다이얼로그 */}
      <InactivityWarningDialog
        open={showInactivityWarning}
        onContinue={dismissInactivityWarning}
      />
    </Box>
  )
}
