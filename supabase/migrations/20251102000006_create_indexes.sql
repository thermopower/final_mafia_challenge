-- Migration: Create indexes for all tables
-- Created: 2025-11-02
-- Description: 조회 성능 최적화를 위한 인덱스 생성

-- ======================================================================
-- 1. department_kpi 인덱스
-- ======================================================================

-- 평가년도별 조회 (대시보드 메인 쿼리)
CREATE INDEX IF NOT EXISTS idx_dept_kpi_year 
ON department_kpi(evaluation_year DESC);

-- 학과별 조회
CREATE INDEX IF NOT EXISTS idx_dept_kpi_dept 
ON department_kpi(department);

-- 단과대학별 조회
CREATE INDEX IF NOT EXISTS idx_dept_kpi_college 
ON department_kpi(college);

-- 연도 + 단과대학 복합 조회 (필터링)
CREATE INDEX IF NOT EXISTS idx_dept_kpi_year_college 
ON department_kpi(evaluation_year, college);

-- 생성 시각 기준 정렬 (최근 업데이트 확인)
CREATE INDEX IF NOT EXISTS idx_dept_kpi_created 
ON department_kpi(created_at DESC);

-- ======================================================================
-- 2. publication 인덱스
-- ======================================================================

-- 게재일 기준 조회 (연도별 추이)
CREATE INDEX IF NOT EXISTS idx_pub_date 
ON publication(publication_date DESC);

-- 학과별 조회
CREATE INDEX IF NOT EXISTS idx_pub_dept 
ON publication(department);

-- 단과대학별 조회
CREATE INDEX IF NOT EXISTS idx_pub_college 
ON publication(college);

-- 저널 등급별 조회 (SCIE/KCI 분류)
CREATE INDEX IF NOT EXISTS idx_pub_grade 
ON publication(journal_grade);

-- 과제 연계 여부 조회
CREATE INDEX IF NOT EXISTS idx_pub_linked 
ON publication(project_linked);

-- 연도 + 학과 복합 조회 (필터링)
CREATE INDEX IF NOT EXISTS idx_pub_year_dept 
ON publication(EXTRACT(YEAR FROM publication_date), department);

-- Impact Factor 통계 (SCIE 논문만) - 부분 인덱스
CREATE INDEX IF NOT EXISTS idx_pub_if 
ON publication(impact_factor) 
WHERE journal_grade = 'SCIE' AND impact_factor IS NOT NULL;

-- ======================================================================
-- 3. research_project 인덱스
-- ======================================================================

-- 과제번호별 조회 (집행 내역 조회)
CREATE INDEX IF NOT EXISTS idx_rp_project_number 
ON research_project(project_number);

-- 연구책임자별 조회
CREATE INDEX IF NOT EXISTS idx_rp_pi 
ON research_project(principal_investigator);

-- 학과별 조회
CREATE INDEX IF NOT EXISTS idx_rp_dept 
ON research_project(department);

-- 지원 기관별 조회
CREATE INDEX IF NOT EXISTS idx_rp_agency 
ON research_project(funding_agency);

-- 집행일자별 조회 (월별/분기별 추이)
CREATE INDEX IF NOT EXISTS idx_rp_date 
ON research_project(execution_date DESC);

-- 상태별 조회 (집행완료/처리중)
CREATE INDEX IF NOT EXISTS idx_rp_status 
ON research_project(status);

-- 과제번호 + 집행일자 복합 조회
CREATE INDEX IF NOT EXISTS idx_rp_project_date 
ON research_project(project_number, execution_date);

-- 집행 항목별 집계
CREATE INDEX IF NOT EXISTS idx_rp_item 
ON research_project(execution_item);

-- ======================================================================
-- 4. student 인덱스
-- ======================================================================

-- 학과별 조회
CREATE INDEX IF NOT EXISTS idx_student_dept 
ON student(department);

-- 단과대학별 조회
CREATE INDEX IF NOT EXISTS idx_student_college 
ON student(college);

-- 과정 구분별 조회 (학사/석사/박사)
CREATE INDEX IF NOT EXISTS idx_student_program 
ON student(program_type);

-- 학적 상태별 조회 (재학/휴학/졸업)
CREATE INDEX IF NOT EXISTS idx_student_status 
ON student(enrollment_status);

-- 학년별 조회
CREATE INDEX IF NOT EXISTS idx_student_grade 
ON student(grade);

-- 지도교수별 조회 - 부분 인덱스 (NULL 제외)
CREATE INDEX IF NOT EXISTS idx_student_advisor 
ON student(advisor) 
WHERE advisor IS NOT NULL;

-- 입학년도별 조회
CREATE INDEX IF NOT EXISTS idx_student_admission 
ON student(admission_year);

-- 학과 + 학적상태 복합 조회 (가장 자주 사용)
CREATE INDEX IF NOT EXISTS idx_student_dept_status 
ON student(department, enrollment_status);

-- 성별 통계
CREATE INDEX IF NOT EXISTS idx_student_gender 
ON student(gender);

-- ======================================================================
-- 5. upload_history 인덱스
-- ======================================================================

-- 업로드 일시 기준 조회 (최근 이력)
CREATE INDEX IF NOT EXISTS idx_upload_history_date 
ON upload_history(uploaded_at DESC);

-- 데이터 타입별 조회
CREATE INDEX IF NOT EXISTS idx_upload_history_type 
ON upload_history(data_type);

-- 상태별 조회 (실패 이력 조회)
CREATE INDEX IF NOT EXISTS idx_upload_history_status 
ON upload_history(status);

-- 업로드 사용자별 조회
CREATE INDEX IF NOT EXISTS idx_upload_history_user 
ON upload_history(uploaded_by);

-- ======================================================================
-- 인덱스 생성 완료 메시지
-- ======================================================================

DO $$
BEGIN
    RAISE NOTICE '모든 인덱스 생성 완료: 총 33개의 인덱스가 생성되었습니다.';
    RAISE NOTICE '- department_kpi: 5개 인덱스';
    RAISE NOTICE '- publication: 7개 인덱스';
    RAISE NOTICE '- research_project: 8개 인덱스';
    RAISE NOTICE '- student: 9개 인덱스';
    RAISE NOTICE '- upload_history: 4개 인덱스';
END $$;
