/**
 * InactivityWarningDialog - 비활성 경고 다이얼로그
 *
 * 책임:
 * - 비활성 타임아웃 경고 UI 제공
 * - 계속 사용 버튼 제공
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

interface InactivityWarningDialogProps {
  open: boolean
  onContinue: () => void
}

export const InactivityWarningDialog: React.FC<InactivityWarningDialogProps> = ({
  open,
  onContinue,
}) => {
  return (
    <Dialog
      open={open}
      onClose={onContinue}
      aria-labelledby="inactivity-dialog-title"
      aria-describedby="inactivity-dialog-description"
    >
      <DialogTitle id="inactivity-dialog-title">비활성 상태 감지</DialogTitle>
      <DialogContent>
        <DialogContentText id="inactivity-dialog-description">
          비활성 상태로 인해 곧 로그아웃됩니다.
          <br />
          계속 사용하시겠습니까?
          <br />
          <br />
          (1분 후 자동 로그아웃)
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onContinue} color="primary" variant="contained" autoFocus>
          계속 사용
        </Button>
      </DialogActions>
    </Dialog>
  )
}
