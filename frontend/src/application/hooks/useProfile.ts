/**
 * useProfile Hook
 *
 * 사용자 프로필 조회 및 수정 상태를 관리합니다.
 */

import { useState, useEffect } from 'react';
import accountApi, { ProfileUpdateRequest, ChangePasswordRequest } from '@/services/api/accountApi';
import type { UserProfile } from '@/domain/models/User';
import { authService } from '@/infrastructure/external/authService';
import { useNavigate } from 'react-router-dom';

export const useProfile = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);
  const navigate = useNavigate();

  /**
   * 프로필 조회
   */
  const fetchProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await accountApi.getProfile();
      setProfile(response);
    } catch (err: any) {
      setError(err.response?.data?.error || '프로필을 불러오는 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  /**
   * 프로필 업데이트
   */
  const updateProfile = async (data: ProfileUpdateRequest) => {
    setLoading(true);
    setError(null);
    try {
      const updated = await accountApi.updateProfile(data);
      setProfile(updated);
      setEditMode(false);
    } catch (err: any) {
      setError(err.response?.data?.error || '프로필 업데이트 중 오류가 발생했습니다');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * 비밀번호 변경
   *
   * 비밀번호 변경 후 자동으로 로그아웃하고 로그인 페이지로 이동합니다.
   */
  const changePassword = async (currentPassword: string, newPassword: string) => {
    setLoading(true);
    setError(null);
    try {
      // Supabase Auth를 사용하여 비밀번호 변경
      await authService.updatePassword(newPassword);

      // 비밀번호 변경 후 자동 로그아웃
      await authService.signOut();

      // 로그인 페이지로 리다이렉트
      navigate('/login');
    } catch (err: any) {
      setError(err.message || '비밀번호 변경 중 오류가 발생했습니다');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    profile,
    loading,
    error,
    editMode,
    setEditMode,
    fetchProfile,
    updateProfile,
    changePassword,
  };
};
