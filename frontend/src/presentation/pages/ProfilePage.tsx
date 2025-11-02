/**
 * ProfilePage Component
 *
 * 사용자 프로필 조회 및 수정 페이지
 */

import { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
} from '@mui/material';
import { useProfile } from '@/application/hooks/useProfile';

export default function ProfilePage() {
  const {
    profile,
    loading,
    error,
    editMode,
    setEditMode,
    fetchProfile,
    updateProfile,
    changePassword,
  } = useProfile();

  const [fullName, setFullName] = useState('');
  const [department, setDepartment] = useState('');
  const [passwordModalOpen, setPasswordModalOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirm, setNewPasswordConfirm] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    if (profile) {
      setFullName(profile.full_name || '');
      setDepartment(profile.department || '');
    }
  }, [profile]);

  const handleSaveProfile = async () => {
    try {
      await updateProfile({ full_name: fullName, department });
      setSuccessMessage('프로필이 업데이트되었습니다');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      // Error already handled by useProfile
    }
  };

  const handleChangePassword = async () => {
    setPasswordError('');

    // 유효성 검증
    if (newPassword.length < 8) {
      setPasswordError('비밀번호는 최소 8자 이상이어야 합니다');
      return;
    }

    if (newPassword !== newPasswordConfirm) {
      setPasswordError('비밀번호가 일치하지 않습니다');
      return;
    }

    try {
      await changePassword(currentPassword, newPassword);
      // 성공 시 자동으로 로그아웃되고 로그인 페이지로 이동
    } catch (err) {
      setPasswordError('비밀번호 변경에 실패했습니다');
    }
  };

  if (loading && !profile) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        프로필 관리
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {successMessage && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {successMessage}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              기본 정보
            </Typography>

            <TextField
              fullWidth
              label="이메일"
              value={profile?.email || ''}
              disabled
              margin="normal"
              helperText="이메일은 변경할 수 없습니다"
            />

            <TextField
              fullWidth
              label="이름"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              disabled={!editMode}
              margin="normal"
            />

            <TextField
              fullWidth
              label="부서"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              disabled={!editMode}
              margin="normal"
            />

            <TextField
              fullWidth
              label="역할"
              value={profile?.role || ''}
              disabled
              margin="normal"
              helperText="역할은 관리자만 변경할 수 있습니다"
            />
          </Box>

          <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
            {!editMode ? (
              <>
                <Button variant="contained" onClick={() => setEditMode(true)}>
                  프로필 수정
                </Button>
                <Button variant="outlined" onClick={() => setPasswordModalOpen(true)}>
                  비밀번호 변경
                </Button>
              </>
            ) : (
              <>
                <Button variant="contained" onClick={handleSaveProfile} disabled={loading}>
                  저장
                </Button>
                <Button variant="outlined" onClick={() => setEditMode(false)}>
                  취소
                </Button>
              </>
            )}
          </Box>
        </CardContent>
      </Card>

      {/* 비밀번호 변경 모달 */}
      <Dialog open={passwordModalOpen} onClose={() => setPasswordModalOpen(false)}>
        <DialogTitle>비밀번호 변경</DialogTitle>
        <DialogContent>
          {passwordError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {passwordError}
            </Alert>
          )}

          <TextField
            fullWidth
            type="password"
            label="현재 비밀번호"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            margin="normal"
          />

          <TextField
            fullWidth
            type="password"
            label="새 비밀번호"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            margin="normal"
            helperText="최소 8자 이상"
          />

          <TextField
            fullWidth
            type="password"
            label="새 비밀번호 확인"
            value={newPasswordConfirm}
            onChange={(e) => setNewPasswordConfirm(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPasswordModalOpen(false)}>취소</Button>
          <Button onClick={handleChangePassword} variant="contained" disabled={loading}>
            변경
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
