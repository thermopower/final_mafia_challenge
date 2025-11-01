/**
 * useLogout 훅 테스트
 *
 * TDD Red-Green-Refactor 사이클에 따라 작성
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { useLogout } from '../useLogout'
import { authService } from '@/infrastructure/external/authService'
import { AuthProvider } from '@/application/contexts/AuthContext'
import type { ReactNode } from 'react'

// Mock 설정
vi.mock('@/infrastructure/external/authService')
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}))

// Wrapper 컴포넌트
const wrapper = ({ children }: { children: ReactNode }) => (
  <AuthProvider>{children}</AuthProvider>
)

describe('useLogout', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // localStorage 초기화
    localStorage.clear()
  })

  it('logout 호출 시 Supabase Auth 로그아웃을 수행한다', async () => {
    // Arrange
    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockResolvedValue({ error: null })

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    await act(async () => {
      await result.current.logout()
    })

    // Assert
    expect(mockSignOut).toHaveBeenCalled()
  })

  it('logout 호출 시 로컬 스토리지에서 토큰을 삭제한다', async () => {
    // Arrange
    localStorage.setItem('access_token', 'mock-access-token')
    localStorage.setItem('refresh_token', 'mock-refresh-token')

    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockResolvedValue({ error: null })

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    await act(async () => {
      await result.current.logout()
    })

    // Assert
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
  })

  it('Supabase Auth 실패 시에도 로컬 토큰을 삭제하고 로그아웃을 진행한다', async () => {
    // Arrange
    localStorage.setItem('access_token', 'mock-access-token')

    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockResolvedValue({ error: new Error('Network error') })

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    await act(async () => {
      await result.current.logout()
    })

    // Assert
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('logout 중 loading 상태가 true가 된다', async () => {
    // Arrange
    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({ error: null }), 100))
    )

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    let loadingDuringLogout = false

    act(() => {
      result.current.logout().then(() => {})
    })

    // Assert
    await waitFor(() => {
      if (result.current.loading) {
        loadingDuringLogout = true
      }
    })

    expect(loadingDuringLogout).toBe(true)
  })

  it('logout 완료 후 loading 상태가 false가 된다', async () => {
    // Arrange
    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockResolvedValue({ error: null })

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    await act(async () => {
      await result.current.logout()
    })

    // Assert
    expect(result.current.loading).toBe(false)
  })

  it('로그아웃 성공 시 error가 null이다', async () => {
    // Arrange
    const mockSignOut = vi.mocked(authService.signOut)
    mockSignOut.mockResolvedValue({ error: null })

    // Act
    const { result } = renderHook(() => useLogout(), { wrapper })

    await act(async () => {
      await result.current.logout()
    })

    // Assert
    expect(result.current.error).toBeNull()
  })
})
