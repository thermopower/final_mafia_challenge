/**
 * LogoutConfirmDialog - 로그아웃 확인 다이얼로그
 *
 * 책임:
 * - 로그아웃 확인 UI 제공
 * - 취소 및 로그아웃 버튼 제공
 */
import React from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from '@mui/material'

interface LogoutConfirmDialogProps {
  open: boolean
  onClose: () => void
  onConfirm: () => void
}

export const LogoutConfirmDialog: React.FC<LogoutConfirmDialogProps> = ({
  open,
  onClose,
  onConfirm,
}) => {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      aria-labelledby="logout-dialog-title"
      aria-describedby="logout-dialog-description"
    >
      <DialogTitle id="logout-dialog-title">로그아웃 확인</DialogTitle>
      <DialogContent>
        <DialogContentText id="logout-dialog-description">
          로그아웃하시겠습니까?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          취소
        </Button>
        <Button onClick={onConfirm} color="primary" variant="contained" autoFocus>
          로그아웃
        </Button>
      </DialogActions>
    </Dialog>
  )
}
