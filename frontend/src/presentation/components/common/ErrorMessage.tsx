/**
 * ErrorMessage - 오류 메시지 컴포넌트
 *
 * 책임:
 * - 오류 메시지 표시
 * - 재시도 버튼 표시 (선택)
 */
import React from 'react'
import { Alert, AlertTitle, Button } from '@mui/material'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <Alert severity="error" sx={{ mb: 2 }}>
      <AlertTitle>오류</AlertTitle>
      {message}
      {onRetry && (
        <Button size="small" onClick={onRetry} sx={{ mt: 1 }}>
          다시 시도
        </Button>
      )}
    </Alert>
  )
}
