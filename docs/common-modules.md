# 공통 모듈 작업 계획

## 목차
1. [개요](#개요)
2. [Backend 공통 모듈](#backend-공통-모듈)
3. [Frontend 공통 모듈](#frontend-공통-모듈)
4. [테스트 환경 구축](#테스트-환경-구축)
5. [개발 우선순위](#개발-우선순위)

---

## 개요

### 프로젝트 정보
- **프로젝트명**: 대학교 사내 데이터 시각화 대시보드
- **기술 스택**: Django REST Framework + React + TypeScript + Supabase
- **아키텍처**: Layered Architecture with SOLID Principles
- **테스트 전략**: TDD (Test-Driven Development)

### 공통 모듈 설계 원칙
1. **최소 설계**: 오버엔지니어링 방지, 문서에 명시된 기능만 구현
2. **SOLID 원칙 준수**: 단일 책임, 개방-폐쇄, 의존성 역전 원칙 적용
3. **재사용성 극대화**: 모든 페이지에서 공통으로 사용될 로직만 포함
4. **병렬 개발 지원**: 페이지 단위 개발 시 코드 충돌 최소화
5. **테스트 용이성**: 모든 공통 모듈은 순수 함수 중심으로 설계

### 작업 범위
본 문서는 페이지 단위 개발을 시작하기 전에 완료해야 할 공통 모듈을 정의합니다. 다음 항목들은 **반드시 이 단계에서 구현**되어야 합니다:
- 인증 및 권한 관리
- API 통신 레이어
- 데이터 검증 및 변환
- 오류 처리
- 공통 UI 컴포넌트 (기본 레이아웃만)
- 테스트 환경 구축

---

## Backend 공통 모듈

### 1. 인증 및 권한 관리 (Authentication & Authorization)

#### 1.1 Supabase JWT 검증 미들웨어

**파일 위치**: `backend/infrastructure/authentication/supabase_auth.py`

**책임**:
- HTTP 요청에서 JWT 토큰 추출
- Supabase JWT Secret으로 토큰 서명 검증
- 토큰 만료 여부 확인
- 사용자 ID 및 역할 추출
- 요청 객체에 사용자 정보 첨부

**주요 함수**:
```python
class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request) -> Tuple[str, str]:
        """
        JWT 토큰을 검증하고 사용자 ID를 반환

        Returns:
            (user_id, token) 튜플

        Raises:
            AuthenticationFailed: 토큰이 유효하지 않은 경우
        """
        pass
```

**테스트 시나리오**:
1. 유효한 JWT 토큰 → 사용자 ID 추출 성공
2. 만료된 토큰 → AuthenticationFailed 예외 발생
3. 잘못된 서명 → AuthenticationFailed 예외 발생
4. Authorization 헤더 없음 → None 반환 (익명 사용자)
5. Bearer 형식 아님 → AuthenticationFailed 예외 발생

**의존성**:
- `PyJWT` 라이브러리
- `django.conf.settings` (SUPABASE_JWT_SECRET)

---

#### 1.2 권한 체크 데코레이터

**파일 위치**: `backend/infrastructure/authentication/permissions.py`

**책임**:
- View 레벨에서 사용자 권한 검증
- 관리자 전용 기능 보호
- 권한 부족 시 403 Forbidden 응답

**주요 함수**:
```python
def require_admin(view_func):
    """
    관리자 권한 필수 데코레이터

    Usage:
        @require_admin
        def upload_view(request):
            ...
    """
    pass

def require_authenticated(view_func):
    """
    로그인 필수 데코레이터
    """
    pass
```

**테스트 시나리오**:
1. 관리자 사용자 → 접근 허용
2. 일반 사용자 → 403 Forbidden
3. 비로그인 사용자 → 401 Unauthorized

---

### 2. 데이터 검증 (Data Validation)

#### 2.1 공통 Validator 클래스

**파일 위치**: `backend/apps/core/validators.py`

**책임**:
- 이메일 형식 검증
- 날짜 형식 검증 (YYYY-MM-DD)
- 숫자 범위 검증
- 필수 필드 검증
- 중복 데이터 검증

**주요 함수**:
```python
class CommonValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        """이메일 형식 검증"""
        pass

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """날짜 형식 검증 (YYYY-MM-DD)"""
        pass

    @staticmethod
    def validate_positive_number(value: Union[int, Decimal]) -> bool:
        """양수 검증"""
        pass

    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """필수 필드 검증 - 누락된 필드 목록 반환"""
        pass
```

**테스트 시나리오**:
1. 유효한 이메일 → True
2. 잘못된 이메일 형식 → False
3. 유효한 날짜 → True
4. 잘못된 날짜 형식 → False
5. 양수 → True
6. 음수 또는 0 → False
7. 모든 필수 필드 존재 → (True, [])
8. 일부 필드 누락 → (False, ['field1', 'field2'])

---

#### 2.2 엑셀 파일 검증기

**파일 위치**: `backend/apps/uploads/services/excel_validator.py`

**책임**:
- 엑셀 파일 형식 검증 (.xlsx, .xls)
- 파일 크기 검증 (최대 10MB)
- 헤더 컬럼 검증
- 데이터 타입별 필수 컬럼 검증

**주요 함수**:
```python
class ExcelFileValidator:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.xlsx', '.xls']

    REQUIRED_COLUMNS = {
        'performance': ['날짜', '금액', '카테고리'],
        'paper': ['제목', '저자', '게재일', '분야'],
        'student': ['학번', '이름', '학과', '학년'],
        'budget': ['항목', '금액', '카테고리'],
    }

    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """파일 확장자 검증"""
        pass

    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """파일 크기 검증"""
        pass

    @staticmethod
    def validate_required_columns(headers: List[str], data_type: str) -> Tuple[bool, List[str]]:
        """필수 컬럼 검증 - 누락된 컬럼 목록 반환"""
        pass
```

**테스트 시나리오**:
1. .xlsx 파일 → True
2. .csv 파일 → False
3. 5MB 파일 → True
4. 15MB 파일 → False
5. 실적 데이터 모든 컬럼 존재 → (True, [])
6. 실적 데이터 '금액' 컬럼 누락 → (False, ['금액'])

---

### 3. 데이터 변환 (Data Transformation)

#### 3.1 날짜 변환 유틸리티

**파일 위치**: `backend/apps/core/utils/date_utils.py`

**책임**:
- 문자열 → Date 객체 변환
- Date 객체 → ISO 8601 형식 변환
- 다양한 날짜 형식 파싱 (YYYY-MM-DD, YYYY/MM/DD)

**주요 함수**:
```python
class DateUtils:
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime.date]:
        """
        다양한 형식의 날짜 문자열을 date 객체로 변환

        지원 형식:
        - YYYY-MM-DD
        - YYYY/MM/DD
        - YYYY.MM.DD

        Returns:
            datetime.date 또는 None (파싱 실패 시)
        """
        pass

    @staticmethod
    def format_date(date_obj: datetime.date) -> str:
        """date 객체를 YYYY-MM-DD 형식으로 변환"""
        pass
```

**테스트 시나리오**:
1. '2024-11-01' → date(2024, 11, 1)
2. '2024/11/01' → date(2024, 11, 1)
3. '2024.11.01' → date(2024, 11, 1)
4. '작년' → None
5. date(2024, 11, 1) → '2024-11-01'

---

#### 3.2 숫자 변환 유틸리티

**파일 위치**: `backend/apps/core/utils/number_utils.py`

**책임**:
- 쉼표 포함 숫자 문자열 → Decimal 변환
- % 포함 문자열 → Decimal 변환
- 안전한 숫자 변환 (오류 시 None 반환)

**주요 함수**:
```python
class NumberUtils:
    @staticmethod
    def parse_decimal(value: str) -> Optional[Decimal]:
        """
        문자열을 Decimal로 변환

        지원 형식:
        - "1,200,000" → Decimal("1200000")
        - "85.5%" → Decimal("85.5")
        - "1200000" → Decimal("1200000")

        Returns:
            Decimal 또는 None (변환 실패 시)
        """
        pass

    @staticmethod
    def format_currency(amount: Decimal) -> str:
        """금액을 천 단위 쉼표 형식으로 변환"""
        pass
```

**테스트 시나리오**:
1. '1,200,000' → Decimal('1200000')
2. '85.5%' → Decimal('85.5')
3. '백만원' → None
4. Decimal('1200000') → '1,200,000'

---

### 4. 오류 처리 (Error Handling)

#### 4.1 커스텀 예외 클래스

**파일 위치**: `backend/apps/core/exceptions.py`

**책임**:
- 비즈니스 로직 예외 정의
- HTTP 상태 코드와 오류 메시지 매핑
- 사용자 친화적 오류 메시지 제공

**주요 클래스**:
```python
class BaseAPIException(Exception):
    """기본 API 예외 클래스"""
    status_code = 500
    default_message = "서버 오류가 발생했습니다"

    def __init__(self, message: str = None):
        self.message = message or self.default_message


class ValidationError(BaseAPIException):
    """데이터 검증 오류 (400)"""
    status_code = 400
    default_message = "입력 데이터가 유효하지 않습니다"


class AuthenticationError(BaseAPIException):
    """인증 오류 (401)"""
    status_code = 401
    default_message = "인증이 필요합니다"


class PermissionDeniedError(BaseAPIException):
    """권한 오류 (403)"""
    status_code = 403
    default_message = "접근 권한이 없습니다"


class ResourceNotFoundError(BaseAPIException):
    """리소스 없음 (404)"""
    status_code = 404
    default_message = "요청한 리소스를 찾을 수 없습니다"


class FileProcessingError(BaseAPIException):
    """파일 처리 오류 (400)"""
    status_code = 400
    default_message = "파일 처리 중 오류가 발생했습니다"
```

**테스트 시나리오**:
1. ValidationError("금액이 음수입니다") → status_code=400
2. AuthenticationError() → default_message 사용
3. 예외 메시지 커스터마이징 → 전달된 메시지 사용

---

#### 4.2 글로벌 예외 핸들러

**파일 위치**: `backend/infrastructure/middleware/exception_handler.py`

**책임**:
- 모든 예외를 일관된 JSON 형식으로 변환
- 로그 기록
- 프로덕션 환경에서 민감 정보 숨김

**주요 함수**:
```python
def exception_handler(exc, context):
    """
    DRF 글로벌 예외 핸들러

    Response 형식:
    {
        "error": "오류 메시지",
        "code": "ERROR_CODE",
        "details": {...}  # 개발 환경만
    }
    """
    pass
```

**테스트 시나리오**:
1. ValidationError 발생 → JSON 응답 생성
2. 예상치 못한 예외 → 500 응답 + 로그 기록
3. 개발 환경 → 스택 트레이스 포함
4. 프로덕션 환경 → 스택 트레이스 제외

---

### 5. 로깅 (Logging)

#### 5.1 구조화된 로거

**파일 위치**: `backend/infrastructure/logging/logger.py`

**책임**:
- 일관된 로그 형식
- 로그 레벨 관리 (DEBUG, INFO, WARNING, ERROR)
- 요청 ID 추적

**주요 함수**:
```python
class StructuredLogger:
    @staticmethod
    def log_api_request(method: str, path: str, user_id: str = None):
        """API 요청 로깅"""
        pass

    @staticmethod
    def log_error(error: Exception, context: Dict = None):
        """오류 로깅"""
        pass

    @staticmethod
    def log_file_upload(filename: str, data_type: str, rows: int, user_id: str):
        """파일 업로드 로깅"""
        pass
```

**테스트 시나리오**:
1. API 요청 로그 → JSON 형식으로 기록
2. 오류 로그 → 스택 트레이스 포함
3. 파일 업로드 로그 → 파일명, 데이터 유형, 행 수 기록

---

### 6. Database Repository 기본 클래스

#### 6.1 Base Repository

**파일 위치**: `backend/apps/core/repositories/base_repository.py`

**책임**:
- 공통 CRUD 메서드 제공
- ORM 쿼리 추상화
- 도메인 모델 ↔ ORM 모델 변환

**주요 클래스**:
```python
class BaseRepository(ABC):
    model = None  # 하위 클래스에서 ORM 모델 지정

    def get_by_id(self, id: int) -> Optional[object]:
        """ID로 단일 객체 조회"""
        pass

    def get_all(self, filters: Dict = None) -> List[object]:
        """전체 또는 필터링된 객체 목록 조회"""
        pass

    def create(self, data: Dict) -> object:
        """새 객체 생성"""
        pass

    def update(self, id: int, data: Dict) -> object:
        """객체 업데이트"""
        pass

    def delete(self, id: int) -> bool:
        """객체 삭제 (소프트 삭제)"""
        pass

    @abstractmethod
    def _to_domain(self, orm_obj) -> object:
        """ORM 모델 → 도메인 모델 변환"""
        pass

    @abstractmethod
    def _to_orm(self, domain_obj) -> object:
        """도메인 모델 → ORM 모델 변환"""
        pass
```

**테스트 시나리오**:
1. get_by_id(1) → 객체 반환
2. get_by_id(999) → None
3. create(data) → 새 객체 생성
4. update(id, data) → 객체 업데이트
5. delete(id) → is_deleted=True로 설정

---

## Frontend 공통 모듈

### 1. 인증 및 세션 관리

#### 1.1 Supabase 클라이언트 초기화

**파일 위치**: `frontend/src/infrastructure/external/supabase.ts`

**책임**:
- Supabase 클라이언트 싱글톤 생성
- 환경 변수에서 URL 및 Anon Key 로드

**주요 함수**:
```typescript
import { createClient, SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey)
```

**테스트 시나리오**:
1. 환경 변수 존재 → 클라이언트 생성 성공
2. 환경 변수 누락 → 에러 발생

---

#### 1.2 인증 서비스

**파일 위치**: `frontend/src/infrastructure/external/authService.ts`

**책임**:
- 로그인/로그아웃
- 토큰 갱신
- 현재 사용자 조회

**주요 함수**:
```typescript
export const authService = {
  async signIn(email: string, password: string): Promise<{ data: any; error: any }> {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    return { data, error }
  },

  async signOut(): Promise<{ error: any }> {
    const { error } = await supabase.auth.signOut()
    return { error }
  },

  async getCurrentUser(): Promise<any> {
    const { data: { user } } = await supabase.auth.getUser()
    return user
  },

  async getAccessToken(): Promise<string | null> {
    const { data: { session } } = await supabase.auth.getSession()
    return session?.access_token || null
  },
}
```

**테스트 시나리오** (MSW 모킹):
1. 유효한 자격증명 → 로그인 성공
2. 잘못된 자격증명 → 오류 반환
3. 로그아웃 → 세션 종료
4. getAccessToken → 토큰 반환
5. 세션 만료 → null 반환

---

#### 1.3 AuthContext

**파일 위치**: `frontend/src/application/contexts/AuthContext.tsx`

**책임**:
- 전역 인증 상태 관리
- 사용자 정보 저장
- 로그인/로그아웃 함수 제공

**주요 인터페이스**:
```typescript
interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

interface User {
  id: string
  email: string
  full_name: string
  role: 'admin' | 'user'
}
```

**테스트 시나리오**:
1. 초기 상태 → user=null, isAuthenticated=false
2. login 성공 → user 설정, isAuthenticated=true
3. logout → user=null, isAuthenticated=false
4. refreshUser → 최신 사용자 정보 로드

---

### 2. API 통신 레이어

#### 2.1 Axios 인스턴스

**파일 위치**: `frontend/src/services/api/client.ts`

**책임**:
- Axios 인스턴스 생성
- Request Interceptor: JWT 토큰 자동 추가
- Response Interceptor: 오류 처리 및 토큰 갱신

**주요 함수**:
```typescript
import axios, { AxiosInstance } from 'axios'
import { authService } from '@/infrastructure/external/authService'

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
})

// Request Interceptor: 토큰 자동 추가
apiClient.interceptors.request.use(async (config) => {
  const token = await authService.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response Interceptor: 401 오류 시 토큰 갱신 시도
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // 401 오류 → Refresh Token으로 갱신 시도
    // 갱신 실패 → 로그인 페이지로 리다이렉트
    return Promise.reject(error)
  }
)

export default apiClient
```

**테스트 시나리오** (MSW):
1. API 요청 → Authorization 헤더 자동 추가
2. 401 응답 → 토큰 갱신 후 재시도
3. 갱신 실패 → 로그인 페이지로 리다이렉트
4. 네트워크 오류 → 재시도 로직 실행

---

#### 2.2 타입 정의

**파일 위치**: `frontend/src/domain/models/`

**책임**:
- API 응답 타입 정의
- 도메인 모델 타입 정의
- Enum 정의

**주요 타입**:
```typescript
// User.ts
export interface User {
  id: string
  email: string
  full_name: string
  department: string | null
  role: 'admin' | 'user'
  created_at: string
  updated_at: string
}

// Dashboard.ts
export interface DashboardSummary {
  performance: PerformanceSummary
  papers: PaperSummary
  students: StudentSummary
  budget: BudgetSummary
}

export interface PerformanceSummary {
  total_amount: number
  growth_rate: number
  category_breakdown: CategoryBreakdown[]
}

// Upload.ts
export interface UploadResponse {
  id: number
  filename: string
  data_type: DataType
  rows_processed: number
  status: UploadStatus
  uploaded_at: string
}

export type DataType = 'performance' | 'paper' | 'student' | 'budget'
export type UploadStatus = 'pending' | 'processing' | 'success' | 'failed'
```

**테스트 시나리오**:
1. 타입 정의 → TypeScript 컴파일 성공
2. Enum 값 검증 → 허용된 값만 사용

---

### 3. 데이터 변환 (Data Transformation)

#### 3.1 차트 데이터 변환기

**파일 위치**: `frontend/src/services/transformers/chartTransformer.ts`

**책임**:
- Backend API 응답 → Recharts 형식 변환
- 날짜 포맷팅
- 숫자 포맷팅

**주요 함수**:
```typescript
export const chartTransformer = {
  /**
   * 막대 차트 데이터 변환
   * Backend: { category: string, value: number }[]
   * Recharts: { name: string, value: number }[]
   */
  transformBarChartData(data: any[]): any[] {
    return data.map(item => ({
      name: item.category || item.name,
      value: item.value || item.amount,
    }))
  },

  /**
   * 라인 차트 데이터 변환 (시계열)
   * Backend: { date: string, value: number }[]
   * Recharts: { date: string, value: number }[]
   */
  transformLineChartData(data: any[]): any[] {
    return data.map(item => ({
      date: formatDate(item.date),
      value: item.value,
    }))
  },

  /**
   * 파이 차트 데이터 변환
   * Backend: { name: string, value: number }[]
   * Recharts: { name: string, value: number }[]
   */
  transformPieChartData(data: any[]): any[] {
    return data
  },
}
```

**테스트 시나리오**:
1. 막대 차트 데이터 변환 → Recharts 형식 출력
2. 라인 차트 데이터 변환 → 날짜 포맷팅 확인
3. 빈 배열 → 빈 배열 반환

---

#### 3.2 날짜 포맷팅 유틸리티

**파일 위치**: `frontend/src/utils/formatters.ts`

**책임**:
- 날짜 포맷팅 (YYYY-MM-DD → 2024년 11월 1일)
- 숫자 포맷팅 (1000000 → 1,000,000)
- 퍼센트 포맷팅

**주요 함수**:
```typescript
export const formatters = {
  formatDate(dateStr: string): string {
    // "2024-11-01" → "2024년 11월 1일"
    const date = new Date(dateStr)
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
  },

  formatCurrency(amount: number): string {
    // 1000000 → "1,000,000원"
    return `${amount.toLocaleString('ko-KR')}원`
  },

  formatPercent(value: number): string {
    // 15.5 → "15.5%"
    return `${value.toFixed(1)}%`
  },

  formatCompactNumber(value: number): string {
    // 1200000 → "1.2M"
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`
    return value.toString()
  },
}
```

**테스트 시나리오**:
1. formatDate('2024-11-01') → '2024년 11월 1일'
2. formatCurrency(1000000) → '1,000,000원'
3. formatPercent(15.5) → '15.5%'
4. formatCompactNumber(1200000) → '1.2M'

---

### 4. 공통 UI 컴포넌트

#### 4.1 Layout 컴포넌트

**파일 위치**: `frontend/src/presentation/components/layout/`

**책임**:
- 공통 레이아웃 제공
- 네비게이션 바, 사이드바, 푸터

**주요 컴포넌트**:

##### AppLayout.tsx
```typescript
interface AppLayoutProps {
  children: React.ReactNode
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex' }}>
      <Navbar />
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
      <Footer />
    </Box>
  )
}
```

##### Navbar.tsx
```typescript
export const Navbar: React.FC = () => {
  const { user, logout } = useAuth()

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography variant="h6">대학교 데이터 대시보드</Typography>
        <Box sx={{ flexGrow: 1 }} />
        <IconButton onClick={logout}>
          <LogoutIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  )
}
```

**테스트 시나리오**:
1. AppLayout 렌더링 → Navbar, Sidebar, Footer 포함
2. Navbar 로그아웃 버튼 클릭 → logout 함수 호출
3. 사용자 이름 표시 → user.full_name 표시

---

#### 4.2 공통 Form 컴포넌트

**파일 위치**: `frontend/src/presentation/components/common/`

**책임**:
- 재사용 가능한 Input, Button 컴포넌트
- 일관된 스타일링

**주요 컴포넌트**:

##### Input.tsx
```typescript
interface InputProps {
  label: string
  type?: 'text' | 'email' | 'password' | 'number'
  value: string
  onChange: (value: string) => void
  error?: string
  required?: boolean
}

export const Input: React.FC<InputProps> = ({ label, type = 'text', value, onChange, error, required }) => {
  return (
    <TextField
      label={label}
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      error={!!error}
      helperText={error}
      required={required}
      fullWidth
    />
  )
}
```

##### Button.tsx
```typescript
interface ButtonProps {
  children: React.ReactNode
  variant?: 'contained' | 'outlined' | 'text'
  color?: 'primary' | 'secondary' | 'error'
  onClick: () => void
  disabled?: boolean
  loading?: boolean
}

export const Button: React.FC<ButtonProps> = ({ children, variant = 'contained', color = 'primary', onClick, disabled, loading }) => {
  return (
    <MuiButton
      variant={variant}
      color={color}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? <CircularProgress size={24} /> : children}
    </MuiButton>
  )
}
```

**테스트 시나리오**:
1. Input 렌더링 → label, value 표시
2. Input 변경 → onChange 함수 호출
3. Input 오류 → error 메시지 표시
4. Button 클릭 → onClick 함수 호출
5. Button loading → CircularProgress 표시

---

#### 4.3 로딩 및 오류 컴포넌트

**파일 위치**: `frontend/src/presentation/components/common/`

**책임**:
- 로딩 상태 표시
- 오류 메시지 표시
- 빈 상태 UI

**주요 컴포넌트**:

##### Loading.tsx
```typescript
interface LoadingProps {
  message?: string
}

