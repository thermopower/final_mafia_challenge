/**
 * Button - 커스텀 버튼 컴포넌트
 *
 * 책임:
 * - 일관된 스타일의 버튼 제공
 * - 로딩 상태 지원
 */
import React from 'react'
import { Button as MuiButton, CircularProgress, ButtonProps as MuiButtonProps } from '@mui/material'

interface ButtonProps extends Omit<MuiButtonProps, 'onClick'> {
  children: React.ReactNode
  onClick: () => void
  loading?: boolean
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'contained',
  color = 'primary',
  onClick,
  disabled,
  loading,
  ...rest
}) => {
  return (
    <MuiButton
      variant={variant}
      color={color}
      onClick={onClick}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? <CircularProgress size={24} color="inherit" /> : children}
    </MuiButton>
  )
}
