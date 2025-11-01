# 기술 스택 추천

## 프로젝트 개요
대학교 사내 데이터 시각화 대시보드 개발

## 추천 기술 스택

### Frontend
**React 18+ with TypeScript**
- 판단 근거:
  1. AI 친화성: 가장 인기있고 AI가 잘 구현하는 라이브러리 (GitHub Stars: 220k+)
  2. 유지보수: Meta(Facebook)에서 활발히 관리, 대규모 커뮤니티
  3. 안정성: 하위 호환성 우수, Breaking Change 최소화 정책

**데이터 시각화: Recharts or Chart.js**
- Recharts 추천 이유:
  1. React 전용 차트 라이브러리로 통합 용이
  2. 직관적인 선언형 API
  3. 안정적이고 지속적으로 유지보수됨
- Chart.js 대안:
  1. 더 범용적이고 검증된 라이브러리
  2. react-chartjs-2로 React 통합 가능

**UI 프레임워크: Material-UI (MUI) 또는 Ant Design**
- MUI 추천 이유:
  1. Google Material Design 기반, 전문적인 UI
  2. MIT 라이선스, 활발한 유지보수
  3. 대시보드 구축에 최적화된 컴포넌트 제공
  4. TypeScript 완벽 지원

### Backend
**Django REST Framework (Python)**
- 판단 근거:
  1. AI 친화성: Python은 AI가 가장 잘 구현하는 언어, DRF는 표준 REST API 프레임워크
  2. 유지보수: Django Software Foundation 관리, 20년 이상 검증됨
  3. 안정성: 매우 성숙한 프레임워크, 하위 호환성 우수
  4. 생산성: Admin 패널 자동 생성, ORM 내장, 인증/권한 시스템 기본 제공
  5. 데이터 처리: Python의 pandas, openpyxl로 엑셀 처리에 최적화

### 데이터베이스
**Supabase (PostgreSQL 기반)**
- 판단 근거:
  1. PostgreSQL 기반의 오픈소스 BaaS (Backend as a Service)
  2. 관리형 데이터베이스로 인프라 관리 불필요
  3. 실시간 기능, 자동 백업, Row Level Security 제공
  4. 무료 티어 제공으로 교육기관에 적합
  5. RESTful API 자동 생성 (선택적 사용 가능)
  6. Railway와 원활한 연동

**ORM: Django ORM**
- Django 내장 ORM 사용
- Python 기반으로 직관적인 쿼리 작성
- 마이그레이션 자동 관리
- psycopg2를 통한 PostgreSQL 연결

### 파일 처리
**openpyxl 또는 pandas (Python)**
- openpyxl 추천 이유:
  1. Python에서 가장 널리 사용되는 엑셀 처리 라이브러리
  2. .xlsx 파일 읽기/쓰기 완벽 지원
  3. 안정적이고 활발히 유지보수됨
- pandas 대안:
  1. 데이터 분석 및 변환에 최적화
  2. 엑셀 데이터를 DataFrame으로 쉽게 변환
  3. 대용량 데이터 처리에 강력함

### 인증
**Supabase Auth**
- 판단 근거:
  1. Supabase 내장 인증 시스템으로 별도 구현 불필요
  2. 이메일/비밀번호, OAuth, Magic Link 등 다양한 인증 방식 지원
  3. JWT 토큰 자동 발급 및 관리
  4. Row Level Security(RLS)와 완벽하게 통합
  5. 사용자 관리 UI 제공 (Supabase Dashboard)
  6. 프론트엔드에서 @supabase/supabase-js로 간편하게 연동

- 아키텍처:
  - Frontend에서 Supabase Auth로 직접 인증 처리
  - 백엔드는 Supabase JWT 토큰 검증만 수행
  - 사용자 정보는 Supabase의 auth.users 테이블에 자동 저장
  - 추가 프로필 정보는 public.profiles 테이블에 별도 관리

### 파일 저장 및 미디어
**Django FileField/ImageField**
- Django 내장 파일 처리 기능
- MEDIA_ROOT 설정으로 업로드 파일 관리
- Railway에서 임시 파일 저장 지원 (또는 S3/Cloudinary 연동 가능)

