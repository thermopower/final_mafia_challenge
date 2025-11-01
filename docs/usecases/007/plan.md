# UC-007: 로그아웃 - 구현 계획

## 1. 개요

### 1.1 기능 요약
- **목적**: 로그인한 사용자가 안전하게 로그아웃
- **핵심 기능**:
  - 수동 로그아웃 (확인 다이얼로그)
  - 자동 로그아웃 (토큰 만료, 비활성 타임아웃)
  - 세션 정리 (토큰 삭제, AuthContext 초기화)
- **사용자**: 모든 로그인 사용자

### 1.2 아키텍처 원칙
- **Layered Architecture**
- **SOLID 원칙**
- **TDD**

---

## 2. Backend 구현

### 2.1 API 엔드포인트

```
POST /api/auth/logout/
Request:
(Authorization: Bearer {token})

Response 200 OK:
{
  "message": "로그아웃되었습니다"
}
```

### 2.2 Service Layer

**주요 메서드**:
```python
class LogoutService:
    def logout(self, user_id: str):
        """로그아웃 이력 기록 (선택 사항)"""
        pass
```

---

## 3. Frontend 구현

### 3.1 Application Layer

```typescript
export const useLogout = () => {
  const { setUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const logout = async () => {
    setLoading(true);
    setError(null);

    try {
      // Supabase Auth 로그아웃
      const { error: supabaseError } = await authService.signOut();
      if (supabaseError) {
        throw supabaseError;
      }

      // Backend에 로그아웃 이력 기록 (선택 사항)
      try {
        await accountApi.logout();
      } catch (err) {
        // Backend 실패해도 로그아웃 진행
        console.warn('Backend logout failed:', err);
      }

      // 로컬 스토리지 정리
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');

      // AuthContext 초기화
      setUser(null);

      // 로그인 페이지로 리다이렉트
      window.location.href = '/login';
    } catch (err) {
      setError('로그아웃 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  return { logout, loading, error };
};
```

```typescript
// 비활성 타임아웃
export const useInactivityTimeout = (timeoutMs: number = 30 * 60 * 1000) => {
  const { logout } = useLogout();
  const [showWarning, setShowWarning] = useState(false);

  useEffect(() => {
    let warningTimer: NodeJS.Timeout;
    let logoutTimer: NodeJS.Timeout;

    const resetTimers = () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);

      // 29분 후 경고 표시
      warningTimer = setTimeout(() => {
        setShowWarning(true);
      }, timeoutMs - 60000);

      // 30분 후 자동 로그아웃
      logoutTimer = setTimeout(() => {
        logout();
      }, timeoutMs);
    };

    const handleActivity = () => {
      setShowWarning(false);
      resetTimers();
    };

    // 활동 감지 이벤트
    window.addEventListener('mousedown', handleActivity);
    window.addEventListener('keydown', handleActivity);
    window.addEventListener('scroll', handleActivity);
    window.addEventListener('touchstart', handleActivity);

    resetTimers();

    return () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
      window.removeEventListener('mousedown', handleActivity);
      window.removeEventListener('keydown', handleActivity);
      window.removeEventListener('scroll', handleActivity);
      window.removeEventListener('touchstart', handleActivity);
    };
  }, [logout, timeoutMs]);

  return { showWarning, setShowWarning };
};
```

### 3.2 Presentation Layer

**파일**:
- `frontend/src/presentation/components/layout/LogoutButton.tsx`
- `frontend/src/presentation/components/common/LogoutConfirmDialog.tsx`
- `frontend/src/presentation/components/common/InactivityWarningDialog.tsx`

---

## 4. TDD 구현 계획

### 4.1 Backend TDD

**Test Case 1: LogoutViewSet - API**
```python
@pytest.mark.django_db
class TestLogoutViewSet:
    def test_logout_returns_200(self, api_client, auth_token):
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

        response = api_client.post('/api/auth/logout/')

        assert response.status_code == 200
        assert response.data['message'] == '로그아웃되었습니다'
```

### 4.2 Frontend TDD

**Test Case 2: useLogout 훅**
```typescript
import { renderHook, act, waitFor } from '@testing-library/react';
import { useLogout } from '../useLogout';
import { authService } from '@/infrastructure/external/authService';
import { accountApi } from '@/services/api/accountApi';

vi.mock('@/infrastructure/external/authService');
vi.mock('@/services/api/accountApi');

describe('useLogout', () => {
  it('logout 호출 시 Supabase 로그아웃 및 토큰 삭제를 수행한다', async () => {
    (authService.signOut as any).mockResolvedValue({ error: null });
    (accountApi.logout as any).mockResolvedValue({});

    const { result } = renderHook(() => useLogout());

    await act(async () => {
      await result.current.logout();
    });

    expect(authService.signOut).toHaveBeenCalled();
    expect(accountApi.logout).toHaveBeenCalled();
  });
});
```

**Test Case 3: useInactivityTimeout 훅**
```typescript
import { renderHook, act } from '@testing-library/react';
import { useInactivityTimeout } from '../useInactivityTimeout';

vi.useFakeTimers();

describe('useInactivityTimeout', () => {
  it('29분 후 경고를 표시한다', () => {
    const { result } = renderHook(() => useInactivityTimeout(30 * 60 * 1000));

    expect(result.current.showWarning).toBe(false);

    act(() => {
      vi.advanceTimersByTime(29 * 60 * 1000);
    });

    expect(result.current.showWarning).toBe(true);
  });
});
```

---

## 5. 파일 생성 순서

### 5.1 Backend
```
1. Presentation Layer
   ├── backend/apps/accounts/tests/test_logout_views.py
   └── backend/apps/accounts/presentation/views.py (logout 엔드포인트 추가)
```

### 5.2 Frontend
```
1. Application Layer
   ├── frontend/src/application/hooks/__tests__/useLogout.test.ts
   ├── frontend/src/application/hooks/useLogout.ts
   ├── frontend/src/application/hooks/__tests__/useInactivityTimeout.test.ts
   └── frontend/src/application/hooks/useInactivityTimeout.ts

2. Presentation Layer
   ├── frontend/src/presentation/components/layout/LogoutButton.tsx
   ├── frontend/src/presentation/components/common/LogoutConfirmDialog.tsx
   └── frontend/src/presentation/components/common/InactivityWarningDialog.tsx
```

---

## 6. 성공 기준

### 6.1 Backend
- [ ] 로그아웃 이력 기록 정상

### 6.2 Frontend
- [ ] 수동 로그아웃 정상
- [ ] 확인 다이얼로그 표시
- [ ] Supabase Auth 로그아웃 정상
- [ ] 로컬 토큰 삭제 정상
- [ ] AuthContext 초기화 정상
- [ ] 비활성 타임아웃 (30분) 정상
- [ ] 비활성 경고 (29분) 정상
- [ ] 자동 로그아웃 정상

---

## 7. 마무리

이 계획서는 UC-007 (로그아웃) 기능을 TDD 원칙에 따라 구현하기 위한 가이드입니다.

**핵심 원칙**:
1. **Supabase Auth 로그아웃** 연동
2. **로컬 토큰 삭제**로 완전한 세션 종료
3. **비활성 타임아웃** (30분)으로 보안 강화
4. **서버 실패 시에도 로그아웃 진행** (로컬 우선)
