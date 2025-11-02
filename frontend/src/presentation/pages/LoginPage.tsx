import React from 'react';
import { Container, Box, Typography, Paper, Link as MuiLink } from '@mui/material';
import { Link } from 'react-router-dom';
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
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              계정이 없으신가요?{' '}
              <MuiLink component={Link} to="/signup" variant="body2">
                회원가입
              </MuiLink>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};
