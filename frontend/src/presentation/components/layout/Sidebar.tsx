/**
 * Sidebar - 사이드 네비게이션
 *
 * 책임:
 * - 대시보드 메뉴 표시
 * - 권한별 메뉴 필터링
 */
import React from 'react'
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  Science as ScienceIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
  Upload as UploadIcon,
  Storage as StorageIcon,
} from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/application/contexts/AuthContext'

const drawerWidth = 240

export const Sidebar: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user } = useAuth()

  const menuItems = [
    { text: '통합 대시보드', icon: <DashboardIcon />, path: '/dashboard', roles: ['admin', 'user'] },
    { text: '연구 성과', icon: <ScienceIcon />, path: '/dashboard/research', roles: ['admin', 'user'] },
    { text: '학생 현황', icon: <PeopleIcon />, path: '/dashboard/students', roles: ['admin', 'user'] },
    { text: '예산 집행', icon: <MoneyIcon />, path: '/dashboard/budget', roles: ['admin'] },
    { text: '데이터 업로드', icon: <UploadIcon />, path: '/upload', roles: ['admin'] },
    { text: '데이터 조회', icon: <StorageIcon />, path: '/data', roles: ['admin', 'user'] },
  ]

  const filteredMenuItems = menuItems.filter((item) =>
    user ? item.roles.includes(user.role) : false
  )

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Toolbar />
      <List>
        {filteredMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  )
}