### 개발 도구
- **Python 3.11+**: 최신 성능 개선 및 타입 힌팅 지원
- **Poetry 또는 pip-tools**: 의존성 관리
- **Black + Flake8**: 코드 포매팅 및 린팅
- **pytest**: 테스트 프레임워크
- **django-extensions**: 개발 편의성 도구
- **django-cors-headers**: CORS 설정 (프론트엔드 연동용)

### Frontend 빌드 도구
- **Vite**: 빠른 개발 서버 및 빌드
- **TypeScript**: 타입 안정성
- **ESLint + Prettier**: 코드 품질 관리

## 최종 추천 아키텍처 (확정)

### 분리형 아키텍처 - Django REST Framework + React
```
Backend:
  - Django 5.x + Django REST Framework
  - Python 3.11+
  - Django ORM
  - openpyxl + pandas (엑셀 처리)
  - django-cors-headers
  - supabase-py (Supabase 클라이언트, JWT 검증용)

Frontend:
  - React 18 + TypeScript + Vite
  - Material-UI (MUI)
  - Recharts (데이터 시각화)
  - @supabase/supabase-js (Supabase 클라이언트 & Auth)
  - React Router (라우팅)

Database & Auth:
  - Supabase (PostgreSQL 관리형 + Auth)
  - psycopg2-binary (PostgreSQL 드라이버)

배포:
  - Backend: Railway
  - Frontend: Vercel 또는 Railway
  - Database & Auth: Supabase (클라우드 호스팅)
```

## 추천 이유 요약
1. **AI 친화성**: Python과 Django는 AI가 가장 잘 구현하는 스택, 광범위한 예제와 문서
2. **안정성**: Django Software Foundation 관리, 20년 이상 검증된 프레임워크
3. **하위 호환성**: Django의 안정적인 LTS 릴리스, Breaking Change 최소화
4. **교육기관 적합성**: 오픈소스, MIT 라이선스, 전세계 대학에서 사용
5. **개발 효율성**:
   - Django Admin 자동 생성으로 데이터 관리 용이
   - ORM으로 SQL 작성 최소화
   - DRF의 Serializer로 API 빠르게 구축
   - Python의 pandas/openpyxl로 엑셀 처리 간편
6. **배포 편의성**: Railway에서 Python 환경 완벽 지원, Supabase 연동 간단
7. **비용 효율성**: 모두 무료 티어 제공 (Railway, Supabase, Vercel)

## 프로젝트 구조 제안

### Backend (Django) 디렉토리 구조:
```
backend/
├── config/                  # Django 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── dashboard/          # 대시보드 앱
│   │   ├── models.py       # 데이터 모델 (실적, 논문, 학생, 예산 등)
│   │   ├── serializers.py  # DRF Serializer
│   │   ├── views.py        # API Views
│   │   ├── urls.py
│   │   └── services/       # 비즈니스 로직
│   │       └── excel_parser.py  # 엑셀 파싱 로직
│   ├── accounts/           # 사용자 프로필 앱
│   │   ├── models.py       # 추가 프로필 정보 모델
│   │   ├── serializers.py
│   │   └── views.py        # 프로필 조회/수정 API
│   └── uploads/            # 파일 업로드 앱
│       ├── models.py
│       ├── views.py
│       └── utils.py
├── middleware/
│   └── supabase_auth.py   # Supabase JWT 검증 미들웨어
├── media/                  # 업로드된 파일
├── requirements.txt        # Python 의존성
├── manage.py
└── railway.toml           # Railway 배포 설정

```

