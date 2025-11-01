/**
 * useInactivityTimeout 훅
 *
 * 책임:
 * - 사용자 비활성 상태 감지 (30분)
 * - 비활성 경고 표시 (29분 후)
 * - 자동 로그아웃 (30분 후)
 * - 사용자 활동 감지 및 타이머 리셋
 */
import { useEffect, useState } from 'react'
import { useLogout } from './useLogout'

export const useInactivityTimeout = (timeoutMs: number = 30 * 60 * 1000) => {
  const { logout } = useLogout()
  const [showWarning, setShowWarning] = useState(false)

  useEffect(() => {
    let warningTimer: NodeJS.Timeout
    let logoutTimer: NodeJS.Timeout

    const resetTimers = () => {
      // 기존 타이머 정리
      clearTimeout(warningTimer)
      clearTimeout(logoutTimer)

      // 경고 숨김
      setShowWarning(false)

      // 29분 후 경고 표시
      warningTimer = setTimeout(() => {
        setShowWarning(true)
      }, timeoutMs - 60000) // 1분 전에 경고

      // 30분 후 자동 로그아웃
      logoutTimer = setTimeout(() => {
        logout()
      }, timeoutMs)
    }

    const handleActivity = () => {
      resetTimers()
    }

    // 활동 감지 이벤트 리스너 등록
    window.addEventListener('mousedown', handleActivity)
    window.addEventListener('keydown', handleActivity)
    window.addEventListener('scroll', handleActivity)
    window.addEventListener('touchstart', handleActivity)

    // 초기 타이머 시작
    resetTimers()

    // 클린업: 타이머 정리 및 이벤트 리스너 제거
    return () => {
      clearTimeout(warningTimer)
      clearTimeout(logoutTimer)
      window.removeEventListener('mousedown', handleActivity)
      window.removeEventListener('keydown', handleActivity)
      window.removeEventListener('scroll', handleActivity)
      window.removeEventListener('touchstart', handleActivity)
    }
  }, [logout, timeoutMs])

  return { showWarning, setShowWarning }
}