export const Loading: React.FC<LoadingProps> = ({ message = '로딩 중...' }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', p: 3 }}>
      <CircularProgress />
      <Typography variant="body2" sx={{ mt: 2 }}>
        {message}
      </Typography>
    </Box>
  )
}
```

##### ErrorMessage.tsx
```typescript
interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <Alert severity="error" sx={{ mb: 2 }}>
      <AlertTitle>오류</AlertTitle>
      {message}
      {onRetry && (
        <Button size="small" onClick={onRetry} sx={{ mt: 1 }}>
          다시 시도
        </Button>
      )}
    </Alert>
  )
}
```

**테스트 시나리오**:
1. Loading 렌더링 → CircularProgress + 메시지 표시
2. ErrorMessage 렌더링 → Alert + 메시지 표시
3. onRetry 제공 → 다시 시도 버튼 표시

---

### 5. 라우팅 (Routing)

#### 5.1 Route 설정

**파일 위치**: `frontend/src/infrastructure/routing/routes.tsx`

**책임**:
- 모든 라우트 정의
- 권한별 라우트 분리

**주요 코드**:
```typescript
import { createBrowserRouter } from 'react-router-dom'
import { PrivateRoute } from './PrivateRoute'
import { PublicRoute } from './PublicRoute'

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <PublicRoute><LoginPage /></PublicRoute>,
  },
  {
    path: '/',
    element: <PrivateRoute><AppLayout /></PrivateRoute>,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'upload', element: <AdminRoute><UploadPage /></AdminRoute> },
      { path: 'data', element: <DataViewPage /> },
      { path: 'profile', element: <ProfilePage /> },
    ],
  },
])
```

**테스트 시나리오**:
1. '/login' 접근 → LoginPage 렌더링
2. '/' 접근 (로그인) → DashboardPage 렌더링
3. '/' 접근 (비로그인) → LoginPage로 리다이렉트
4. '/upload' 접근 (일반 사용자) → 403 페이지

---

#### 5.2 PrivateRoute

**파일 위치**: `frontend/src/infrastructure/routing/PrivateRoute.tsx`

**책임**:
- 로그인 사용자만 접근 허용
- 비로그인 시 로그인 페이지로 리다이렉트

**주요 코드**:
```typescript
interface PrivateRouteProps {
  children: React.ReactNode
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <Loading />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
```

**테스트 시나리오**:
1. 로그인 상태 → children 렌더링
2. 비로그인 상태 → /login으로 리다이렉트
3. 로딩 중 → Loading 컴포넌트 표시

---

#### 5.3 AdminRoute

**파일 위치**: `frontend/src/infrastructure/routing/AdminRoute.tsx`

**책임**:
- 관리자 권한 사용자만 접근 허용
- 일반 사용자는 403 페이지 표시

**주요 코드**:
```typescript
interface AdminRouteProps {
  children: React.ReactNode
}

export const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (user?.role !== 'admin') {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h5">접근 권한이 없습니다</Typography>
        <Typography variant="body1">관리자만 접근할 수 있습니다</Typography>
        <Button onClick={() => window.history.back()}>돌아가기</Button>
      </Box>
    )
  }

  return <>{children}</>
}
```

**테스트 시나리오**:
1. 관리자 사용자 → children 렌더링
2. 일반 사용자 → 403 메시지 표시
3. 비로그인 → /login으로 리다이렉트

---

## 테스트 환경 구축

### 1. Backend 테스트 환경

#### 1.1 테스트 설정

**파일 위치**: `backend/pytest.ini`

**내용**:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --tb=short
    --cov=apps
    --cov=infrastructure
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -n auto
    --maxfail=1
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (DB access)
    e2e: End-to-end tests (slow)
    slow: Slow running tests
```

