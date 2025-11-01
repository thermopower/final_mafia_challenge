/**
 * Axios 인스턴스
 *
 * JWT 토큰 자동 추가 및 오류 처리를 위한 인터셉터를 포함합니다.
 */
import axios, { AxiosInstance } from 'axios'
import { authService } from '@/infrastructure/external/authService'

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
})

// Request Interceptor: 토큰 자동 추가
apiClient.interceptors.request.use(async (config) => {
  const token = await authService.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response Interceptor: 401 오류 시 토큰 갱신 시도
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // 401 오류 → Refresh Token으로 갱신 시도
    // 갱신 실패 → 로그인 페이지로 리다이렉트
    if (error.response?.status === 401) {
      // 리프레시 로직 (Supabase는 자동으로 처리)
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
