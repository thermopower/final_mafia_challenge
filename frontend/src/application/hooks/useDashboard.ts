import { useState, useEffect } from 'react'
import { dashboardApi } from '@/services/api/dashboardApi'
import { DashboardSummary } from '@/domain/models/Dashboard'

interface UseDashboardParams {
  year?: number
  department?: string
}

interface UseDashboardReturn {
  data: DashboardSummary | null
  isLoading: boolean
  error: string | null
  refetch: () => Promise<void>
}

/**
 * 대시보드 데이터 조회 커스텀 훅
 *
 * @param params - 필터 파라미터
 * @returns 대시보드 데이터 및 상태
 */
export const useDashboard = (params: UseDashboardParams = {}): UseDashboardReturn => {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const result = await dashboardApi.getDashboardSummary(params)
      setData(result)
    } catch (err: any) {
      setError(err.response?.data?.error || '데이터를 불러오는 중 오류가 발생했습니다')
      console.error('Dashboard fetch error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [params.year, params.department])

  return {
    data,
    isLoading,
    error,
    refetch: fetchData
  }
}
