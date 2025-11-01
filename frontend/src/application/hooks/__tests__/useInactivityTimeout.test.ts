/**
 * useInactivityTimeout 훅 테스트
 *
 * TDD Red-Green-Refactor 사이클에 따라 작성
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useInactivityTimeout } from '../useInactivityTimeout'

// Mock 설정
vi.mock('../useLogout', () => ({
  useLogout: () => ({
    logout: vi.fn(),
    loading: false,
    error: null,
  }),
}))

describe('useInactivityTimeout', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
  })

  it('초기 상태에서 showWarning이 false이다', () => {
    // Arrange & Act
    const { result } = renderHook(() => useInactivityTimeout(30 * 60 * 1000))

    // Assert
    expect(result.current.showWarning).toBe(false)
  })

  it('29분 후 경고를 표시한다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000 // 30분
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    expect(result.current.showWarning).toBe(false)

    // Act - 29분 경과
    act(() => {
      vi.advanceTimersByTime(29 * 60 * 1000)
    })

    // Assert
    expect(result.current.showWarning).toBe(true)
  })

  it('사용자 활동 감지 시 타이머가 리셋된다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    // Act - 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    expect(result.current.showWarning).toBe(false)

    // 사용자 활동 (마우스 클릭)
    act(() => {
      const event = new MouseEvent('mousedown')
      window.dispatchEvent(event)
    })

    // 다시 28분 경과 (총 56분이지만 리셋됨)
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // Assert - 아직 경고 표시 안 됨
    expect(result.current.showWarning).toBe(false)
  })

  it('경고 표시 후 활동 감지 시 경고가 사라진다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    // Act - 29분 경과 (경고 표시)
    act(() => {
      vi.advanceTimersByTime(29 * 60 * 1000)
    })

    expect(result.current.showWarning).toBe(true)

    // 사용자 활동
    act(() => {
      const event = new MouseEvent('mousedown')
      window.dispatchEvent(event)
    })

    // Assert
    expect(result.current.showWarning).toBe(false)
  })

  it('키보드 입력 시 타이머가 리셋된다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    // Act - 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // 키보드 입력
    act(() => {
      const event = new KeyboardEvent('keydown')
      window.dispatchEvent(event)
    })

    // 다시 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // Assert
    expect(result.current.showWarning).toBe(false)
  })

  it('스크롤 시 타이머가 리셋된다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    // Act - 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // 스크롤
    act(() => {
      const event = new Event('scroll')
      window.dispatchEvent(event)
    })

    // 다시 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // Assert
    expect(result.current.showWarning).toBe(false)
  })

  it('터치 입력 시 타이머가 리셋된다', () => {
    // Arrange
    const timeoutMs = 30 * 60 * 1000
    const { result } = renderHook(() => useInactivityTimeout(timeoutMs))

    // Act - 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // 터치
    act(() => {
      const event = new TouchEvent('touchstart')
      window.dispatchEvent(event)
    })

    // 다시 28분 경과
    act(() => {
      vi.advanceTimersByTime(28 * 60 * 1000)
    })

    // Assert
    expect(result.current.showWarning).toBe(false)
  })

  it('컴포넌트 언마운트 시 타이머가 정리된다', () => {
    // Arrange
    const { unmount } = renderHook(() => useInactivityTimeout(30 * 60 * 1000))

    const clearTimeoutSpy = vi.spyOn(global, 'clearTimeout')

    // Act
    unmount()

    // Assert - clearTimeout이 호출되었는지 확인
    expect(clearTimeoutSpy).toHaveBeenCalled()
  })
})
