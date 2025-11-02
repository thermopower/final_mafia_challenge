-- Migration: Create upload_history table
-- Created: 2025-11-02
-- Description: 업로드 이력 테이블 생성 (CSV 파일 업로드 추적)

-- Create upload_history table
CREATE TABLE IF NOT EXISTS upload_history (
    id BIGSERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL CHECK (data_type IN ('department_kpi', 'publication', 'research_project', 'student_roster')),
    rows_processed INTEGER NOT NULL DEFAULT 0 CHECK (rows_processed >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('success', 'partial', 'failed')),
    error_message TEXT,
    uploaded_by VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add table and column comments
COMMENT ON TABLE upload_history IS '업로드 이력 - CSV 파일 업로드 추적';
COMMENT ON COLUMN upload_history.id IS '기본키 (자동 증가)';
COMMENT ON COLUMN upload_history.file_name IS '업로드된 파일명';
COMMENT ON COLUMN upload_history.data_type IS '데이터 유형 (department_kpi, publication, research_project, student_roster 중 하나)';
COMMENT ON COLUMN upload_history.rows_processed IS '성공적으로 처리된 행 수 (0 이상)';
COMMENT ON COLUMN upload_history.status IS '업로드 상태 (success: 전체 성공, partial: 부분 성공, failed: 전체 실패)';
COMMENT ON COLUMN upload_history.error_message IS '오류 발생 시 상세 메시지 (NULL 허용)';
COMMENT ON COLUMN upload_history.uploaded_by IS '업로드한 사용자 (이메일 또는 이름)';
COMMENT ON COLUMN upload_history.uploaded_at IS '업로드 일시';
