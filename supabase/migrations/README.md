# Supabase 데이터베이스 마이그레이션 (참고용)

## ⚠️ 중요 공지

**이 폴더의 SQL 파일들은 참고용/문서화 목적입니다.**

실제 배포 환경에서는 **Django 마이그레이션**이 자동으로 모든 테이블을 생성하므로,
이 SQL 파일들을 수동으로 실행할 필요가 **전혀 없습니다**.

---

## 실제 사용 중인 시스템

### Django ORM + 자동 마이그레이션

```bash
# Railway 배포 시 자동 실행됨
python manage.py migrate
```

Django가 다음 테이블들을 자동 생성:
- `dashboard_departmentkpi` - 학과 KPI 데이터
- `dashboard_publication` - 논문 목록
- `dashboard_researchproject` - 연구 과제 데이터
- `dashboard_student` - 학생 명단
- `dashboard_performance` - 실적 데이터 (레거시)
- `uploads_uploadhistory` - 업로드 이력
- 그 외 Django 기본 테이블들

**마이그레이션 파일 위치**: `backend/apps/*/migrations/`

---

## 이 폴더의 SQL 파일 목록

### 현재 사용 중인 스키마 (참고용)

| 파일명 | 설명 | 대응 Django 모델 |
|--------|------|------------------|
| `20251102000001_create_department_kpi_table.sql` | 학과 KPI 테이블 | `dashboard.DepartmentKPI` |
| `20251102000002_create_publication_table.sql` | 논문 목록 테이블 | `dashboard.Publication` |
| `20251102000003_create_research_project_table.sql` | 연구 과제 테이블 | `dashboard.ResearchProject` |
| `20251102000004_create_student_table.sql` | 학생 명단 테이블 | `dashboard.Student` |
| `20251102000005_create_upload_history_table.sql` | 업로드 이력 테이블 | `uploads.UploadHistory` |
| `20251102000006_create_indexes.sql` | 인덱스 생성 | Django 모델의 `indexes` 설정 |

### 유틸리티

| 파일명 | 설명 |
|--------|------|
| `rollback_all.sql` | 긴급 롤백용 SQL (모든 테이블 삭제) |
| `legacy/` | 옛날 버전 SQL 파일 (참고용 보관) |

---

## 데이터베이스 초기화 방법

### Supabase 대시보드에서 초기화

```sql
-- 모든 테이블 삭제 및 스키마 재생성
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

### Railway 재배포

초기화 후 Railway가 자동으로 재배포하면서 Django migrate가 모든 테이블을 자동 생성합니다.

---

## 스키마 확인 방법

### Supabase SQL Editor

```sql
-- 생성된 테이블 목록 확인
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- 테이블별 행 수 확인
SELECT
  schemaname,
  tablename,
  n_tup_ins AS total_inserts
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

---

## 참고 자료

- Django 마이그레이션 파일: `backend/apps/*/migrations/`
- Django 모델 정의: `backend/apps/*/persistence/models.py`
- 데이터베이스 스키마 문서: `docs/database.md`
- Supabase 프로젝트: https://supabase.com

---

## 문제 해결

### "No migrations to apply" 오류

데이터베이스를 초기화하고 재배포하세요.

### "relation does not exist" 오류

1. Supabase에서 스키마 재생성
2. Railway 재배포
3. Django migrate가 자동으로 테이블 생성

### 테이블 구조 확인

```sql
-- 특정 테이블의 컬럼 확인
SELECT
  column_name,
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'dashboard_student'
ORDER BY ordinal_position;
```

---

**최종 업데이트**: 2025-11-03
