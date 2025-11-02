-- Migration: Create research_project table
-- Created: 2025-11-02
-- Description: 연구 과제 집행 데이터 테이블 생성 (예산 집행 현황)

-- Create research_project table
CREATE TABLE IF NOT EXISTS research_project (
    id BIGSERIAL PRIMARY KEY,
    execution_id VARCHAR(50) NOT NULL UNIQUE,
    project_number VARCHAR(100) NOT NULL,
    project_name VARCHAR(200) NOT NULL,
    principal_investigator VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    funding_agency VARCHAR(100) NOT NULL,
    total_budget BIGINT NOT NULL CHECK (total_budget >= 0),
    execution_date DATE NOT NULL,
    execution_item VARCHAR(200) NOT NULL,
    execution_amount BIGINT NOT NULL CHECK (execution_amount >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('집행완료', '처리중')),
    remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add table and column comments
COMMENT ON TABLE research_project IS '연구 과제 집행 데이터 - 예산 집행 현황';
COMMENT ON COLUMN research_project.id IS '기본키 (자동 증가)';
COMMENT ON COLUMN research_project.execution_id IS '집행 고유 ID (T2324NNN 형식)';
COMMENT ON COLUMN research_project.project_number IS '과제번호 (예: NRF-2023-015)';
COMMENT ON COLUMN research_project.project_name IS '과제명 (연구 과제 이름)';
COMMENT ON COLUMN research_project.principal_investigator IS '연구책임자 (PI: Principal Investigator)';
COMMENT ON COLUMN research_project.department IS '소속학과 (연구책임자 소속)';
COMMENT ON COLUMN research_project.funding_agency IS '지원기관 (예: 한국연구재단, 정보통신기획평가원)';
COMMENT ON COLUMN research_project.total_budget IS '총 연구비 (원 단위, 0 이상)';
COMMENT ON COLUMN research_project.execution_date IS '집행일자 (YYYY-MM-DD 형식)';
COMMENT ON COLUMN research_project.execution_item IS '집행항목 (예: 연구장비 도입, 인건비)';
COMMENT ON COLUMN research_project.execution_amount IS '집행 금액 (원 단위, 0 이상)';
COMMENT ON COLUMN research_project.status IS '집행 상태 (집행완료 또는 처리중)';
COMMENT ON COLUMN research_project.remarks IS '비고 (추가 설명, NULL 허용)';
COMMENT ON COLUMN research_project.created_at IS '레코드 생성 시각';
COMMENT ON COLUMN research_project.updated_at IS '레코드 최종 수정 시각';

-- Create trigger for automatic updated_at
CREATE TRIGGER update_research_project_updated_at
BEFORE UPDATE ON research_project
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