---

#### 1.2 테스트 데이터베이스 설정

**파일 위치**: `backend/config/settings/test.py`

**내용**:
```python
from .base import *

DEBUG = False

# In-memory SQLite for unit tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()
```

---

#### 1.3 Pytest Fixtures

**파일 위치**: `backend/tests/conftest.py`

**내용**:
```python
import pytest
from django.test import Client
from apps.accounts.persistence.models import UserProfile

@pytest.fixture
def api_client():
    """Django test client"""
    return Client()

@pytest.fixture
def create_user(db):
    """사용자 생성 팩토리"""
    def _create_user(email='test@example.com', role='user'):
        return UserProfile.objects.create(
            email=email,
            full_name='테스트 사용자',
            role=role,
        )
    return _create_user

@pytest.fixture
def admin_user(create_user):
    """관리자 사용자"""
    return create_user(email='admin@example.com', role='admin')

@pytest.fixture
def authenticated_client(api_client, create_user):
    """인증된 클라이언트"""
    user = create_user()
    # JWT 토큰 생성 및 설정
    api_client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {generate_jwt(user.id)}'
    return api_client
```

---

#### 1.4 테스트 예시 (CommonValidator)

**파일 위치**: `backend/apps/core/tests/unit/test_validators.py`

**내용**:
```python
import pytest
from decimal import Decimal
from apps.core.validators import CommonValidator

class TestCommonValidator:
    """CommonValidator 단위 테스트"""

    # 이메일 검증
    def test_validate_email_returns_true_for_valid_email(self):
        # Arrange
        validator = CommonValidator()
        email = "test@example.com"

        # Act
        result = validator.validate_email(email)

        # Assert
        assert result is True

    def test_validate_email_returns_false_for_invalid_email(self):
        # Arrange
        validator = CommonValidator()
        email = "invalid-email"

        # Act
        result = validator.validate_email(email)

        # Assert
        assert result is False

    # 날짜 검증
    def test_validate_date_returns_true_for_valid_date(self):
        # Arrange
        validator = CommonValidator()
        date_str = "2024-11-01"

        # Act
        result = validator.validate_date(date_str)

        # Assert
        assert result is True

    def test_validate_date_returns_false_for_invalid_date(self):
        # Arrange
        validator = CommonValidator()
        date_str = "2024/13/01"

        # Act
        result = validator.validate_date(date_str)

        # Assert
        assert result is False

    # 양수 검증
    def test_validate_positive_number_returns_true_for_positive(self):
        # Arrange
        validator = CommonValidator()
        value = Decimal("100")

        # Act
        result = validator.validate_positive_number(value)

        # Assert
        assert result is True

    def test_validate_positive_number_returns_false_for_negative(self):
        # Arrange
        validator = CommonValidator()
        value = Decimal("-100")

        # Act
        result = validator.validate_positive_number(value)

        # Assert
        assert result is False

    # 필수 필드 검증
    def test_validate_required_fields_returns_true_when_all_present(self):
        # Arrange
        validator = CommonValidator()
        data = {"name": "홍길동", "email": "test@example.com"}
        required_fields = ["name", "email"]

        # Act
        is_valid, missing = validator.validate_required_fields(data, required_fields)

        # Assert
        assert is_valid is True
        assert missing == []

    def test_validate_required_fields_returns_false_when_missing(self):
        # Arrange
        validator = CommonValidator()
        data = {"name": "홍길동"}
        required_fields = ["name", "email", "phone"]

        # Act
        is_valid, missing = validator.validate_required_fields(data, required_fields)

        # Assert
        assert is_valid is False
        assert set(missing) == {"email", "phone"}
```

