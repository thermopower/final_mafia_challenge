# UC-006: 프로필 관리 - 구현 계획

## 1. 개요

### 1.1 기능 요약
- **목적**: 로그인한 사용자가 자신의 프로필 정보를 조회 및 수정
- **핵심 기능**:
  - 프로필 조회 (이름, 이메일, 부서, 역할, 가입일)
  - 프로필 수정 (이름, 부서, 프로필 사진)
  - 비밀번호 변경 (Supabase Auth 연동)
- **사용자**: 모든 로그인 사용자

### 1.2 아키텍처 원칙
- **Layered Architecture**
- **SOLID 원칙**
- **TDD**

---

## 2. Backend 구현

### 2.1 API 엔드포인트

```
GET /api/account/profile/
Response 200 OK:
{
  "id": "uuid-123",
  "email": "user@university.ac.kr",
  "full_name": "홍길동",
  "department": "컴퓨터공학과",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-11-01T10:00:00Z"
}

PUT /api/account/profile/
Request:
{
  "full_name": "홍길동",
  "department": "컴퓨터공학과"
}

Response 200 OK:
{
  "id": "uuid-123",
  "email": "user@university.ac.kr",
  "full_name": "홍길동",
  "department": "컴퓨터공학과",
  "role": "user"
}
```

### 2.2 Service Layer

**주요 메서드**:
```python
class ProfileService:
    def get_profile(self, user_id: str) -> User:
        """프로필 조회"""
        pass

    def update_profile(self, user_id: str, profile_data: Dict) -> User:
        """프로필 업데이트"""
        pass
```

---

## 3. Frontend 구현

### 3.1 Application Layer

```typescript
export const useProfile = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const response = await accountApi.getProfile();
      setProfile(response);
    } catch (err) {
      setError('프로필을 불러오는 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (data: Partial<UserProfile>) => {
    setLoading(true);
    try {
      const updated = await accountApi.updateProfile(data);
      setProfile(updated);
      setEditMode(false);
    } catch (err) {
      setError('프로필 업데이트 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      await authService.updatePassword(currentPassword, newPassword);
      // 비밀번호 변경 후 자동 로그아웃
      await authService.signOut();
      // 로그인 페이지로 리다이렉트
    } catch (err) {
      setError('비밀번호 변경 중 오류가 발생했습니다');
    }
  };

  return { profile, loading, error, editMode, setEditMode, fetchProfile, updateProfile, changePassword };
};
```

### 3.2 Presentation Layer

**파일**:
- `frontend/src/presentation/pages/ProfilePage.tsx`
- `frontend/src/presentation/components/profile/ProfileView.tsx`
- `frontend/src/presentation/components/profile/ProfileEditForm.tsx`
- `frontend/src/presentation/components/profile/PasswordChangeModal.tsx`

---

## 4. TDD 구현 계획

### 4.1 Backend TDD

**Test Case 1: ProfileService - 프로필 조회**
```python
class TestProfileService:
    def test_get_profile_returns_user_data(self, mocker):
        mock_repo = mocker.Mock(spec=UserRepository)
        mock_repo.get_by_id.return_value = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='홍길동'
        )

        service = ProfileService(user_repo=mock_repo)
        profile = service.get_profile('uuid-123')

        assert profile.full_name == '홍길동'
```

**Test Case 2: ProfileViewSet - API**
```python
@pytest.mark.django_db
class TestProfileViewSet:
    def test_get_profile_returns_200(self, api_client, auth_token):
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

        response = api_client.get('/api/account/profile/')

        assert response.status_code == 200
        assert 'email' in response.data

    def test_update_profile_returns_200(self, api_client, auth_token):
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

        response = api_client.put('/api/account/profile/', {
            'full_name': '홍길동',
            'department': '컴퓨터공학과'
        })

        assert response.status_code == 200
        assert response.data['full_name'] == '홍길동'
```

### 4.2 Frontend TDD

**Test Case 3: useProfile 훅**
```typescript
import { renderHook, act, waitFor } from '@testing-library/react';
import { useProfile } from '../useProfile';
import { accountApi } from '@/services/api/accountApi';

vi.mock('@/services/api/accountApi');

describe('useProfile', () => {
  it('fetchProfile 호출 시 프로필 데이터를 가져온다', async () => {
    const mockProfile = { id: '1', email: 'user@university.ac.kr', full_name: '홍길동' };
    (accountApi.getProfile as any).mockResolvedValue(mockProfile);

    const { result } = renderHook(() => useProfile());

    await act(async () => {
      await result.current.fetchProfile();
    });

    await waitFor(() => {
      expect(result.current.profile).toEqual(mockProfile);
    });
  });
});
```

---

## 5. 파일 생성 순서

### 5.1 Backend
```
1. Service Layer
   ├── backend/apps/accounts/tests/test_profile_service.py
   └── backend/apps/accounts/services/profile_service.py

2. Presentation Layer
   ├── backend/apps/accounts/tests/test_profile_views.py
   └── backend/apps/accounts/presentation/views.py
```

### 5.2 Frontend
```
1. Application Layer
   ├── frontend/src/application/hooks/__tests__/useProfile.test.ts
   └── frontend/src/application/hooks/useProfile.ts

2. Presentation Layer
   ├── frontend/src/presentation/pages/ProfilePage.tsx
   ├── frontend/src/presentation/components/profile/ProfileView.tsx
   ├── frontend/src/presentation/components/profile/ProfileEditForm.tsx
   └── frontend/src/presentation/components/profile/PasswordChangeModal.tsx
```

---

## 6. 성공 기준

### 6.1 Backend
- [ ] 프로필 조회 정상
- [ ] 프로필 업데이트 정상
- [ ] 읽기 전용 필드 보호 (이메일, 역할)

### 6.2 Frontend
- [ ] 프로필 조회 및 표시 정상
- [ ] 수정 모드 전환 정상
- [ ] 비밀번호 변경 후 자동 로그아웃
- [ ] 비밀번호 강도 표시

---

## 7. 마무리

이 계획서는 UC-006 (프로필 관리) 기능을 TDD 원칙에 따라 구현하기 위한 가이드입니다.

**핵심 원칙**:
1. **읽기 전용 필드 보호** (이메일, 역할, 가입일)
2. **비밀번호 변경은 Supabase Auth** 연동
3. **비밀번호 변경 후 자동 로그아웃**으로 보안 강화
