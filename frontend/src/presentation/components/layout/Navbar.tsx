/**
 * Navbar - 상단 네비게이션 바
 *
 * 책임:
 * - 로고/제목 표시
 * - 사용자 프로필 드롭다운
 * - 로그아웃 버튼
 * - 로그아웃 확인 다이얼로그
 */
import React, { useState } from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Box,
} from '@mui/material'
import {
  AccountCircle,
  Logout as LogoutIcon,
} from '@mui/icons-material'
import { useAuth } from '@/application/contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { LogoutConfirmDialog } from '@/presentation/components/common/LogoutConfirmDialog'
import { useLogout } from '@/application/hooks/useLogout'

export const Navbar: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const { logout } = useLogout()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [logoutDialogOpen, setLogoutDialogOpen] = useState(false)

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  const handleProfile = () => {
    handleClose()
    navigate('/profile')
  }

  const handleLogoutClick = () => {
    handleClose()
    setLogoutDialogOpen(true)
  }

  const handleLogoutConfirm = async () => {
    setLogoutDialogOpen(false)
    await logout()
  }

  const handleLogoutCancel = () => {
    setLogoutDialogOpen(false)
  }

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          대학교 데이터 대시보드
        </Typography>

        {user && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">{user.full_name || user.email}</Typography>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleProfile}>내 프로필</MenuItem>
              <MenuItem onClick={handleLogoutClick}>
                <LogoutIcon fontSize="small" sx={{ mr: 1 }} />
                로그아웃
              </MenuItem>
            </Menu>
          </Box>
        )}
      </Toolbar>

      {/* 로그아웃 확인 다이얼로그 */}
      <LogoutConfirmDialog
        open={logoutDialogOpen}
        onClose={handleLogoutCancel}
        onConfirm={handleLogoutConfirm}
      />
    </AppBar>
  )
}