### Frontend (React) 디렉토리 구조:
```
frontend/
├── src/
│   ├── components/         # React 컴포넌트
│   │   ├── charts/         # 차트 컴포넌트
│   │   │   ├── BarChart.tsx
│   │   │   ├── LineChart.tsx
│   │   │   └── PieChart.tsx
│   │   ├── layout/         # 레이아웃 컴포넌트
│   │   │   ├── Navbar.tsx
│   │   │   └── Sidebar.tsx
│   │   └── common/         # 공통 컴포넌트
│   ├── pages/              # 페이지 컴포넌트
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Upload.tsx
│   │   └── DataView.tsx
│   ├── lib/                # 라이브러리 설정
│   │   └── supabase.ts     # Supabase 클라이언트 초기화
│   ├── services/           # API 서비스
│   │   ├── api.ts          # Axios 인스턴스 (JWT 인터셉터)
│   │   └── dashboard.ts    # 대시보드 API
│   ├── contexts/           # React Context
│   │   └── AuthContext.tsx # Supabase Auth 상태 관리
│   ├── types/              # TypeScript 타입
│   ├── hooks/              # Custom Hooks
│   ├── utils/              # 유틸리티 함수
│   └── App.tsx
├── package.json
└── vite.config.ts
```

## 핵심 Python 패키지 목록
```txt
Django>=5.0,<5.1
djangorestframework>=3.14
django-cors-headers>=4.3
psycopg2-binary>=2.9
python-decouple>=3.8
openpyxl>=3.1
pandas>=2.1
Pillow>=10.1
gunicorn>=21.2  # Railway 배포용
whitenoise>=6.6  # 정적 파일 서빙
supabase>=2.0  # Supabase 클라이언트 (JWT 검증용)
PyJWT>=2.8  # JWT 토큰 검증
```

## 핵심 Frontend 패키지 목록
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@mui/material": "^5.14.0",
    "@mui/icons-material": "^5.14.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "recharts": "^2.10.0",
    "@supabase/supabase-js": "^2.38.0",
    "axios": "^1.6.0"
  }
}
```

## Railway 배포 설정
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn config.wsgi:application"
healthcheckPath = "/api/health/"
restartPolicyType = "ON_FAILURE"

[env]
DJANGO_SETTINGS_MODULE = "config.settings"
```

## Supabase 연결 설정

### Backend (Django settings.py)
```python
from decouple import config

# 데이터베이스 연결 (Supabase PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),  # Supabase 호스트
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Supabase 설정 (JWT 검증용)
SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_KEY = config('SUPABASE_ANON_KEY')  # 또는 SERVICE_ROLE_KEY
SUPABASE_JWT_SECRET = config('SUPABASE_JWT_SECRET')
```

### Backend JWT 검증 미들웨어 예시
```python
# middleware/supabase_auth.py
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256'],
                audience='authenticated'
            )
            # payload에서 user 정보 추출
            user_id = payload.get('sub')
            return (user_id, token)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
```

### Frontend (Supabase 클라이언트 설정)
```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 인증 헬퍼 함수
export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })
  return { data, error }
}

export const signUp = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  })
  return { data, error }
}

export const signOut = async () => {
  const { error } = await supabase.auth.signOut()
  return { error }
}

export const getCurrentUser = async () => {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

// 토큰 가져오기 (백엔드 API 호출 시 사용)
export const getAccessToken = async () => {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token
}
```

### Frontend Axios 인터셉터 (자동 토큰 포함)
```typescript
// src/services/api.ts
import axios from 'axios'
import { getAccessToken } from '../lib/supabase'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
})

// 요청 인터셉터: 모든 요청에 Supabase JWT 토큰 추가
api.interceptors.request.use(async (config) => {
  const token = await getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
```

## 인증 플로우

1. **회원가입/로그인**:
   - Frontend에서 `@supabase/supabase-js`로 Supabase Auth 직접 호출
   - 성공 시 JWT 토큰 자동 발급 (localStorage에 저장)

2. **백엔드 API 호출**:
   - Frontend에서 Axios 요청 시 Authorization 헤더에 Supabase JWT 포함
   - Backend에서 JWT 검증 후 사용자 식별

3. **사용자 프로필**:
   - Supabase의 `auth.users` 테이블에 기본 정보 자동 저장
   - 추가 정보는 `public.profiles` 테이블에 저장 (Django ORM으로 관리)

4. **권한 관리**:
   - Supabase RLS(Row Level Security)로 데이터베이스 레벨 권한 설정
   - Django에서도 추가 권한 검증 가능

---

## 테스트 환경 구축 전략

