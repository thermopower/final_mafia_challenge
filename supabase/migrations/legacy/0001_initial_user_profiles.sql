-- Migration: 0001_initial_user_profiles
-- Description: 사용자 프로필 테이블 생성
-- Created: 2024-11-01
-- Author: System

-- 사용자 프로필 테이블 생성
CREATE TABLE IF NOT EXISTS user_profiles (
    -- Supabase Auth의 user_id와 동일한 UUID 사용
    id UUID PRIMARY KEY,

    -- 기본 정보
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    department VARCHAR(100),

    -- 역할 (admin: 관리자, user: 일반 사용자)
    role VARCHAR(20) NOT NULL DEFAULT 'user',

    -- 프로필 사진
    profile_picture_url TEXT,

    -- 계정 상태
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- 제약 조건
    CONSTRAINT chk_user_profiles_role CHECK (role IN ('admin', 'user')),
    CONSTRAINT chk_user_profiles_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 인덱스 생성
CREATE INDEX idx_user_profiles_email ON user_profiles(email);
CREATE INDEX idx_user_profiles_role ON user_profiles(role);
CREATE INDEX idx_user_profiles_is_active ON user_profiles(is_active);

-- 코멘트 추가
COMMENT ON TABLE user_profiles IS '사용자 프로필 정보';
COMMENT ON COLUMN user_profiles.id IS 'Supabase Auth의 user_id (UUID)';
COMMENT ON COLUMN user_profiles.email IS '사용자 이메일';
COMMENT ON COLUMN user_profiles.full_name IS '사용자 전체 이름';
COMMENT ON COLUMN user_profiles.department IS '부서명';
COMMENT ON COLUMN user_profiles.role IS '역할 (admin: 관리자, user: 일반 사용자)';
COMMENT ON COLUMN user_profiles.profile_picture_url IS '프로필 사진 URL';
COMMENT ON COLUMN user_profiles.is_active IS '계정 활성화 여부';
COMMENT ON COLUMN user_profiles.created_at IS '생성 일시';
COMMENT ON COLUMN user_profiles.updated_at IS '수정 일시';

-- updated_at 자동 갱신 트리거 함수 생성
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- updated_at 트리거 적용
CREATE TRIGGER trg_user_profiles_updated_at
BEFORE UPDATE ON user_profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
