/**
 * Input - 커스텀 입력 컴포넌트
 *
 * 책임:
 * - 일관된 스타일의 입력 필드 제공
 * - 오류 메시지 표시
 */
import React from 'react'
import { TextField } from '@mui/material'

interface InputProps {
  label: string
  type?: 'text' | 'email' | 'password' | 'number'
  value: string
  onChange: (value: string) => void
  error?: string
  required?: boolean
  fullWidth?: boolean
  multiline?: boolean
  rows?: number
}

export const Input: React.FC<InputProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  error,
  required = false,
  fullWidth = true,
  multiline = false,
  rows,
}) => {
  return (
    <TextField
      label={label}
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      error={!!error}
      helperText={error}
      required={required}
      fullWidth={fullWidth}
      multiline={multiline}
      rows={rows}
      margin="normal"
    />
  )
}
