import { RouterProvider } from 'react-router-dom';
import { AuthProvider } from '@/application/contexts/AuthContext';
import { router } from '@/infrastructure/routing/routes';

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