---

### 2. Frontend 테스트 환경

#### 2.1 Vitest 설정

**파일 위치**: `frontend/vitest.config.ts`

**내용**:
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
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
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

---

#### 2.2 테스트 셋업

**파일 위치**: `frontend/src/tests/setup.ts`

**내용**:
```typescript
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

// 각 테스트 후 자동 정리
afterEach(() => {
  cleanup()
})

// MSW 설정 (API 모킹)
import { setupServer } from 'msw/node'
import { handlers } from './mocks/handlers'

export const server = setupServer(...handlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

#### 2.3 MSW Handlers

**파일 위치**: `frontend/src/tests/mocks/handlers.ts`

**내용**:
```typescript
import { http, HttpResponse } from 'msw'

export const handlers = [
  // 로그인 API
  http.post('/api/auth/login', async ({ request }) => {
    const { email, password } = await request.json()

    if (email === 'admin@example.com' && password === 'password') {
      return HttpResponse.json({
        access_token: 'mock-jwt-token',
        user: {
          id: '1',
          email: 'admin@example.com',
          full_name: '관리자',
          role: 'admin',
        },
      })
    }

    return HttpResponse.json({ error: '잘못된 자격증명' }, { status: 401 })
  }),

  // 대시보드 API
  http.get('/api/dashboard/', () => {
    return HttpResponse.json({
      performance: {
        total_amount: 1200000,
        growth_rate: 15.5,
      },
      papers: {
        total_count: 45,
        scie_count: 20,
      },
    })
  }),
]
```

---

#### 2.4 테스트 예시 (chartTransformer)

**파일 위치**: `frontend/src/services/transformers/chartTransformer.test.ts`

**내용**:
```typescript
import { describe, it, expect } from 'vitest'
import { chartTransformer } from './chartTransformer'

