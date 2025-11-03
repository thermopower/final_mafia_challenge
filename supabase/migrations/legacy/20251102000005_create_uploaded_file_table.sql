-- Migration: Create uploaded_file table
-- Description: Stores file upload history and metadata

CREATE TABLE IF NOT EXISTS uploaded_file (
    id BIGSERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    rows_processed INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    uploaded_by VARCHAR(100) NOT NULL,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add check constraints
ALTER TABLE uploaded_file
ADD CONSTRAINT chk_file_type CHECK (file_type IN ('department_kpi', 'publication', 'research_project', 'student'));

ALTER TABLE uploaded_file
ADD CONSTRAINT chk_status CHECK (status IN ('success', 'failed', 'processing'));

ALTER TABLE uploaded_file
ADD CONSTRAINT chk_rows_processed_positive CHECK (rows_processed >= 0);

-- Create indexes
CREATE INDEX idx_uploaded_file_upload_date ON uploaded_file(upload_date DESC);
CREATE INDEX idx_uploaded_file_file_type ON uploaded_file(file_type);
CREATE INDEX idx_uploaded_file_status ON uploaded_file(status);
CREATE INDEX idx_uploaded_file_uploaded_by ON uploaded_file(uploaded_by);

-- Comment
COMMENT ON TABLE uploaded_file IS 'Stores file upload history including filename, type, processing status, and error messages';