### TDD 원칙 준수
프로젝트는 `docs/rules/tdd.md`에 명시된 **Red → Green → Refactor** 사이클을 엄격히 따릅니다.

### 테스트 피라미드 전략

```
        /\
       /  \  E2E Tests (10%)
      /----\  - 실제 사용자 시나리오
     /      \ - Playwright (Frontend)
    /--------\ - pytest E2E (Backend)
   /          \
  / Integration\ Tests (20%)
 /    Tests     \ - API Endpoints
/--------------\ - 데이터 흐름 검증
/              \
/  Unit Tests   \ (70%)
/   (Pure Logic) \ - Service Layer
/------------------\ - Repository Layer
     Fast & Many      - Utility Functions
```

### Backend 테스트 구조

#### 1. Unit Tests (70%) - 순수 함수 중심
**위치**: `apps/{app_name}/tests/unit/`

**전략**:
- **Service Layer**: Mock Repository를 사용한 비즈니스 로직 테스트
- **Repository Layer**: In-memory SQLite DB 사용 (모킹 최소화)
- **Utility Functions**: 완전 독립적인 순수 함수 테스트

**예시**:
```python
# apps/dashboard/tests/unit/test_metric_calculator.py
from apps.dashboard.services.metric_calculator import MetricCalculator
from apps.dashboard.domain.models import PerformanceData
from decimal import Decimal

class TestMetricCalculator:
    """순수 함수 테스트 - 외부 의존성 없음"""

    def test_calculate_growth_rate_returns_correct_percentage(self):
        # Arrange
        calculator = MetricCalculator()
        previous = Decimal("100")
        current = Decimal("150")

        # Act
        growth_rate = calculator.calculate_growth_rate(previous, current)

        # Assert
        assert growth_rate == Decimal("50.0")

    def test_calculate_growth_rate_handles_zero_previous(self):
        # Arrange
        calculator = MetricCalculator()

        # Act & Assert
        with pytest.raises(ValueError, match="이전 값은 0이 될 수 없습니다"):
            calculator.calculate_growth_rate(Decimal("0"), Decimal("100"))
```

**모킹 최소화 원칙**:
- Repository는 실제 In-memory DB를 사용하여 테스트
- 외부 API 호출만 모킹 (Supabase Auth, Email Service 등)

```python
# apps/uploads/tests/unit/test_excel_parser.py
import pytest
from apps.uploads.services.excel_parser import PerformanceExcelParser

class TestPerformanceExcelParser:
    """파일 파싱 순수 로직 테스트"""

    def test_parse_valid_excel_returns_correct_data_structure(self, tmp_path):
        # Arrange
        parser = PerformanceExcelParser()
        excel_file = tmp_path / "test.xlsx"
        # 실제 엑셀 파일 생성 (openpyxl 사용)
        create_test_excel(excel_file, [
            {"department": "컴퓨터공학과", "amount": 1000},
        ])

        # Act
        result = parser.parse(str(excel_file))

        # Assert
        assert len(result) == 1
        assert result[0].department == "컴퓨터공학과"
        assert result[0].amount == Decimal("1000")
```

#### 2. Integration Tests (20%)
**위치**: `apps/{app_name}/tests/integration/`

**전략**:
- Django TestClient 사용
- 실제 Test Database 사용 (PostgreSQL)
- API Request → Service → Repository → DB 전체 흐름 검증

```python
# apps/dashboard/tests/integration/test_dashboard_api.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestDashboardAPI:
    """API Endpoint 통합 테스트"""

    def test_get_dashboard_returns_200_with_valid_data(self, authenticated_client):
        # Arrange
        # 실제 DB에 테스트 데이터 생성
        PerformanceModel.objects.create(
            department="컴퓨터공학과",
            amount=1000,
            date="2024-01-01"
        )

        # Act
        response = authenticated_client.get('/api/dashboard/')

        # Assert
        assert response.status_code == 200
        assert 'summary' in response.json()
        assert response.json()['summary']['total_performance'] == 1000
```

#### 3. E2E Tests (10%)
**위치**: `tests/e2e/`

**전략**:
- pytest + Playwright (또는 Selenium)
- 실제 브라우저 시뮬레이션
- 주요 사용자 플로우 검증