describe('chartTransformer', () => {
  describe('transformBarChartData', () => {
    it('should transform backend data to Recharts format', () => {
      // Arrange
      const backendData = [
        { category: '연구비', value: 1000000 },
        { category: '특허료', value: 500000 },
      ]

      // Act
      const result = chartTransformer.transformBarChartData(backendData)

      // Assert
      expect(result).toEqual([
        { name: '연구비', value: 1000000 },
        { name: '특허료', value: 500000 },
      ])
    })

    it('should return empty array for empty input', () => {
      // Arrange
      const backendData: any[] = []

      // Act
      const result = chartTransformer.transformBarChartData(backendData)

      // Assert
      expect(result).toEqual([])
    })
  })

  describe('transformLineChartData', () => {
    it('should format date strings correctly', () => {
      // Arrange
      const backendData = [
        { date: '2024-01-01', value: 100 },
        { date: '2024-02-01', value: 150 },
      ]

      // Act
      const result = chartTransformer.transformLineChartData(backendData)

      // Assert
      expect(result[0].date).toBe('2024년 1월 1일')
      expect(result[1].date).toBe('2024년 2월 1일')
    })
  })
})
```

---

#### 2.5 컴포넌트 테스트 예시

**파일 위치**: `frontend/src/presentation/components/common/Input.test.tsx`

**내용**:
```typescript
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Input } from './Input'

