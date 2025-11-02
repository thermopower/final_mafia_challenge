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
apiClient.interceptors.request.use(
  async (config) => {
    const token = await authService.getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response Interceptor: 401 오류 처리
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // 401 오류 처리
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Supabase의 세션 갱신 시도
        const session = await authService.refreshSession()

        if (session?.access_token) {
          // 토큰이 갱신되면 원래 요청을 재시도
          originalRequest.headers.Authorization = `Bearer ${session.access_token}`
          return apiClient(originalRequest)
        } else {
          // 세션 갱신 실패 시 로그아웃
          await authService.signOut()
          return Promise.reject(error)
        }
      } catch (refreshError) {
        // 갱신 실패 시 로그아웃
        await authService.signOut()
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
