/**
 * useDebounce Hook
 *
 * 입력값을 디바운싱하여 API 호출 빈도를 줄입니다.
 */

import { useState, useEffect } from 'react';

/**
 * 디바운스 훅
 *
 * @param value 디바운싱할 값
 * @param delay 지연 시간 (밀리초, 기본값: 300ms)
 * @returns 디바운싱된 값
 */
export const useDebounce = <T>(value: T, delay: number = 300): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // delay 후에 값을 업데이트
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // 다음 effect가 실행되기 전 또는 컴포넌트 언마운트 시 타이머 정리
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
