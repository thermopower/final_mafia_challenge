/**
 * Export API Service
 *
 * CSV 내보내기 API 호출
 */

import apiClient from './client';
import type { DataFilter } from '@/domain/models/DataView';

export const exportApi = {
  /**
   * CSV 파일 내보내기
   *
   * @param filters 필터 조건
   * @returns Promise<void> (파일 다운로드 트리거)
   */
  async exportToCSV(filters: DataFilter): Promise<void> {
    // 1. 쿼리 파라미터 구성
    const params: Record<string, string> = {};

    if (filters.type) {
      params.type = filters.type;
    }

    if (filters.year) {
      params.year = filters.year.toString();
    }

    if (filters.search) {
      params.search = filters.search;
    }

    // 2. API 호출 (responseType: 'blob'로 설정)
    const response = await apiClient.get('/data/export/', {
      params,
      responseType: 'blob', // Blob으로 응답 받기
    });

    // 3. Blob으로부터 파일 다운로드 트리거
    const blob = new Blob([response.data], { type: 'text/csv; charset=utf-8-sig' });

    // 4. Content-Disposition 헤더에서 파일명 추출
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'export.csv'; // 기본 파일명

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1];
      }
    }

    // 5. 다운로드 링크 생성 및 클릭 트리거
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // 6. 정리
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};
