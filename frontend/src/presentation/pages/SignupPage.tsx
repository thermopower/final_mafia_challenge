import React from 'react';
import { Container, Box, Typography, Paper, Link as MuiLink } from '@mui/material';
import { Link } from 'react-router-dom';
import { SignupForm } from '@/presentation/components/forms/SignupForm';

export const SignupPage: React.FC = () => {
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
            회원가입
          </Typography>
          <SignupForm />
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              이미 계정이 있으신가요?{' '}
              <MuiLink component={Link} to="/login" variant="body2">
                로그인
              </MuiLink>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};
