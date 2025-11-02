-- Migration: Create student table
-- Created: 2025-11-02
-- Description: 학생 명단 테이블 생성 (학생 기본 정보 및 학적 상태)

-- Create student table
CREATE TABLE IF NOT EXISTS student (
    id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL CHECK (LENGTH(name) >= 2 AND LENGTH(name) <= 50),
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 0 AND grade <= 4),
    program_type VARCHAR(10) NOT NULL CHECK (program_type IN ('학사', '석사', '박사')),
    enrollment_status VARCHAR(10) NOT NULL CHECK (enrollment_status IN ('재학', '휴학', '졸업')),
    gender CHAR(1) NOT NULL CHECK (gender IN ('남', '여')),
    admission_year INTEGER NOT NULL CHECK (admission_year >= 2015 AND admission_year <= 2025),
    advisor VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add table and column comments
COMMENT ON TABLE student IS '학생 명단 - 학생 기본 정보 및 학적 상태';
COMMENT ON COLUMN student.id IS '기본키 (자동 증가)';
COMMENT ON COLUMN student.student_id IS '학번 (YYYYMMNNN 형식, 고유값)';
COMMENT ON COLUMN student.name IS '학생 이름 (2~50자)';
COMMENT ON COLUMN student.college IS '단과대학 (예: 공과대학)';
COMMENT ON COLUMN student.department IS '학과 (예: 컴퓨터공학과)';
COMMENT ON COLUMN student.grade IS '학년 (학사: 1~4, 석사/박사: 0)';
COMMENT ON COLUMN student.program_type IS '과정 구분 (학사/석사/박사)';
COMMENT ON COLUMN student.enrollment_status IS '학적 상태 (재학/휴학/졸업)';
COMMENT ON COLUMN student.gender IS '성별 (남 또는 여)';
COMMENT ON COLUMN student.admission_year IS '입학년도 (2015~2025 범위)';
COMMENT ON COLUMN student.advisor IS '지도교수 (학부생은 NULL 가능)';
COMMENT ON COLUMN student.email IS '이메일 주소 (학생 이메일)';
COMMENT ON COLUMN student.created_at IS '레코드 생성 시각';
COMMENT ON COLUMN student.updated_at IS '레코드 최종 수정 시각';

-- Create trigger for automatic updated_at
CREATE TRIGGER update_student_updated_at
BEFORE UPDATE ON student
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
