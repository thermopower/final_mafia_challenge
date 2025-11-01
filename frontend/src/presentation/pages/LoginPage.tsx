import React from 'react';
import { Container, Box, Typography, Paper } from '@mui/material';
import { LoginForm } from '@/presentation/components/forms/LoginForm';

export const LoginPage: React.FC = () => {
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            대학교 데이터 대시보드
          </Typography>
          <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
            로그인하여 계속하기
          </Typography>
          <LoginForm />
        </Paper>
      </Box>
    </Container>
  );
};
