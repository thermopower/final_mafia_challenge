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
