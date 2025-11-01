import apiClient from './client'
import { DashboardSummary } from '@/domain/models/Dashboard'

/**
 * Dashboard API 서비스
 */
export const dashboardApi = {
  /**
   * 대시보드 데이터 조회
   *
   * @param params - 필터 파라미터
   * @returns 대시보드 전체 데이터
   */
  async getDashboardSummary(params?: {
    year?: number
    department?: string
  }): Promise<DashboardSummary> {
    const response = await apiClient.get<DashboardSummary>('/dashboard/', {
      params
    })
    return response.data
  }
}
