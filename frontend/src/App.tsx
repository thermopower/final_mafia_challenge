import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '@/application/contexts/AuthContext';
import { PrivateRoute } from '@/infrastructure/routing/PrivateRoute';
import { PublicRoute } from '@/infrastructure/routing/PublicRoute';
import { AdminRoute } from '@/infrastructure/routing/AdminRoute';
import { LoginPage } from '@/presentation/pages/LoginPage';
import { SignupPage } from '@/presentation/pages/SignupPage';
import { DashboardPage } from '@/presentation/pages/DashboardPage';
import { ResearchPage } from '@/presentation/pages/ResearchPage';
import { StudentPage } from '@/presentation/pages/StudentPage';
import UploadPage from '@/presentation/pages/UploadPage';
import { DataViewPage } from '@/presentation/pages/DataViewPage';
import ProfilePage from '@/presentation/pages/ProfilePage';
import { AppLayout } from '@/presentation/components/layout/AppLayout';

function AppContent() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
        <Route path="/signup" element={<PublicRoute><SignupPage /></PublicRoute>} />
        <Route path="/" element={<PrivateRoute><AppLayout /></PrivateRoute>}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="dashboard/research" element={<ResearchPage />} />
          <Route path="dashboard/students" element={<StudentPage />} />
          <Route path="upload" element={<AdminRoute><UploadPage /></AdminRoute>} />
          <Route path="data" element={<DataViewPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
