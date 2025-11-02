-- Migration: Create department_kpi table
-- Created: 2025-11-02
-- Description: 학과 KPI 데이터 테이블 생성 (평가년도별 학과 성과 지표)

-- Create department_kpi table
CREATE TABLE IF NOT EXISTS department_kpi (
    id BIGSERIAL PRIMARY KEY,
    evaluation_year INTEGER NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    employment_rate NUMERIC(5,2) NOT NULL CHECK (employment_rate >= 0 AND employment_rate <= 100),
    full_time_faculty INTEGER NOT NULL CHECK (full_time_faculty >= 0),
    visiting_faculty INTEGER NOT NULL CHECK (visiting_faculty >= 0),
    tech_transfer_income NUMERIC(10,1) NOT NULL CHECK (tech_transfer_income >= 0),
    intl_conferences INTEGER NOT NULL CHECK (intl_conferences >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_department_kpi_year_dept UNIQUE (evaluation_year, department)
);

-- Add table and column comments
COMMENT ON TABLE department_kpi IS '학과 KPI 데이터 - 평가년도별 학과 성과 지표';
COMMENT ON COLUMN department_kpi.id IS '기본키 (자동 증가)';
COMMENT ON COLUMN department_kpi.evaluation_year IS '평가년도 (2020~2030 범위)';
COMMENT ON COLUMN department_kpi.college IS '단과대학 (예: 공과대학)';
COMMENT ON COLUMN department_kpi.department IS '학과 (예: 컴퓨터공학과)';
COMMENT ON COLUMN department_kpi.employment_rate IS '졸업생 취업률 (%, 소수점 2자리)';
COMMENT ON COLUMN department_kpi.full_time_faculty IS '전임교원 수 (명)';
COMMENT ON COLUMN department_kpi.visiting_faculty IS '초빙교원 수 (명)';
COMMENT ON COLUMN department_kpi.tech_transfer_income IS '연간 기술이전 수입액 (억원 단위)';
COMMENT ON COLUMN department_kpi.intl_conferences IS '국제학술대회 개최 횟수';
COMMENT ON COLUMN department_kpi.created_at IS '레코드 생성 시각';
COMMENT ON COLUMN department_kpi.updated_at IS '레코드 최종 수정 시각';

-- Create function for automatic updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic updated_at
CREATE TRIGGER update_department_kpi_updated_at
BEFORE UPDATE ON department_kpi
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