```python
# tests/e2e/test_excel_upload_flow.py
import pytest
from playwright.sync_api import Page

@pytest.mark.e2e
def test_user_can_upload_excel_and_view_dashboard(page: Page):
    """E2E: 엑셀 업로드 → 대시보드 확인"""

    # 1. 로그인
    page.goto("http://localhost:3000/login")
    page.fill('input[name="email"]', "test@example.com")
    page.fill('input[name="password"]', "password123")
    page.click('button[type="submit"]')

    # 2. 엑셀 업로드
    page.goto("http://localhost:3000/upload")
    page.set_input_files('input[type="file"]', 'test_data.xlsx')
    page.click('button:has-text("업로드")')

    # 3. 성공 메시지 확인
    assert page.locator('text=업로드 완료').is_visible()

    # 4. 대시보드에서 데이터 확인
    page.goto("http://localhost:3000/dashboard")
    assert page.locator('text=컴퓨터공학과').is_visible()
```

### Frontend 테스트 구조

#### 1. Component Unit Tests (70%)
**도구**: Vitest + React Testing Library

**전략**:
- Props 기반 렌더링 테스트
- 사용자 상호작용 테스트
- API 호출은 MSW로 모킹

```typescript
// src/presentation/components/charts/BarChart.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import BarChart from './BarChart'

describe('BarChart', () => {
  it('renders chart with valid data', () => {
    // Arrange
    const mockData = [
      { name: '컴퓨터공학과', value: 1000 },
      { name: '전자공학과', value: 800 },
    ]

    // Act
    render(<BarChart data={mockData} title="학과별 실적" />)

    // Assert
    expect(screen.getByText('학과별 실적')).toBeInTheDocument()
    expect(screen.getByText('컴퓨터공학과')).toBeInTheDocument()
  })

  it('shows "no data" message when data is empty', () => {
    // Arrange
    const emptyData: any[] = []

    // Act
    render(<BarChart data={emptyData} title="학과별 실적" />)

    // Assert
    expect(screen.getByText(/데이터가 없습니다/i)).toBeInTheDocument()
  })
})
```

#### 2. Hook Tests
```typescript
// src/application/hooks/useAuth.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { useAuth } from './useAuth'
import { supabase } from '@/infrastructure/external/supabase'

vi.mock('@/infrastructure/external/supabase')

describe('useAuth', () => {
  it('returns user when authenticated', async () => {
    // Arrange
    vi.mocked(supabase.auth.getUser).mockResolvedValue({
      data: { user: { id: '123', email: 'test@example.com' } },
      error: null,
    })

    // Act
    const { result } = renderHook(() => useAuth())

    // Assert
    await waitFor(() => {
      expect(result.current.user).toEqual({
        id: '123',
        email: 'test@example.com',
      })
    })
  })
})
```

#### 3. Integration Tests (20%)
**도구**: MSW (Mock Service Worker)

```typescript
// src/services/api/dashboardApi.test.ts
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { getDashboard } from './dashboardApi'

const server = setupServer(
  http.get('/api/dashboard/', () => {
    return HttpResponse.json({
      summary: { total_performance: 1000 },
    })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('dashboardApi', () => {
  it('fetches dashboard data successfully', async () => {
    // Act
    const data = await getDashboard()

    // Assert
    expect(data.summary.total_performance).toBe(1000)
  })
})
```

#### 4. E2E Tests (10%)
**도구**: Playwright

```typescript
// src/tests/e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test'

test('user can view dashboard after login', async ({ page }) => {
  // 1. 로그인
  await page.goto('http://localhost:5173/login')
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  // 2. 대시보드 확인
  await expect(page).toHaveURL(/.*dashboard/)
  await expect(page.locator('h1')).toContainText('대시보드')

  // 3. 차트 렌더링 확인
  await expect(page.locator('[role="img"][aria-label="chart"]')).toBeVisible()
})
```

### 테스트 도구 및 패키지

