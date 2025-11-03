-- Migration: 0004_create_students_table
-- Description: 학생 데이터 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 학생 데이터 테이블 생성
CREATE TABLE IF NOT EXISTS students (
    -- 기본 키
    id BIGSERIAL PRIMARY KEY,

    -- 학생 정보
    student_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    grade INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',

    -- 업로드 정보
    uploaded_by UUID NOT NULL,

    -- 소프트 삭제
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- 제약 조건
    CONSTRAINT chk_students_grade CHECK (grade >= 1 AND grade <= 6),
    CONSTRAINT chk_students_status CHECK (status IN ('active', 'graduated', 'withdrawn')),
    CONSTRAINT fk_students_uploaded_by FOREIGN KEY (uploaded_by)
        REFERENCES user_profiles(id) ON DELETE RESTRICT
);

-- 인덱스 생성
CREATE INDEX idx_students_department_grade ON students(department, grade) WHERE is_deleted = FALSE;
CREATE INDEX idx_students_uploaded_by ON students(uploaded_by);
CREATE INDEX idx_students_is_deleted ON students(is_deleted);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_student_id ON students(student_id);

-- 코멘트 추가
COMMENT ON TABLE students IS '학생 데이터';
COMMENT ON COLUMN students.id IS '자동 증가 ID';
COMMENT ON COLUMN students.student_id IS '학번';
COMMENT ON COLUMN students.name IS '학생 이름';
COMMENT ON COLUMN students.department IS '학과';
COMMENT ON COLUMN students.grade IS '학년 (1-4: 학부, 5-6: 대학원)';
COMMENT ON COLUMN students.status IS '상태 (active: 재학, graduated: 졸업, withdrawn: 휴학/자퇴)';
COMMENT ON COLUMN students.uploaded_by IS '업로드한 사용자';
COMMENT ON COLUMN students.is_deleted IS '소프트 삭제 플래그';
COMMENT ON COLUMN students.created_at IS '생성 일시';
COMMENT ON COLUMN students.updated_at IS '수정 일시';

-- updated_at 트리거 적용
CREATE TRIGGER trg_students_updated_at
BEFORE UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
