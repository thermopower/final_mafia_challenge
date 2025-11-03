-- Migration: 0002_create_performances_table
-- Description: 실적 데이터 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 실적 데이터 테이블 생성
CREATE TABLE IF NOT EXISTS performances (
    -- 기본 키
    id BIGSERIAL PRIMARY KEY,

    -- 실적 정보
    date DATE NOT NULL,
    title VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,

    -- 업로드 정보
    uploaded_by UUID NOT NULL,

    -- 소프트 삭제
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- 제약 조건
    CONSTRAINT chk_performances_amount CHECK (amount >= 0),
    CONSTRAINT fk_performances_uploaded_by FOREIGN KEY (uploaded_by)
        REFERENCES user_profiles(id) ON DELETE RESTRICT
);

-- 인덱스 생성
CREATE INDEX idx_performances_date_category ON performances(date, category) WHERE is_deleted = FALSE;
CREATE INDEX idx_performances_uploaded_by ON performances(uploaded_by);
CREATE INDEX idx_performances_is_deleted ON performances(is_deleted);
CREATE INDEX idx_performances_date ON performances(date DESC);

-- 전문 검색 인덱스 (Optional)
CREATE INDEX idx_performances_title_gin ON performances USING gin(to_tsvector('simple', title));

-- 코멘트 추가
COMMENT ON TABLE performances IS '실적 데이터';
COMMENT ON COLUMN performances.id IS '자동 증가 ID';
COMMENT ON COLUMN performances.date IS '실적 발생 날짜';
COMMENT ON COLUMN performances.title IS '실적 항목명';
COMMENT ON COLUMN performances.amount IS '금액 (원)';
COMMENT ON COLUMN performances.category IS '카테고리';
COMMENT ON COLUMN performances.description IS '상세 설명';
COMMENT ON COLUMN performances.uploaded_by IS '업로드한 사용자';
COMMENT ON COLUMN performances.is_deleted IS '소프트 삭제 플래그';
COMMENT ON COLUMN performances.created_at IS '생성 일시';
COMMENT ON COLUMN performances.updated_at IS '수정 일시';

-- updated_at 트리거 적용
CREATE TRIGGER trg_performances_updated_at
BEFORE UPDATE ON performances
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
