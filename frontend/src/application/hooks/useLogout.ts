/**
 * useLogout 훅
 *
 * 책임:
 * - 수동 로그아웃 처리
 * - Supabase Auth 로그아웃
 * - 로컬 토큰 삭제
 * - AuthContext 초기화
 * - 로그인 페이지로 리다이렉트
 */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '@/infrastructure/external/authService'
import { useAuth } from '@/application/contexts/AuthContext'

export const useLogout = () => {
  const navigate = useNavigate()
  const { logout: contextLogout } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const logout = async () => {
    setLoading(true)
    setError(null)

    try {
      // 1. Supabase Auth 로그아웃
      const { error: supabaseError } = await authService.signOut()
      if (supabaseError) {
        console.warn('Supabase 로그아웃 실패:', supabaseError)
        // 서버 실패 시에도 로그아웃 진행
      }

      // 2. 로컬 스토리지에서 토큰 삭제
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

      // 3. AuthContext 초기화
      await contextLogout()

      // 4. 로그인 페이지로 리다이렉트
      navigate('/login')
    } catch (err) {
      console.error('로그아웃 오류:', err)
      setError('로그아웃 중 오류가 발생했습니다')

      // 오류 발생 시에도 로컬 토큰은 삭제
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  return { logout, loading, error }
}