describe('Input', () => {
  it('renders with label and value', () => {
    // Arrange & Act
    render(<Input label="이름" value="홍길동" onChange={() => {}} />)

    // Assert
    expect(screen.getByLabelText('이름')).toBeInTheDocument()
    expect(screen.getByDisplayValue('홍길동')).toBeInTheDocument()
  })

  it('calls onChange when value changes', () => {
    // Arrange
    const onChange = vi.fn()
    render(<Input label="이름" value="" onChange={onChange} />)

    // Act
    const input = screen.getByLabelText('이름')
    fireEvent.change(input, { target: { value: '김철수' } })

    // Assert
    expect(onChange).toHaveBeenCalledWith('김철수')
  })

  it('displays error message when provided', () => {
    // Arrange & Act
    render(<Input label="이메일" value="" onChange={() => {}} error="유효한 이메일을 입력하세요" />)

    // Assert
    expect(screen.getByText('유효한 이메일을 입력하세요')).toBeInTheDocument()
  })

  it('marks field as required', () => {
    // Arrange & Act
    render(<Input label="이름" value="" onChange={() => {}} required />)

    // Assert
    const input = screen.getByLabelText('이름')
    expect(input).toBeRequired()
  })
})
```

---

### 3. 테스트 실행 명령어

#### Backend
```bash
# 모든 테스트 실행
pytest

