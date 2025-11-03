-- Migration: 0006_create_uploaded_files_table
-- Description: 업로드 파일 메타데이터 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 업로드 파일 메타데이터 테이블 생성
CREATE TABLE IF NOT EXISTS uploaded_files (
    -- 기본 키
    id BIGSERIAL PRIMARY KEY,

    -- 파일 정보
    filename VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,

    -- 처리 결과
    rows_processed INTEGER NOT NULL DEFAULT 0,
    rows_failed INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,

    -- 업로드 정보
    uploaded_by UUID NOT NULL,

    -- 타임스탬프
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,

    -- 제약 조건
    CONSTRAINT chk_uploaded_files_data_type CHECK (data_type IN ('performance', 'paper', 'student', 'budget')),
    CONSTRAINT chk_uploaded_files_status CHECK (status IN ('pending', 'processing', 'success', 'failed')),
    CONSTRAINT chk_uploaded_files_rows_processed CHECK (rows_processed >= 0),
    CONSTRAINT chk_uploaded_files_rows_failed CHECK (rows_failed >= 0),
    CONSTRAINT fk_uploaded_files_uploaded_by FOREIGN KEY (uploaded_by)
        REFERENCES user_profiles(id) ON DELETE RESTRICT
);

-- 인덱스 생성
CREATE INDEX idx_uploaded_files_user_date ON uploaded_files(uploaded_by, uploaded_at DESC);
CREATE INDEX idx_uploaded_files_status ON uploaded_files(status);
CREATE INDEX idx_uploaded_files_data_type ON uploaded_files(data_type);
CREATE INDEX idx_uploaded_files_uploaded_at ON uploaded_files(uploaded_at DESC);

-- 코멘트 추가
COMMENT ON TABLE uploaded_files IS '업로드 파일 메타데이터';
COMMENT ON COLUMN uploaded_files.id IS '자동 증가 ID';
COMMENT ON COLUMN uploaded_files.filename IS '원본 파일명';
COMMENT ON COLUMN uploaded_files.data_type IS '데이터 유형 (performance, paper, student, budget)';
COMMENT ON COLUMN uploaded_files.file_size IS '파일 크기 (bytes)';
COMMENT ON COLUMN uploaded_files.rows_processed IS '처리된 행 수';
COMMENT ON COLUMN uploaded_files.rows_failed IS '처리 실패한 행 수';
COMMENT ON COLUMN uploaded_files.status IS '상태 (pending, processing, success, failed)';
COMMENT ON COLUMN uploaded_files.error_message IS '오류 메시지 (실패 시)';
COMMENT ON COLUMN uploaded_files.uploaded_by IS '업로드한 사용자';
COMMENT ON COLUMN uploaded_files.uploaded_at IS '업로드 일시';
COMMENT ON COLUMN uploaded_files.completed_at IS '처리 완료 일시';
