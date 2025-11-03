-- Migration: 0003_create_papers_table
-- Description: 논문 데이터 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 논문 데이터 테이블 생성
CREATE TABLE IF NOT EXISTS papers (
    -- 기본 키
    id BIGSERIAL PRIMARY KEY,

    -- 논문 정보
    title VARCHAR(500) NOT NULL,
    authors TEXT NOT NULL,
    publication_date DATE NOT NULL,
    field VARCHAR(100) NOT NULL,
    journal_name VARCHAR(255),
    doi VARCHAR(100) UNIQUE,

    -- 업로드 정보
    uploaded_by UUID NOT NULL,

    -- 소프트 삭제
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- 외래 키 제약 조건
    CONSTRAINT fk_papers_uploaded_by FOREIGN KEY (uploaded_by)
        REFERENCES user_profiles(id) ON DELETE RESTRICT
);

-- 인덱스 생성
CREATE INDEX idx_papers_publication_date_field ON papers(publication_date, field) WHERE is_deleted = FALSE;
CREATE INDEX idx_papers_uploaded_by ON papers(uploaded_by);
CREATE INDEX idx_papers_is_deleted ON papers(is_deleted);
CREATE INDEX idx_papers_publication_date ON papers(publication_date DESC);
CREATE INDEX idx_papers_field ON papers(field);

-- 전문 검색 인덱스 (Optional)
CREATE INDEX idx_papers_title_gin ON papers USING gin(to_tsvector('simple', title));

-- 코멘트 추가
COMMENT ON TABLE papers IS '논문 데이터';
COMMENT ON COLUMN papers.id IS '자동 증가 ID';
COMMENT ON COLUMN papers.title IS '논문 제목';
COMMENT ON COLUMN papers.authors IS '저자 목록 (쉼표 구분)';
COMMENT ON COLUMN papers.publication_date IS '게재일';
COMMENT ON COLUMN papers.field IS '분야 (국내학술지, 국제학술지 등)';
COMMENT ON COLUMN papers.journal_name IS '학술지명';
COMMENT ON COLUMN papers.doi IS 'DOI (Digital Object Identifier)';
COMMENT ON COLUMN papers.uploaded_by IS '업로드한 사용자';
COMMENT ON COLUMN papers.is_deleted IS '소프트 삭제 플래그';
COMMENT ON COLUMN papers.created_at IS '생성 일시';
COMMENT ON COLUMN papers.updated_at IS '수정 일시';

-- updated_at 트리거 적용
CREATE TRIGGER trg_papers_updated_at
BEFORE UPDATE ON papers
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
