# 데이터베이스 마이그레이션 가이드

## 개요

이 디렉토리에는 대학교 사내 데이터 시각화 대시보드 프로젝트의 PostgreSQL 데이터베이스 마이그레이션 스크립트가 포함되어 있습니다.

## 마이그레이션 파일 목록

| 파일명 | 설명 | 의존성 |
|--------|------|--------|
| `0001_initial_user_profiles.sql` | 사용자 프로필 테이블 생성 | 없음 |
| `0002_create_performances_table.sql` | 실적 데이터 테이블 생성 | 0001 |
| `0003_create_papers_table.sql` | 논문 데이터 테이블 생성 | 0001 |
| `0004_create_students_table.sql` | 학생 데이터 테이블 생성 | 0001 |
| `0005_create_budgets_table.sql` | 예산 데이터 테이블 생성 | 0001 |
| `0006_create_uploaded_files_table.sql` | 업로드 파일 메타데이터 테이블 생성 | 0001 |
| `0007_seed_data.sql` | 개발/테스트용 시드 데이터 삽입 | 0001-0006 |

## 마이그레이션 실행 방법

### 방법 1: Supabase CLI 사용 (권장)

```bash
# Supabase 프로젝트 초기화 (최초 1회)
supabase init

# Supabase 로컬 환경 시작
supabase start

# 마이그레이션 실행
supabase db push

# 또는 특정 마이그레이션 파일 실행
supabase db push --file supabase/migrations/0001_initial_user_profiles.sql
```

### 방법 2: psql 직접 사용

```bash
# PostgreSQL 접속
psql -h db.your-project.supabase.co -U postgres -d postgres

# 마이그레이션 파일 순차 실행
\i supabase/migrations/0001_initial_user_profiles.sql
\i supabase/migrations/0002_create_performances_table.sql
\i supabase/migrations/0003_create_papers_table.sql
\i supabase/migrations/0004_create_students_table.sql
\i supabase/migrations/0005_create_budgets_table.sql
\i supabase/migrations/0006_create_uploaded_files_table.sql

# 개발 환경에서만 시드 데이터 삽입
\i supabase/migrations/0007_seed_data.sql
```

### 방법 3: Django 마이그레이션과 통합

Django ORM 모델을 정의한 후, 마이그레이션을 생성하고 적용할 수 있습니다.

```bash
# Django 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 시드 데이터 삽입 (fixtures 사용)
python manage.py loaddata seed_data.json
```

## 마이그레이션 실행 순서

**중요**: 마이그레이션은 반드시 번호 순서대로 실행해야 합니다.

1. `0001_initial_user_profiles.sql` - 사용자 프로필 테이블 및 트리거 함수 생성
2. `0002_create_performances_table.sql` - 실적 테이블 생성 (user_profiles 참조)
3. `0003_create_papers_table.sql` - 논문 테이블 생성 (user_profiles 참조)
4. `0004_create_students_table.sql` - 학생 테이블 생성 (user_profiles 참조)
5. `0005_create_budgets_table.sql` - 예산 테이블 생성 (user_profiles 참조)
6. `0006_create_uploaded_files_table.sql` - 업로드 파일 메타데이터 테이블 생성 (user_profiles 참조)
7. `0007_seed_data.sql` - 시드 데이터 삽입 (개발/테스트 환경만)

## 롤백 방법

각 마이그레이션을 롤백하려면 역순으로 테이블을 삭제합니다.

```sql
-- 롤백 순서 (역순)
DROP TABLE IF EXISTS uploaded_files CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS papers CASCADE;
DROP TABLE IF EXISTS performances CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;

-- 트리거 함수 삭제
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
```

또는 개별 파일의 롤백:

```bash
psql -h db.your-project.supabase.co -U postgres -d postgres -f rollback_all.sql
```

## 환경별 실행 가이드

### 개발 환경 (Development)

```bash
# 모든 마이그레이션 + 시드 데이터 실행
supabase db push
```

### 스테이징 환경 (Staging)

```bash
# 시드 데이터 제외하고 실행
supabase db push --exclude 0007_seed_data.sql
```

### 프로덕션 환경 (Production)

```bash
# 시드 데이터 제외하고 실행
# 프로덕션에서는 반드시 백업 후 실행!
pg_dump -h db.your-project.supabase.co -U postgres -d postgres > backup_$(date +%Y%m%d_%H%M%S).sql

# 마이그레이션 실행 (시드 데이터 제외)
for i in {1..6}; do
  psql -h db.your-project.supabase.co -U postgres -d postgres -f supabase/migrations/000${i}_*.sql
done
```

## 마이그레이션 검증

마이그레이션 실행 후 다음 쿼리로 테이블 생성을 확인합니다.

```sql
-- 생성된 테이블 목록 확인
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 각 테이블의 행 수 확인
SELECT
  'user_profiles' AS table_name,
  COUNT(*) AS row_count
FROM user_profiles
UNION ALL
SELECT 'performances', COUNT(*) FROM performances
UNION ALL
SELECT 'papers', COUNT(*) FROM papers
UNION ALL
SELECT 'students', COUNT(*) FROM students
UNION ALL
SELECT 'budgets', COUNT(*) FROM budgets
UNION ALL
SELECT 'uploaded_files', COUNT(*) FROM uploaded_files;

-- 외래 키 제약 조건 확인
SELECT
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name, kcu.column_name;

-- 인덱스 확인
SELECT
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

## 트러블슈팅

### 오류: "relation already exists"

```sql
-- 기존 테이블이 있는 경우 삭제 후 재생성
DROP TABLE IF EXISTS [테이블명] CASCADE;
```

### 오류: "foreign key constraint fails"

외래 키 참조 문제가 발생하면 순서대로 롤백 후 다시 실행:

```sql
-- 자식 테이블부터 삭제
DROP TABLE IF EXISTS uploaded_files CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS papers CASCADE;
DROP TABLE IF EXISTS performances CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
```

### 오류: "duplicate key value violates unique constraint"

시드 데이터 중복 삽입 시:

```sql
-- 시드 데이터 삭제
TRUNCATE TABLE uploaded_files, budgets, students, papers, performances, user_profiles RESTART IDENTITY CASCADE;

-- 다시 시드 데이터 삽입
\i supabase/migrations/0007_seed_data.sql
```

## 추가 마이그레이션 생성 방법

새로운 마이그레이션 파일을 추가하려면:

1. 파일명 규칙: `000X_description.sql` (예: `0008_add_comments_table.sql`)
2. 파일 내용:

```sql
-- Migration: 0008_add_comments_table
-- Description: 코멘트 테이블 추가
-- Created: YYYY-MM-DD
-- Author: Your Name

-- UP 마이그레이션
CREATE TABLE IF NOT EXISTS comments (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- DOWN 마이그레이션 (롤백용)
-- DROP TABLE IF EXISTS comments CASCADE;
```

3. 마이그레이션 실행:

```bash
psql -h db.your-project.supabase.co -U postgres -d postgres -f supabase/migrations/0008_add_comments_table.sql
```

## 참고 자료

- [Supabase 마이그레이션 문서](https://supabase.com/docs/guides/cli/local-development#database-migrations)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
- [Django 마이그레이션 문서](https://docs.djangoproject.com/en/5.0/topics/migrations/)

## 연락처

문제가 발생하면 프로젝트 관리자에게 문의하세요.
