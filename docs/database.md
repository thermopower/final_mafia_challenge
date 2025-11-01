# 데이터베이스 설계 문서

## 목차
1. [개요](#개요)
2. [간략한 데이터 플로우](#간략한-데이터-플로우)
3. [ERD (Entity Relationship Diagram)](#erd-entity-relationship-diagram)
4. [테이블 상세 스키마](#테이블-상세-스키마)
5. [데이터 관계 및 외래키](#데이터-관계-및-외래키)
6. [인덱스 및 성능 최적화 전략](#인덱스-및-성능-최적화-전략)
7. [데이터 흐름도 (CRUD 작업)](#데이터-흐름도-crud-작업)
8. [마이그레이션 전략](#마이그레이션-전략)

---

## 개요

### 프로젝트 정보
- **프로젝트명**: 대학교 사내 데이터 시각화 대시보드
- **기술 스택**: Django REST Framework + React + Supabase (PostgreSQL)
- **데이터베이스**: PostgreSQL 15+ (Supabase 관리형)
- **ORM**: Django ORM

### 설계 원칙
- **정규화**: 제3정규형(3NF) 준수
- **확장성**: 향후 추가 데이터 유형을 쉽게 통합 가능
- **성능**: 적절한 인덱스와 쿼리 최적화
- **감사 추적**: 모든 데이터 변경 이력 추적 (created_at, updated_at)
- **소프트 삭제**: 데이터 복구 가능성을 위한 is_deleted 플래그

---

## 간략한 데이터 플로우

### 1. 인증 플로우
```
[사용자] → [Supabase Auth] → [JWT 토큰]
    ↓
[Backend AuthMiddleware] → JWT 검증 → [user_profiles 테이블]
    ↓
[사용자 정보 및 역할 추출]
```

### 2. Excel 업로드 플로우
```
[Excel 파일] → [Frontend Upload]
    ↓
[Backend UploadView] → [FileProcessorService]
    ↓
[ExcelParser] → 데이터 파싱
    ↓
[DataValidator] → 데이터 검증
    ↓
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ performances │    papers    │   students   │   budgets    │
└──────────────┴──────────────┴──────────────┴──────────────┘
    ↓
[uploaded_files] ← 업로드 메타데이터 저장
```

### 3. 대시보드 조회 플로우
```
[사용자] → [Dashboard 요청] → [DashboardService]
    ↓
병렬 조회:
┌─────────────────────────────────────────────┐
│ PerformanceRepository.get_summary()         │
│ PaperRepository.get_count_by_period()       │
│ StudentRepository.get_count_by_department() │
│ BudgetRepository.get_total_by_category()    │
└─────────────────────────────────────────────┘
    ↓
[MetricCalculator] → 지표 계산
    ↓
[ChartDataBuilder] → 차트 데이터 생성
    ↓
[JSON 응답] → [Frontend 렌더링]
```

### 4. 데이터 조회 플로우
```
[사용자] → [필터 + 검색 조건]
    ↓
[Backend DataView] → [Repository]
    ↓
[필터링된 데이터] + [페이지네이션]
    ↓
[JSON 응답] → [Frontend 테이블 렌더링]
```

### 5. 프로필 관리 플로우
```
[사용자] → [프로필 조회/수정]
    ↓
[Backend ProfileView] → [UserRepository]
    ↓
[user_profiles 테이블] ← CRUD 작업
    ↓
[JSON 응답] → [Frontend 프로필 UI]
```

---

## ERD (Entity Relationship Diagram)

### 엔티티 개요
```
┌─────────────────┐
│  user_profiles  │ (사용자 프로필)
└────────┬────────┘
         │ 1
         │
         │ N
    ┌────┴─────┬─────────┬──────────┬─────────┐
    │          │         │          │         │
    ↓          ↓         ↓          ↓         ↓
┌───────┐  ┌───────┐ ┌─────────┐ ┌────────┐ ┌────────────────┐
│perfor-│  │papers │ │students │ │budgets │ │uploaded_files  │
│mances │  │       │ │         │ │        │ │                │
└───────┘  └───────┘ └─────────┘ └────────┘ └────────────────┘
```

### 관계 설명
- **user_profiles** (1) → (N) **performances**: 한 사용자가 여러 실적 데이터를 업로드
- **user_profiles** (1) → (N) **papers**: 한 사용자가 여러 논문 데이터를 업로드
- **user_profiles** (1) → (N) **students**: 한 사용자가 여러 학생 데이터를 업로드
- **user_profiles** (1) → (N) **budgets**: 한 사용자가 여러 예산 데이터를 업로드
- **user_profiles** (1) → (N) **uploaded_files**: 한 사용자가 여러 파일을 업로드

---

## 테이블 상세 스키마

### 1. user_profiles (사용자 프로필)

사용자 계정 정보 및 프로필을 저장합니다. Supabase Auth와 연동되며, JWT 토큰에서 추출한 user_id를 기본 키로 사용합니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | UUID | PRIMARY KEY | Supabase Auth의 user_id (UUID) |
| email | VARCHAR(255) | NOT NULL, UNIQUE | 사용자 이메일 |
| full_name | VARCHAR(100) | NULL | 사용자 전체 이름 |
| department | VARCHAR(100) | NULL | 부서명 (예: 컴퓨터공학과) |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'user' | 역할 (admin, user) |
| profile_picture_url | TEXT | NULL | 프로필 사진 URL |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 계정 활성화 여부 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 수정 일시 |

**제약 조건**:
- CHECK (role IN ('admin', 'user'))
- CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

---

### 2. performances (실적 데이터)

대학교 실적 데이터를 저장합니다. 연구과제, 특허, 기술이전 등의 실적 정보가 포함됩니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | BIGSERIAL | PRIMARY KEY | 자동 증가 ID |
| date | DATE | NOT NULL | 실적 발생 날짜 |
| title | VARCHAR(255) | NOT NULL | 실적 항목명 (예: 연구과제 A) |
| amount | DECIMAL(15, 2) | NOT NULL | 금액 (원) |
| category | VARCHAR(100) | NOT NULL | 카테고리 (예: 연구비, 특허료) |
| description | TEXT | NULL | 상세 설명 |
| uploaded_by | UUID | NOT NULL, FK → user_profiles(id) | 업로드한 사용자 |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | 소프트 삭제 플래그 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 수정 일시 |

**제약 조건**:
- CHECK (amount >= 0)
- INDEX ON (date, category)
- INDEX ON (uploaded_by)
- INDEX ON (is_deleted)

---

### 3. papers (논문 데이터)

학술 논문 게재 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | BIGSERIAL | PRIMARY KEY | 자동 증가 ID |
| title | VARCHAR(500) | NOT NULL | 논문 제목 |
| authors | TEXT | NOT NULL | 저자 목록 (쉼표 구분) |
| publication_date | DATE | NOT NULL | 게재일 |
| field | VARCHAR(100) | NOT NULL | 분야 (예: 국내학술지, 국제학술지) |
| journal_name | VARCHAR(255) | NULL | 학술지명 |
| doi | VARCHAR(100) | NULL, UNIQUE | DOI (Digital Object Identifier) |
| uploaded_by | UUID | NOT NULL, FK → user_profiles(id) | 업로드한 사용자 |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | 소프트 삭제 플래그 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 수정 일시 |

**제약 조건**:
- INDEX ON (publication_date, field)
- INDEX ON (uploaded_by)
- INDEX ON (is_deleted)

---

### 4. students (학생 데이터)

재학생 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | BIGSERIAL | PRIMARY KEY | 자동 증가 ID |
| student_id | VARCHAR(20) | NOT NULL, UNIQUE | 학번 |
| name | VARCHAR(100) | NOT NULL | 학생 이름 |
| department | VARCHAR(100) | NOT NULL | 학과 |
| grade | INTEGER | NOT NULL | 학년 (1-4, 대학원: 5-6) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | 상태 (active, graduated, withdrawn) |
| uploaded_by | UUID | NOT NULL, FK → user_profiles(id) | 업로드한 사용자 |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | 소프트 삭제 플래그 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 수정 일시 |

**제약 조건**:
- CHECK (grade >= 1 AND grade <= 6)
- CHECK (status IN ('active', 'graduated', 'withdrawn'))
- INDEX ON (department, grade)
- INDEX ON (uploaded_by)
- INDEX ON (is_deleted)

---

### 5. budgets (예산 데이터)

예산 항목 및 집행 정보를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | BIGSERIAL | PRIMARY KEY | 자동 증가 ID |
| item | VARCHAR(255) | NOT NULL | 예산 항목명 |
| amount | DECIMAL(15, 2) | NOT NULL | 금액 (원) |
| category | VARCHAR(100) | NOT NULL | 카테고리 (예: 인건비, 운영비) |
| fiscal_year | INTEGER | NOT NULL | 회계연도 |
| quarter | INTEGER | NULL | 분기 (1-4, NULL은 연간) |
| description | TEXT | NULL | 상세 설명 |
| uploaded_by | UUID | NOT NULL, FK → user_profiles(id) | 업로드한 사용자 |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | 소프트 삭제 플래그 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 수정 일시 |

**제약 조건**:
- CHECK (amount >= 0)
- CHECK (fiscal_year >= 2000 AND fiscal_year <= 2100)
- CHECK (quarter IS NULL OR (quarter >= 1 AND quarter <= 4))
- INDEX ON (fiscal_year, category)
- INDEX ON (uploaded_by)
- INDEX ON (is_deleted)

---

### 6. uploaded_files (업로드 파일 메타데이터)

Excel 파일 업로드 이력 및 메타데이터를 저장합니다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| id | BIGSERIAL | PRIMARY KEY | 자동 증가 ID |
| filename | VARCHAR(255) | NOT NULL | 원본 파일명 |
| data_type | VARCHAR(50) | NOT NULL | 데이터 유형 (performance, paper, student, budget) |
| file_size | BIGINT | NOT NULL | 파일 크기 (bytes) |
| rows_processed | INTEGER | NOT NULL, DEFAULT 0 | 처리된 행 수 |
| rows_failed | INTEGER | NOT NULL, DEFAULT 0 | 처리 실패한 행 수 |
| status | VARCHAR(20) | NOT NULL | 상태 (pending, processing, success, failed) |
| error_message | TEXT | NULL | 오류 메시지 (실패 시) |
| uploaded_by | UUID | NOT NULL, FK → user_profiles(id) | 업로드한 사용자 |
| uploaded_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 업로드 일시 |
| completed_at | TIMESTAMP | NULL | 처리 완료 일시 |

**제약 조건**:
- CHECK (data_type IN ('performance', 'paper', 'student', 'budget'))
- CHECK (status IN ('pending', 'processing', 'success', 'failed'))
- CHECK (rows_processed >= 0)
- CHECK (rows_failed >= 0)
- INDEX ON (uploaded_by, uploaded_at DESC)
- INDEX ON (status)

---

## 데이터 관계 및 외래키

### 외래키 관계

```sql
-- performances 테이블
ALTER TABLE performances
ADD CONSTRAINT fk_performances_uploaded_by
FOREIGN KEY (uploaded_by) REFERENCES user_profiles(id)
ON DELETE RESTRICT;

-- papers 테이블
ALTER TABLE papers
ADD CONSTRAINT fk_papers_uploaded_by
FOREIGN KEY (uploaded_by) REFERENCES user_profiles(id)
ON DELETE RESTRICT;

-- students 테이블
ALTER TABLE students
ADD CONSTRAINT fk_students_uploaded_by
FOREIGN KEY (uploaded_by) REFERENCES user_profiles(id)
ON DELETE RESTRICT;

-- budgets 테이블
ALTER TABLE budgets
ADD CONSTRAINT fk_budgets_uploaded_by
FOREIGN KEY (uploaded_by) REFERENCES user_profiles(id)
ON DELETE RESTRICT;

-- uploaded_files 테이블
ALTER TABLE uploaded_files
ADD CONSTRAINT fk_uploaded_files_uploaded_by
FOREIGN KEY (uploaded_by) REFERENCES user_profiles(id)
ON DELETE RESTRICT;
```

### CASCADE 정책
- **ON DELETE RESTRICT**: 사용자가 삭제되기 전에 해당 사용자가 업로드한 데이터를 먼저 처리해야 함 (데이터 무결성 보장)
- **ON UPDATE CASCADE**: user_profiles의 id가 변경되면 관련 데이터도 자동 업데이트 (UUID는 변경되지 않으므로 실제로는 발생하지 않음)

---

## 인덱스 및 성능 최적화 전략

### 1. 인덱스 전략

#### A. 주요 조회 패턴 기반 인덱스

```sql
-- performances 테이블
CREATE INDEX idx_performances_date_category ON performances(date, category) WHERE is_deleted = FALSE;
CREATE INDEX idx_performances_uploaded_by ON performances(uploaded_by);
CREATE INDEX idx_performances_is_deleted ON performances(is_deleted);

-- papers 테이블
CREATE INDEX idx_papers_publication_date_field ON papers(publication_date, field) WHERE is_deleted = FALSE;
CREATE INDEX idx_papers_uploaded_by ON papers(uploaded_by);
CREATE INDEX idx_papers_is_deleted ON papers(is_deleted);

-- students 테이블
CREATE INDEX idx_students_department_grade ON students(department, grade) WHERE is_deleted = FALSE;
CREATE INDEX idx_students_uploaded_by ON students(uploaded_by);
CREATE INDEX idx_students_is_deleted ON students(is_deleted);

-- budgets 테이블
CREATE INDEX idx_budgets_fiscal_year_category ON budgets(fiscal_year, category) WHERE is_deleted = FALSE;
CREATE INDEX idx_budgets_uploaded_by ON budgets(uploaded_by);
CREATE INDEX idx_budgets_is_deleted ON budgets(is_deleted);

-- uploaded_files 테이블
CREATE INDEX idx_uploaded_files_user_date ON uploaded_files(uploaded_by, uploaded_at DESC);
CREATE INDEX idx_uploaded_files_status ON uploaded_files(status);
```

#### B. 전문 검색(Full-Text Search) 인덱스 (Optional)

```sql
-- performances 테이블 검색
CREATE INDEX idx_performances_title_gin ON performances USING gin(to_tsvector('korean', title));

-- papers 테이블 검색
CREATE INDEX idx_papers_title_gin ON papers USING gin(to_tsvector('korean', title));
```

### 2. 쿼리 최적화 가이드

#### A. N+1 쿼리 방지
Django ORM에서 `select_related()`, `prefetch_related()` 사용:

```python
# BAD: N+1 쿼리 발생
performances = Performance.objects.filter(is_deleted=False)
for p in performances:
    print(p.uploaded_by.full_name)  # 매번 쿼리 발생

# GOOD: JOIN으로 한 번에 조회
performances = Performance.objects.select_related('uploaded_by').filter(is_deleted=False)
for p in performances:
    print(p.uploaded_by.full_name)  # 이미 로드됨
```

#### B. 집계 쿼리 최적화
```python
from django.db.models import Sum, Count, Avg

# 실적 요약 (카테고리별 합계)
summary = Performance.objects.filter(
    is_deleted=False,
    date__year=2024
).values('category').annotate(
    total_amount=Sum('amount'),
    count=Count('id')
)
```

#### C. Pagination
```python
# 커서 기반 페이지네이션 (대용량 데이터)
from django.core.paginator import Paginator

performances = Performance.objects.filter(is_deleted=False).order_by('-date')
paginator = Paginator(performances, 100)  # 페이지당 100건
page = paginator.get_page(1)
```

### 3. 데이터베이스 설정 최적화

```sql
-- Autovacuum 설정 (PostgreSQL)
ALTER TABLE performances SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE papers SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE students SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE budgets SET (autovacuum_vacuum_scale_factor = 0.1);

-- 통계 업데이트
ANALYZE performances;
ANALYZE papers;
ANALYZE students;
ANALYZE budgets;
```

### 4. 캐싱 전략

#### A. 대시보드 데이터 캐싱 (Redis)
```python
from django.core.cache import cache

def get_dashboard_summary(year):
    cache_key = f'dashboard_summary_{year}'
    data = cache.get(cache_key)

    if data is None:
        # 데이터베이스에서 조회
        data = calculate_dashboard_summary(year)
        cache.set(cache_key, data, timeout=300)  # 5분 TTL

    return data
```

#### B. 쿼리 결과 캐싱
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5분 캐싱
def dashboard_view(request):
    # ...
    pass
```

---

## 데이터 흐름도 (CRUD 작업)

### 1. CREATE: Excel 업로드 → 데이터 삽입

```
[사용자] → [Excel 파일 선택]
    ↓
[Frontend: uploadApi.uploadExcel(file, dataType)]
    ↓
[Backend: POST /api/upload/excel/]
    ↓
[UploadView] → [FileProcessorService.process_file()]
    ↓
[ExcelParser.parse()] → List[Dict] 파싱 결과
    ↓
[DataValidator.validate()] → 검증
    ↓
[Repository.bulk_create()] → 트랜잭션 시작
    ↓
┌─────────────────────────────────────────────┐
│ BEGIN TRANSACTION;                          │
│                                             │
│ INSERT INTO performances (...) VALUES (...);│
│ (또는 papers, students, budgets)            │
│                                             │
│ INSERT INTO uploaded_files (...)            │
│ VALUES (                                    │
│   filename='실적.xlsx',                     │
│   data_type='performance',                  │
│   rows_processed=245,                       │
│   status='success',                         │
│   uploaded_by=user_id                       │
│ );                                          │
│                                             │
│ COMMIT;                                     │
└─────────────────────────────────────────────┘
    ↓
[JSON 응답] → [Frontend: 성공 메시지]
```

**트랜잭션 보장**:
- Django `@transaction.atomic` 데코레이터 사용
- 모든 삽입이 성공하거나 전체 롤백

### 2. READ: 대시보드 데이터 조회

```
[사용자] → [대시보드 페이지 진입]
    ↓
[Frontend: dashboardApi.getDashboard({year: 2024})]
    ↓
[Backend: GET /api/dashboard/?year=2024]
    ↓
[DashboardView] → [DashboardService.get_dashboard_summary()]
    ↓
병렬 쿼리 실행:
┌─────────────────────────────────────────────┐
│ SELECT                                      │
│   category,                                 │
│   SUM(amount) as total,                     │
│   COUNT(*) as count                         │
│ FROM performances                           │
│ WHERE is_deleted = FALSE                    │
│   AND EXTRACT(YEAR FROM date) = 2024        │
│ GROUP BY category;                          │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ SELECT                                      │
│   field,                                    │
│   COUNT(*) as count                         │
│ FROM papers                                 │
│ WHERE is_deleted = FALSE                    │
│   AND EXTRACT(YEAR FROM publication_date) = 2024 │
│ GROUP BY field;                             │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ SELECT                                      │
│   department,                               │
│   COUNT(*) as count                         │
│ FROM students                               │
│ WHERE is_deleted = FALSE                    │
│   AND status = 'active'                     │
│ GROUP BY department;                        │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ SELECT                                      │
│   category,                                 │
│   SUM(amount) as total                      │
│ FROM budgets                                │
│ WHERE is_deleted = FALSE                    │
│   AND fiscal_year = 2024                    │
│ GROUP BY category;                          │
└─────────────────────────────────────────────┘
    ↓
[MetricCalculator.calculate_trends()] → 전년 대비 증감률
    ↓
[ChartDataBuilder.build_chart_data()] → 차트 포맷 변환
    ↓
[DashboardSerializer] → JSON 직렬화
    ↓
[JSON 응답] → [Frontend: 차트 렌더링]
```

### 3. UPDATE: 데이터 수정 (관리자)

```
[관리자] → [데이터 상세 모달] → [수정] 버튼
    ↓
[Frontend: dataApi.updateData(id, updatedData)]
    ↓
[Backend: PUT /api/data/{id}/]
    ↓
[DataView] → 권한 확인 (관리자만)
    ↓
[Repository.update()]
    ↓
┌─────────────────────────────────────────────┐
│ UPDATE performances                         │
│ SET                                         │
│   title = '연구과제 A (수정)',              │
│   amount = 1500000,                         │
│   updated_at = NOW()                        │
│ WHERE id = 123                              │
│   AND is_deleted = FALSE;                   │
└─────────────────────────────────────────────┘
    ↓
[JSON 응답] → [Frontend: 성공 메시지]
```

### 4. DELETE: 데이터 삭제 (소프트 삭제)

```
[관리자] → [삭제] 버튼 → [확인 다이얼로그]
    ↓
[Frontend: dataApi.deleteData(id)]
    ↓
[Backend: DELETE /api/data/{id}/]
    ↓
[DataView] → 권한 확인 (관리자만)
    ↓
[Repository.soft_delete()]
    ↓
┌─────────────────────────────────────────────┐
│ UPDATE performances                         │
│ SET                                         │
│   is_deleted = TRUE,                        │
│   updated_at = NOW()                        │
│ WHERE id = 123;                             │
└─────────────────────────────────────────────┘
    ↓
[JSON 응답] → [Frontend: 성공 메시지]
```

**참고**: 30일 후 배치 작업으로 영구 삭제
```sql
DELETE FROM performances
WHERE is_deleted = TRUE
  AND updated_at < NOW() - INTERVAL '30 days';
```

---

## 마이그레이션 전략

### 1. 초기 마이그레이션 순서

Django 마이그레이션 파일 생성 순서:

```
0001_initial.py
├── user_profiles 테이블 생성
│
0002_data_tables.py
├── performances 테이블 생성
├── papers 테이블 생성
├── students 테이블 생성
├── budgets 테이블 생성
│
0003_uploaded_files.py
├── uploaded_files 테이블 생성
│
0004_indexes.py
├── 인덱스 생성 (성능 최적화)
│
0005_constraints.py
├── CHECK 제약 조건 추가
├── 외래키 제약 조건 추가
```

### 2. 마이그레이션 파일 예시

**마이그레이션 파일은 `/supabase/migrations` 디렉토리에 별도로 생성됩니다.**

### 3. 롤백 전략

각 마이그레이션은 `DOWN` 스크립트를 포함하여 롤백 가능해야 합니다.

```sql
-- UP
CREATE TABLE performances (...);

-- DOWN
DROP TABLE IF EXISTS performances CASCADE;
```

### 4. 데이터 마이그레이션 (기존 데이터가 있는 경우)

```sql
-- 예: 기존 Excel 데이터를 데이터베이스로 마이그레이션
INSERT INTO performances (date, title, amount, category, uploaded_by, created_at)
SELECT
  date,
  title,
  amount,
  category,
  '00000000-0000-0000-0000-000000000000'::uuid, -- 시스템 사용자
  NOW()
FROM legacy_performances;
```

### 5. 시드 데이터 (개발/테스트용)

```sql
-- 관리자 계정 생성 (Supabase Auth에서 생성 후 프로필 추가)
INSERT INTO user_profiles (id, email, full_name, department, role)
VALUES
  ('a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, 'admin@university.ac.kr', '관리자', '전산팀', 'admin'),
  ('b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid, 'user@university.ac.kr', '홍길동', '컴퓨터공학과', 'user');

-- 샘플 실적 데이터
INSERT INTO performances (date, title, amount, category, uploaded_by)
VALUES
  ('2024-01-15', '연구과제 A', 1200000, '연구비', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-02-20', '특허 출원', 500000, '특허료', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-03-10', '기술이전', 3000000, '기술료', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 샘플 논문 데이터
INSERT INTO papers (title, authors, publication_date, field, journal_name)
VALUES
  ('딥러닝을 활용한 이미지 분류', '홍길동, 김철수', '2024-01-20', '국제학술지', 'IEEE Transactions on AI', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('빅데이터 분석 기법 연구', '이영희', '2024-02-15', '국내학술지', '한국컴퓨터학회 논문지', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 샘플 학생 데이터
INSERT INTO students (student_id, name, department, grade, uploaded_by)
VALUES
  ('2021001', '김학생', '컴퓨터공학과', 3, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2022002', '이학생', '전자공학과', 2, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023003', '박학생', '기계공학과', 1, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 샘플 예산 데이터
INSERT INTO budgets (item, amount, category, fiscal_year, quarter, uploaded_by)
VALUES
  ('교직원 급여', 50000000, '인건비', 2024, 1, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('연구 장비 구입', 30000000, '연구비', 2024, 1, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('사무용품', 5000000, '운영비', 2024, 1, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);
```

### 6. 마이그레이션 실행

```bash
# Django 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 시드 데이터 삽입 (개발 환경만)
python manage.py loaddata seed_data.json
```

---

## 부록: 데이터베이스 뷰 (Optional)

복잡한 집계 쿼리를 단순화하기 위해 데이터베이스 뷰를 생성할 수 있습니다.

### 1. 대시보드 요약 뷰

```sql
CREATE OR REPLACE VIEW dashboard_summary AS
SELECT
  EXTRACT(YEAR FROM date) as year,
  EXTRACT(QUARTER FROM date) as quarter,
  category,
  SUM(amount) as total_amount,
  COUNT(*) as count,
  AVG(amount) as avg_amount
FROM performances
WHERE is_deleted = FALSE
GROUP BY year, quarter, category;
```

### 2. 논문 통계 뷰

```sql
CREATE OR REPLACE VIEW paper_statistics AS
SELECT
  EXTRACT(YEAR FROM publication_date) as year,
  field,
  COUNT(*) as paper_count,
  COUNT(DISTINCT authors) as unique_authors
FROM papers
WHERE is_deleted = FALSE
GROUP BY year, field;
```

---

## 요약

본 문서는 대학교 사내 데이터 시각화 대시보드 프로젝트의 데이터베이스 설계를 정의합니다.

### 주요 테이블
1. **user_profiles**: 사용자 계정 및 프로필
2. **performances**: 실적 데이터
3. **papers**: 논문 데이터
4. **students**: 학생 데이터
5. **budgets**: 예산 데이터
6. **uploaded_files**: 파일 업로드 메타데이터

### 설계 특징
- **정규화**: 제3정규형 준수로 데이터 중복 최소화
- **소프트 삭제**: 데이터 복구 가능성 보장
- **감사 추적**: created_at, updated_at으로 변경 이력 추적
- **인덱스 최적화**: 주요 조회 패턴에 맞춘 인덱스 설계
- **트랜잭션 보장**: ACID 속성 준수로 데이터 무결성 보장

### 성능 최적화
- 복합 인덱스 활용
- N+1 쿼리 방지
- 캐싱 전략 (Redis)
- 페이지네이션
- 쿼리 최적화

이 설계를 기반으로 안정적이고 확장 가능한 데이터베이스를 구축할 수 있습니다.
