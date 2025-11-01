/**
 * Data API Service
 *
 * 데이터 조회 및 필터링 API 호출
 */

import apiClient from './client';
import type { PaginatedData, DataFilter, UnifiedDataItem } from '@/domain/models/DataView';

export const dataApi = {
  /**
   * 데이터 목록 조회
   *
   * @param filters 필터 조건
   * @param page 페이지 번호 (기본값: 1)
   * @param pageSize 페이지 크기 (기본값: 20)
   * @returns 페이지네이션된 데이터
   */
  async getData(
    filters: DataFilter,
    page: number = 1,
    pageSize: number = 20
  ): Promise<PaginatedData> {
    const params: Record<string, string> = {
      page: page.toString(),
      page_size: pageSize.toString(),
    };

    if (filters.type) {
      params.type = filters.type;
    }

    if (filters.year) {
      params.year = filters.year.toString();
    }

    if (filters.search) {
      params.search = filters.search;
    }

    if (filters.ordering) {
      params.ordering = filters.ordering;
    }

    const response = await apiClient.get<PaginatedData>('/data/', { params });
    return response.data;
  },

  /**
   * 데이터 상세 조회
   *
   * @param dataType 데이터 유형
   * @param id 데이터 ID
   * @returns 데이터 항목
   */
  async getDataById(dataType: string, id: number): Promise<UnifiedDataItem> {
    const response = await apiClient.get<UnifiedDataItem>(`/data/${dataType}/${id}/`);
    return response.data;
  },
};
