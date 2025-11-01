/**
 * Account API Service
 *
 * 사용자 계정 및 프로필 관련 API 호출을 처리합니다.
 */

import client from './client';
import type { UserProfile } from '@/domain/models/User';

/**
 * 프로필 업데이트 요청 타입
 */
export interface ProfileUpdateRequest {
  full_name?: string;
  department?: string;
  profile_picture_url?: string;
}

/**
 * 비밀번호 변경 요청 타입
 */
export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

/**
 * 현재 사용자의 프로필을 조회합니다.
 *
 * @returns 사용자 프로필 정보
 */
export const getProfile = async (): Promise<UserProfile> => {
  const response = await client.get<UserProfile>('/account/profile/');
  return response.data;
};

/**
 * 현재 사용자의 프로필을 업데이트합니다.
 *
 * @param data - 업데이트할 프로필 데이터
 * @returns 업데이트된 사용자 프로필 정보
 */
export const updateProfile = async (data: ProfileUpdateRequest): Promise<UserProfile> => {
  const response = await client.put<UserProfile>('/account/profile/', data);
  return response.data;
};

/**
 * 현재 사용자의 비밀번호를 변경합니다.
 *
 * @param data - 현재 비밀번호 및 새 비밀번호
 */
export const changePassword = async (data: ChangePasswordRequest): Promise<void> => {
  await client.post('/account/profile/change-password/', data);
};

const accountApi = {
  getProfile,
  updateProfile,
  changePassword,
};

export default accountApi;
