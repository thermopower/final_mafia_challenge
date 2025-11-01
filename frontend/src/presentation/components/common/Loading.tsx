/**
 * Loading - 로딩 상태 컴포넌트
 *
 * 책임:
 * - 로딩 스피너 표시
 * - 로딩 메시지 표시
 */
import React from 'react'
import { Box, CircularProgress, Typography } from '@mui/material'

interface LoadingProps {
  message?: string
}

export const Loading: React.FC<LoadingProps> = ({ message = '로딩 중...' }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
        p: 3,
      }}
    >
      <CircularProgress />
      <Typography variant="body2" sx={{ mt: 2 }}>
        {message}
      </Typography>
    </Box>
  )
}
