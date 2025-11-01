/**
 * useExport Hook
 *
 * CSV 내보내기 상태 관리
 */

import { useState } from 'react';
import { exportApi } from '@/services/api/exportApi';
import type { DataFilter } from '@/domain/models/DataView';

/**
 * CSV 내보내기 훅
 *
 * @returns 내보내기 상태 및 제어 함수
 */
export const useExport = () => {
  const [exporting, setExporting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * CSV 파일 내보내기
   *
   * @param filters 필터 조건
   */
  const exportToCSV = async (filters: DataFilter) => {
    setExporting(true);
    setError(null);

    try {
      await exportApi.exportToCSV(filters);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error || 'CSV 내보내기 중 오류가 발생했습니다';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setExporting(false);
    }
  };

  return {
    exporting,
    error,
    exportToCSV,
  };
};
