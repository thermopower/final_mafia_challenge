-- Rollback Script: rollback_all.sql
-- Description: 모든 마이그레이션 롤백 (역순)
-- Created: 2024-11-01
-- Author: System
-- WARNING: 이 스크립트는 모든 데이터를 삭제합니다!

-- 경고 메시지
DO $$
BEGIN
  RAISE NOTICE '=======================================================';
  RAISE NOTICE 'WARNING: This will DROP ALL TABLES and DELETE ALL DATA!';
  RAISE NOTICE '=======================================================';
  RAISE NOTICE 'Press Ctrl+C to cancel, or wait 5 seconds to continue...';
  PERFORM pg_sleep(5);
END $$;

-- 롤백 시작 메시지
DO $$
BEGIN
  RAISE NOTICE 'Starting rollback process...';
END $$;

-- 테이블 삭제 (역순)
-- 외래 키 제약 조건 때문에 자식 테이블부터 삭제해야 함

-- Step 6: uploaded_files 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'uploaded_files') THEN
    DROP TABLE uploaded_files CASCADE;
    RAISE NOTICE 'Dropped table: uploaded_files';
  ELSE
    RAISE NOTICE 'Table uploaded_files does not exist, skipping...';
  END IF;
END $$;

-- Step 5: budgets 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'budgets') THEN
    DROP TABLE budgets CASCADE;
    RAISE NOTICE 'Dropped table: budgets';
  ELSE
    RAISE NOTICE 'Table budgets does not exist, skipping...';
  END IF;
END $$;

-- Step 4: students 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'students') THEN
    DROP TABLE students CASCADE;
    RAISE NOTICE 'Dropped table: students';
  ELSE
    RAISE NOTICE 'Table students does not exist, skipping...';
  END IF;
END $$;

-- Step 3: papers 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'papers') THEN
    DROP TABLE papers CASCADE;
    RAISE NOTICE 'Dropped table: papers';
  ELSE
    RAISE NOTICE 'Table papers does not exist, skipping...';
  END IF;
END $$;

-- Step 2: performances 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'performances') THEN
    DROP TABLE performances CASCADE;
    RAISE NOTICE 'Dropped table: performances';
  ELSE
    RAISE NOTICE 'Table performances does not exist, skipping...';
  END IF;
END $$;

-- Step 1: user_profiles 테이블 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_profiles') THEN
    DROP TABLE user_profiles CASCADE;
    RAISE NOTICE 'Dropped table: user_profiles';
  ELSE
    RAISE NOTICE 'Table user_profiles does not exist, skipping...';
  END IF;
END $$;

-- 트리거 함수 삭제
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'update_updated_at_column') THEN
    DROP FUNCTION update_updated_at_column() CASCADE;
    RAISE NOTICE 'Dropped function: update_updated_at_column()';
  ELSE
    RAISE NOTICE 'Function update_updated_at_column() does not exist, skipping...';
  END IF;
END $$;

-- 롤백 완료 메시지
DO $$
BEGIN
  RAISE NOTICE '=======================================================';
  RAISE NOTICE 'Rollback completed successfully!';
  RAISE NOTICE 'All tables and functions have been dropped.';
  RAISE NOTICE '=======================================================';
END $$;

-- 남은 테이블 확인
DO $$
DECLARE
  remaining_tables INTEGER;
BEGIN
  SELECT COUNT(*)
  INTO remaining_tables
  FROM information_schema.tables
  WHERE table_schema = 'public'
    AND table_name IN ('user_profiles', 'performances', 'papers', 'students', 'budgets', 'uploaded_files');

  IF remaining_tables > 0 THEN
    RAISE WARNING 'Warning: % table(s) still remain!', remaining_tables;
  ELSE
    RAISE NOTICE 'Verification: All target tables have been removed.';
  END IF;
END $$;
