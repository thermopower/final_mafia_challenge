import { createBrowserRouter } from 'react-router-dom';
import { PrivateRoute } from './PrivateRoute';
import { PublicRoute } from './PublicRoute';
import { AdminRoute } from './AdminRoute';
import { LoginPage } from '@/presentation/pages/LoginPage';
import { DashboardPage } from '@/presentation/pages/DashboardPage';
import UploadPage from '@/presentation/pages/UploadPage';
import { DataViewPage } from '@/presentation/pages/DataViewPage';
import ProfilePage from '@/presentation/pages/ProfilePage';
import { AppLayout } from '@/presentation/components/layout/AppLayout';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <PublicRoute><LoginPage /></PublicRoute>,
  },
  {
    path: '/',
    element: <PrivateRoute><AppLayout /></PrivateRoute>,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'dashboard', element: <DashboardPage /> },
      {
        path: 'upload',
        element: <AdminRoute><UploadPage /></AdminRoute>
      },
      { path: 'data', element: <DataViewPage /> },
      { path: 'profile', element: <ProfilePage /> },
    ],
  },
]);
