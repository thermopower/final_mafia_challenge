-- Migration: 0005_create_budgets_table
-- Description: 예산 데이터 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 예산 데이터 테이블 생성
CREATE TABLE IF NOT EXISTS budgets (
    -- 기본 키
    id BIGSERIAL PRIMARY KEY,

    -- 예산 정보
    item VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    fiscal_year INTEGER NOT NULL,
    quarter INTEGER,
    description TEXT,

    -- 업로드 정보
    uploaded_by UUID NOT NULL,

    -- 소프트 삭제
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- 제약 조건
    CONSTRAINT chk_budgets_amount CHECK (amount >= 0),
    CONSTRAINT chk_budgets_fiscal_year CHECK (fiscal_year >= 2000 AND fiscal_year <= 2100),
    CONSTRAINT chk_budgets_quarter CHECK (quarter IS NULL OR (quarter >= 1 AND quarter <= 4)),
    CONSTRAINT fk_budgets_uploaded_by FOREIGN KEY (uploaded_by)
        REFERENCES user_profiles(id) ON DELETE RESTRICT
);

-- 인덱스 생성
CREATE INDEX idx_budgets_fiscal_year_category ON budgets(fiscal_year, category) WHERE is_deleted = FALSE;
CREATE INDEX idx_budgets_uploaded_by ON budgets(uploaded_by);
CREATE INDEX idx_budgets_is_deleted ON budgets(is_deleted);
CREATE INDEX idx_budgets_fiscal_year ON budgets(fiscal_year DESC);
CREATE INDEX idx_budgets_category ON budgets(category);

-- 코멘트 추가
COMMENT ON TABLE budgets IS '예산 데이터';
COMMENT ON COLUMN budgets.id IS '자동 증가 ID';
COMMENT ON COLUMN budgets.item IS '예산 항목명';
COMMENT ON COLUMN budgets.amount IS '금액 (원)';
COMMENT ON COLUMN budgets.category IS '카테고리 (인건비, 운영비 등)';
COMMENT ON COLUMN budgets.fiscal_year IS '회계연도';
COMMENT ON COLUMN budgets.quarter IS '분기 (1-4, NULL은 연간)';
COMMENT ON COLUMN budgets.description IS '상세 설명';
COMMENT ON COLUMN budgets.uploaded_by IS '업로드한 사용자';
COMMENT ON COLUMN budgets.is_deleted IS '소프트 삭제 플래그';
COMMENT ON COLUMN budgets.created_at IS '생성 일시';
COMMENT ON COLUMN budgets.updated_at IS '수정 일시';

-- updated_at 트리거 적용
CREATE TRIGGER trg_budgets_updated_at
BEFORE UPDATE ON budgets
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