# 단위 테스트만 실행
pytest -m unit

# 통합 테스트만 실행
pytest -m integration

# 특정 파일 테스트
pytest apps/core/tests/unit/test_validators.py

# 커버리지 리포트 생성
pytest --cov=apps --cov-report=html
```

#### Frontend
```bash
# 모든 테스트 실행
npm run test

# Watch 모드
npm run test:watch

# UI 모드
npm run test:ui

# 커버리지 리포트
npm run test:coverage
```

---

### 4. TDD 워크플로우 체크리스트

#### 기능 개발 전 필수 체크리스트
- [ ] 구현할 시나리오 목록 작성 (주석으로)
- [ ] 가장 간단한 시나리오부터 시작
- [ ] 🔴 RED: 실패하는 테스트 작성
- [ ] 테스트 실행 → 올바른 이유로 실패하는지 확인
- [ ] 🟢 GREEN: 최소한의 코드로 테스트 통과
- [ ] 🔵 REFACTOR: 중복 제거, 네이밍 개선
- [ ] 모든 테스트 여전히 통과하는지 확인
- [ ] 작은 단위로 커밋
- [ ] 다음 시나리오로 반복

#### PR 머지 전 필수 체크리스트
- [ ] 모든 테스트 통과 (pytest / vitest)
- [ ] 커버리지 80% 이상
- [ ] 테스트 코드 품질 검토
- [ ] CI/CD 파이프라인 통과
- [ ] 코드 리뷰 완료

---

### 5. 모킹 최소화 전략

#### 모킹이 필요한 경우
1. **외부 API 호출** (Supabase Auth, Email Service)
   - 이유: 외부 서비스에 의존하면 테스트가 느려지고 불안정해짐
   - 도구: `responses` (Backend), `msw` (Frontend)

2. **시간 의존성** (현재 시각, 날짜 계산)
   - 이유: 테스트 결과가 실행 시점에 따라 달라짐
   - 도구: `freezegun`

3. **파일 시스템** (대용량 파일 업로드)
   - 이유: 테스트 속도 저하
   - 도구: `tmp_path` fixture

#### 모킹하지 않는 경우
1. **데이터베이스**
   - 대신 In-memory SQLite (unit) 또는 Test DB (integration) 사용
   - 이유: 실제 DB 동작과 차이가 생길 수 있음

2. **Repository Layer**
   - 대신 실제 Repository 구현 사용
   - 이유: Service 테스트에서 실제 데이터 흐름 검증 필요

3. **순수 함수**
   - 모킹 불필요 (입력 → 출력만 검증)

#### 효과
- 테스트가 실제 코드 동작을 정확히 반영
- 리팩토링 시 테스트가 깨지지 않음 (구현 세부사항 독립적)
- 테스트 유지보수 비용 감소

---

## 개발 우선순위

### Phase 1: 기본 인프라 (1주차)

#### Backend
1. Django 프로젝트 초기화
2. Supabase PostgreSQL 연결 설정
3. Supabase JWT 검증 미들웨어 구현 + 테스트
4. 커스텀 예외 클래스 구현 + 테스트
5. 글로벌 예외 핸들러 구현 + 테스트
6. 구조화된 로거 구현 + 테스트

#### Frontend
1. React + TypeScript + Vite 프로젝트 초기화
2. Supabase 클라이언트 초기화
3. 인증 서비스 구현 + 테스트
4. AuthContext 구현 + 테스트
5. Axios 인스턴스 + Interceptor 구현 + 테스트
6. 기본 타입 정의

#### 산출물
- Backend: 인증 미들웨어, 예외 처리, 로깅 완료
- Frontend: 인증 시스템, API 클라이언트 완료
- 테스트: 모든 공통 모듈 80% 이상 커버리지

---

### Phase 2: 데이터 검증 및 변환 (1주차)

#### Backend
1. CommonValidator 구현 + 테스트
2. ExcelFileValidator 구현 + 테스트
3. DateUtils 구현 + 테스트
4. NumberUtils 구현 + 테스트
5. BaseRepository 구현 + 테스트

#### Frontend
1. chartTransformer 구현 + 테스트
2. formatters 구현 + 테스트
3. validators 구현 + 테스트
4. 타입 정의 확장 (Dashboard, Upload 등)

#### 산출물
- Backend: 모든 Validator 및 Util 완료
- Frontend: 데이터 변환 로직 완료
- 테스트: 순수 함수 100% 커버리지

---

### Phase 3: UI 기본 컴포넌트 (1주차)

#### Frontend만
1. AppLayout 구현 + 테스트
2. Navbar 구현 + 테스트
3. Sidebar 구현 + 테스트
4. Footer 구현 + 테스트
5. Input 구현 + 테스트
6. Button 구현 + 테스트
7. Loading 구현 + 테스트
8. ErrorMessage 구현 + 테스트
9. 라우팅 설정 (PrivateRoute, AdminRoute)

#### 산출물
- Frontend: 모든 공통 UI 컴포넌트 완료
- Storybook (선택 사항): 컴포넌트 카탈로그
- 테스트: UI 컴포넌트 80% 이상 커버리지

---

### Phase 4: 통합 테스트 및 문서화 (1주차)

#### Backend
1. 통합 테스트 작성 (인증 플로우)
2. API 문서 생성 (Swagger)
3. README 작성

#### Frontend
1. E2E 테스트 작성 (Playwright)
2. 컴포넌트 문서화 (Storybook)
3. README 작성

#### 산출물
- Backend: Swagger API 문서
- Frontend: Storybook 컴포넌트 문서
- 테스트: 통합 테스트 및 E2E 테스트 완료
- README: 설치 및 실행 가이드

---

## 의존성 패키지

### Backend (requirements/base.txt)
```
Django>=5.0,<5.1
djangorestframework>=3.14
django-cors-headers>=4.3
psycopg2-binary>=2.9
python-decouple>=3.8
openpyxl>=3.1
pandas>=2.1
Pillow>=10.1
gunicorn>=21.2
whitenoise>=6.6
supabase>=2.0
PyJWT>=2.8
```

### Backend (requirements/test.txt)
```
pytest>=7.4.0
pytest-django>=4.5.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-xdist>=3.3.0
factory-boy>=3.3.0
faker>=19.0.0
freezegun>=1.2.0
responses>=0.23.0
```

### Frontend (package.json)
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
  },
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/user-event": "^14.5.0",
    "@vitest/ui": "^0.34.0",
    "vitest": "^0.34.0",
    "jsdom": "^22.1.0",
    "msw": "^2.0.0",
    "@playwright/test": "^1.38.0",
    "c8": "^8.0.0"
  }
}
```

