/**
 * Upload API Service
 */
import client from './client';
import { UploadResult, PaginatedUploadHistory } from '@/domain/models/Upload';

export const uploadApi = {
  /**
   * Excel 파일 업로드
   */
  async uploadExcel(
    formData: FormData,
    onUploadProgress?: (progressEvent: any) => void
  ): Promise<UploadResult> {
    const response = await client.post('/upload/upload/excel/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    });
    return response.data;
  },

  /**
   * 업로드 이력 조회
   */
  async getUploadHistory(
    page: number = 1,
    pageSize: number = 20
  ): Promise<PaginatedUploadHistory> {
    const response = await client.get('/upload/upload/history/', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },
};
