-- Migration: Create publication table
-- Created: 2025-11-02
-- Description: 논문 목록 테이블 생성 (학술지 게재 논문 정보)

-- Create publication table
CREATE TABLE IF NOT EXISTS publication (
    id BIGSERIAL PRIMARY KEY,
    paper_id VARCHAR(50) NOT NULL UNIQUE,
    publication_date DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    paper_title TEXT NOT NULL CHECK (LENGTH(paper_title) >= 1 AND LENGTH(paper_title) <= 500),
    lead_author VARCHAR(100) NOT NULL,
    co_authors TEXT,
    journal_name VARCHAR(200) NOT NULL,
    journal_grade VARCHAR(10) NOT NULL CHECK (journal_grade IN ('SCIE', 'KCI')),
    impact_factor NUMERIC(6,2) CHECK (impact_factor IS NULL OR impact_factor >= 0),
    project_linked CHAR(1) NOT NULL CHECK (project_linked IN ('Y', 'N')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add table and column comments
COMMENT ON TABLE publication IS '논문 목록 - 학술지 게재 논문 정보';
COMMENT ON COLUMN publication.id IS '기본키 (자동 증가)';
COMMENT ON COLUMN publication.paper_id IS '논문 고유 ID (PUB-YY-NNN 형식)';
COMMENT ON COLUMN publication.publication_date IS '논문 게재일 (YYYY-MM-DD 형식)';
COMMENT ON COLUMN publication.college IS '단과대학 (예: 공과대학)';
COMMENT ON COLUMN publication.department IS '학과 (예: 컴퓨터공학과)';
COMMENT ON COLUMN publication.paper_title IS '논문 제목 (1~500자)';
COMMENT ON COLUMN publication.lead_author IS '주저자 (논문 제1저자)';
COMMENT ON COLUMN publication.co_authors IS '참여저자 (세미콜론(;)으로 구분)';
COMMENT ON COLUMN publication.journal_name IS '학술지명 (논문이 게재된 저널명)';
COMMENT ON COLUMN publication.journal_grade IS '저널 등급 (SCIE 또는 KCI)';
COMMENT ON COLUMN publication.impact_factor IS 'Impact Factor (SCIE만 필수, KCI는 NULL)';
COMMENT ON COLUMN publication.project_linked IS '과제연계여부 (Y: 연계됨, N: 연계안됨)';
COMMENT ON COLUMN publication.created_at IS '레코드 생성 시각';
COMMENT ON COLUMN publication.updated_at IS '레코드 최종 수정 시각';

-- Create trigger for automatic updated_at
CREATE TRIGGER update_publication_updated_at
BEFORE UPDATE ON publication
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