---

## 코드 충돌 방지 전략

### 1. 명확한 경계 설정
- Backend: 각 앱은 독립적인 디렉토리 구조
- Frontend: 기능별 디렉토리 분리 (presentation, application, domain, services)
- 공통 모듈: `core/`, `infrastructure/`, `common/` 에만 위치

### 2. 명명 규칙
- Backend 클래스: `PascalCase` (예: `CommonValidator`)
- Backend 함수: `snake_case` (예: `validate_email`)
- Frontend 컴포넌트: `PascalCase` (예: `AppLayout`)
- Frontend 함수: `camelCase` (예: `formatDate`)
- 파일명: 클래스명과 동일 (예: `CommonValidator.py`, `AppLayout.tsx`)

### 3. Import 경로 고정
- Backend: 절대 경로 사용 (`from apps.core.validators import CommonValidator`)
- Frontend: `@/` alias 사용 (`import { Input } from '@/presentation/components/common/Input'`)

### 4. Git 브랜치 전략
- `main`: 프로덕션 배포
- `develop`: 개발 통합
- `feature/common-modules`: 공통 모듈 개발
- `feature/page-{name}`: 페이지 단위 개발

---

## 요약

본 문서는 페이지 단위 개발을 시작하기 전에 완료해야 할 **모든 공통 모듈**을 정의합니다.

### Backend 공통 모듈 (11개)
1. Supabase JWT 검증 미들웨어
2. 권한 체크 데코레이터
3. CommonValidator
4. ExcelFileValidator
5. DateUtils
6. NumberUtils
7. 커스텀 예외 클래스
8. 글로벌 예외 핸들러
9. 구조화된 로거
10. BaseRepository
11. Middleware 설정

### Frontend 공통 모듈 (14개)
1. Supabase 클라이언트 초기화
2. 인증 서비스
3. AuthContext
4. Axios 인스턴스 + Interceptor
5. 타입 정의
6. chartTransformer
7. formatters
8. AppLayout
9. Navbar
10. Sidebar
11. Footer
12. Input
13. Button
14. Loading
15. ErrorMessage
16. PrivateRoute
17. AdminRoute

### 테스트 환경
- Backend: pytest + django.test + factory-boy
- Frontend: Vitest + React Testing Library + MSW + Playwright
- 모킹 최소화 전략 적용
- TDD Red-Green-Refactor 사이클 준수

### 개발 순서
1. Phase 1: 기본 인프라 (인증, API 클라이언트)
2. Phase 2: 데이터 검증 및 변환
3. Phase 3: UI 기본 컴포넌트
4. Phase 4: 통합 테스트 및 문서화

모든 공통 모듈이 완료되면 페이지 단위 개발을 **병렬로** 진행할 수 있습니다.