#### Backend 테스트 패키지
```txt
# requirements/test.txt
pytest>=7.4.0
pytest-django>=4.5.0
pytest-cov>=4.1.0              # 커버리지 측정
pytest-mock>=3.11.0            # Mock 헬퍼
pytest-xdist>=3.3.0            # 병렬 테스트 실행
factory-boy>=3.3.0             # 테스트 데이터 팩토리
faker>=19.0.0                  # 가짜 데이터 생성
freezegun>=1.2.0               # 시간 Mock
responses>=0.23.0              # HTTP Mock
playwright>=1.38.0             # E2E 테스트
```

#### Frontend 테스트 패키지
```json
{
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/user-event": "^14.5.0",
    "@vitest/ui": "^0.34.0",
    "vitest": "^0.34.0",
    "jsdom": "^22.1.0",
    "msw": "^1.3.0",
    "@playwright/test": "^1.38.0",
    "c8": "^8.0.0"
  }
}
```

### 설정 파일

#### pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --tb=short
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -n auto
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (DB access)
    e2e: End-to-end tests (slow)
    slow: Slow running tests
```

#### vitest.config.ts
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/tests/',
      ],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

#### playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './src/tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
})
```

### CI/CD 통합

#### .github/workflows/test.yml
```yaml
name: Run Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements/test.txt

      - name: Run unit tests
        run: |
          cd backend
          pytest -m unit --cov=apps --cov-report=xml

      - name: Run integration tests
        run: |
          cd backend
          pytest -m integration --cov=apps --cov-append --cov-report=xml
        env:
          DB_HOST: localhost
          DB_PORT: 5432
          DB_NAME: test_db
          DB_USER: postgres
          DB_PASSWORD: postgres

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run unit tests
        run: |
          cd frontend
          npm run test:coverage

      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright install --with-deps
          npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
```

### TDD 워크플로우 체크리스트

```markdown
## 기능 개발 전 필수 체크리스트

- [ ] 구현할 시나리오 목록 작성 (주석으로)
- [ ] 가장 간단한 시나리오부터 시작
- [ ] 🔴 RED: 실패하는 테스트 작성
- [ ] 테스트 실행 → 올바른 이유로 실패하는지 확인
- [ ] 🟢 GREEN: 최소한의 코드로 테스트 통과
- [ ] 🔵 REFACTOR: 중복 제거, 네이밍 개선
- [ ] 모든 테스트 여전히 통과하는지 확인
- [ ] 작은 단위로 커밋
- [ ] 다음 시나리오로 반복

## PR 머지 전 필수 체크리스트

- [ ] 모든 테스트 통과 (pytest / vitest)
- [ ] 커버리지 80% 이상
- [ ] 테스트 코드 품질 검토
- [ ] CI/CD 파이프라인 통과
- [ ] E2E 테스트 통과
```

### 모킹 최소화 전략 및 이유

**원칙**: 가능한 실제 구현을 사용하고, 불가피한 경우만 모킹

**모킹이 필요한 경우**:
1. **외부 API 호출** (Supabase Auth, Email Service)
   - 이유: 외부 서비스에 의존하면 테스트가 느려지고 불안정해짐
   - 도구: `responses` (Backend), `msw` (Frontend)

2. **시간 의존성** (현재 시각, 날짜 계산)
   - 이유: 테스트 결과가 실행 시점에 따라 달라짐
   - 도구: `freezegun`

3. **파일 시스템** (대용량 파일 업로드)
   - 이유: 테스트 속도 저하
   - 도구: `tmp_path` fixture

**모킹하지 않는 경우**:
1. **데이터베이스**
   - 대신 In-memory SQLite (unit) 또는 Test DB (integration) 사용
   - 이유: 실제 DB 동작과 차이가 생길 수 있음

2. **Repository Layer**
   - 대신 실제 Repository 구현 사용
   - 이유: Service 테스트에서 실제 데이터 흐름 검증 필요

3. **순수 함수**
   - 모킹 불필요 (입력 → 출력만 검증)

**효과**:
- 테스트가 실제 코드 동작을 정확히 반영
- 리팩토링 시 테스트가 깨지지 않음 (구현 세부사항 독립적)
- 테스트 유지보수 비용 감소

---
