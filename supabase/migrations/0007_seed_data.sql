-- Migration: 0007_seed_data
-- Description: 개발/테스트용 시드 데이터 삽입
-- Created: 2024-11-01
-- Author: System
-- Note: 프로덕션 환경에서는 실행하지 않음

-- WARNING: 이 마이그레이션은 개발/테스트 환경에서만 실행하세요!
-- 프로덕션에서 실행하려면 아래 주석을 해제하고 실행하세요:
-- DO $$
-- BEGIN
--   IF current_setting('server_version_num')::int >= 120000 THEN
--     RAISE EXCEPTION 'This migration should not run in production!';
--   END IF;
-- END $$;

-- 1. 시스템 사용자 및 테스트 사용자 생성
-- Note: 실제로는 Supabase Auth에서 사용자를 먼저 생성해야 합니다.
-- 여기서는 예시 UUID를 사용합니다.

INSERT INTO user_profiles (id, email, full_name, department, role, is_active)
VALUES
  -- 관리자 계정
  ('a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, 'admin@university.ac.kr', '관리자', '전산팀', 'admin', TRUE),

  -- 일반 사용자 계정
  ('b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid, 'user@university.ac.kr', '홍길동', '컴퓨터공학과', 'user', TRUE),
  ('c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid, 'user2@university.ac.kr', '김철수', '전자공학과', 'user', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 2. 샘플 실적 데이터 삽입
INSERT INTO performances (date, title, amount, category, description, uploaded_by)
VALUES
  -- 2024년 데이터
  ('2024-01-15', '연구과제 A', 1200000.00, '연구비', '정부지원 연구과제', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-02-20', '특허 출원', 500000.00, '특허료', 'AI 기반 이미지 처리 특허', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-03-10', '기술이전', 3000000.00, '기술료', '빅데이터 분석 플랫폼 기술이전', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-04-05', '산학협력 프로젝트', 2500000.00, '연구비', 'A기업과의 공동 연구', 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),
  ('2024-05-12', '정부과제', 5000000.00, '연구비', '과학기술정보통신부 과제', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-06-20', '특허 등록', 800000.00, '특허료', '블록체인 보안 기술 특허', 'c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid),
  ('2024-07-15', '연구용역', 1500000.00, '용역비', 'B기업 데이터 분석 용역', 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),
  ('2024-08-10', '기술지도', 1000000.00, '자문료', 'C기업 기술지도', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024-09-05', '국제공동연구', 4000000.00, '연구비', '미국 대학과의 공동 연구', 'c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid),
  ('2024-10-20', '기술이전', 2000000.00, '기술료', 'IoT 센서 기술 이전', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 2023년 데이터 (전년 대비 분석용)
  ('2023-01-10', '연구과제 X', 1000000.00, '연구비', '2023년 연구과제', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023-06-15', '특허 출원', 400000.00, '특허료', '2023년 특허', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023-12-20', '기술이전', 2500000.00, '기술료', '2023년 기술이전', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 3. 샘플 논문 데이터 삽입
INSERT INTO papers (title, authors, publication_date, field, journal_name, doi, uploaded_by)
VALUES
  -- 2024년 논문
  ('딥러닝을 활용한 이미지 분류 기술', '홍길동, 김철수', '2024-01-20', '국제학술지', 'IEEE Transactions on AI', '10.1109/TAI.2024.001', 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),
  ('빅데이터 분석 기법 연구', '이영희', '2024-02-15', '국내학술지', '한국컴퓨터학회 논문지', NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('블록체인 기반 보안 프로토콜', '박민수, 최지연', '2024-03-10', '국제학술지', 'ACM Computing Surveys', '10.1145/ACS.2024.002', 'c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid),
  ('IoT 센서 네트워크 최적화', '김철수', '2024-04-25', '학술대회', 'IEEE IoT Conference 2024', NULL, 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),
  ('인공지능 윤리 연구', '홍길동, 이영희, 박민수', '2024-05-30', '국내학술지', '정보과학회 논문지', NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('양자 컴퓨팅 알고리즘 개발', '최지연', '2024-06-15', '국제학술지', 'Nature Computing', '10.1038/NC.2024.003', 'c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid),
  ('클라우드 컴퓨팅 보안 연구', '김철수, 박민수', '2024-07-20', '학술대회', 'Cloud Security Summit 2024', NULL, 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),
  ('머신러닝 기반 의료 진단 시스템', '홍길동', '2024-08-10', '국제학술지', 'Medical AI Journal', '10.1234/MAI.2024.004', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('5G 네트워크 최적화', '이영희, 최지연', '2024-09-05', '국내학술지', '통신학회 논문지', NULL, 'c3d4e5f6-a7b8-9012-cdef-123456789012'::uuid),
  ('사이버 보안 위협 탐지', '박민수', '2024-10-12', '학술대회', 'CyberSec 2024', NULL, 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid),

  -- 2023년 논문 (전년 대비 분석용)
  ('2023년 AI 연구', '홍길동', '2023-03-15', '국제학술지', 'AI Research Journal', '10.1234/AIR.2023.001', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023년 빅데이터 연구', '김철수', '2023-07-20', '국내학술지', '데이터과학회 논문지', NULL, 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid);

-- 4. 샘플 학생 데이터 삽입
INSERT INTO students (student_id, name, department, grade, status, uploaded_by)
VALUES
  -- 컴퓨터공학과
  ('2021001', '김학생', '컴퓨터공학과', 3, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2022001', '이학생', '컴퓨터공학과', 2, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023001', '박학생', '컴퓨터공학과', 1, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2024001', '최학생', '컴퓨터공학과', 1, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 전자공학과
  ('2021002', '강학생', '전자공학과', 3, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2022002', '정학생', '전자공학과', 2, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023002', '윤학생', '전자공학과', 1, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 기계공학과
  ('2021003', '조학생', '기계공학과', 3, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2022003', '임학생', '기계공학과', 2, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023003', '한학생', '기계공학과', 1, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 대학원생
  ('2023G01', '오석사', '컴퓨터공학과', 5, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2023G02', '나박사', '전자공학과', 6, 'active', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 졸업생/휴학생
  ('2020001', '졸업생', '컴퓨터공학과', 4, 'graduated', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('2022004', '휴학생', '기계공학과', 2, 'withdrawn', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 5. 샘플 예산 데이터 삽입
INSERT INTO budgets (item, amount, category, fiscal_year, quarter, description, uploaded_by)
VALUES
  -- 2024년 1분기
  ('교직원 급여', 50000000.00, '인건비', 2024, 1, '2024년 1분기 교직원 급여', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('연구 장비 구입', 30000000.00, '연구비', 2024, 1, '실험실 장비 구입', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('사무용품', 5000000.00, '운영비', 2024, 1, '사무용품 및 소모품', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('학회 참가비', 8000000.00, '기타', 2024, 1, '국제학회 참가', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 2024년 2분기
  ('교직원 급여', 50000000.00, '인건비', 2024, 2, '2024년 2분기 교직원 급여', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('연구재료비', 15000000.00, '연구비', 2024, 2, '실험 재료 구입', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('전기/수도 요금', 10000000.00, '운영비', 2024, 2, '공과금', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('도서 구입', 7000000.00, '기타', 2024, 2, '학술 도서 구입', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 2024년 3분기
  ('교직원 급여', 50000000.00, '인건비', 2024, 3, '2024년 3분기 교직원 급여', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('소프트웨어 라이선스', 20000000.00, '연구비', 2024, 3, 'MATLAB, SolidWorks 라이선스', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('건물 유지보수', 12000000.00, '운영비', 2024, 3, '건물 수리 및 청소', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 2024년 4분기
  ('교직원 급여', 50000000.00, '인건비', 2024, 4, '2024년 4분기 교직원 급여', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('실험 장비 교체', 25000000.00, '연구비', 2024, 4, '노후 장비 교체', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('냉난방비', 15000000.00, '운영비', 2024, 4, '겨울 난방비', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),

  -- 2023년 데이터 (전년 대비 분석용)
  ('교직원 급여', 45000000.00, '인건비', 2023, 1, '2023년 1분기 교직원 급여', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid),
  ('연구 장비 구입', 25000000.00, '연구비', 2023, 1, '2023년 실험실 장비', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid);

-- 6. 샘플 업로드 파일 이력 삽입
INSERT INTO uploaded_files (filename, data_type, file_size, rows_processed, rows_failed, status, uploaded_by, uploaded_at, completed_at)
VALUES
  ('실적_2024_01.xlsx', 'performance', 52480, 10, 0, 'success', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, '2024-01-20 10:30:00', '2024-01-20 10:30:15'),
  ('논문_2024_상반기.xlsx', 'paper', 73920, 8, 0, 'success', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, '2024-06-25 14:20:00', '2024-06-25 14:20:10'),
  ('학생_명단_2024.xlsx', 'student', 98560, 14, 0, 'success', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, '2024-09-01 09:00:00', '2024-09-01 09:00:08'),
  ('예산_2024.xlsx', 'budget', 61440, 15, 0, 'success', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid, '2024-01-05 11:15:00', '2024-01-05 11:15:12'),
  ('실적_오류.xlsx', 'performance', 45120, 5, 3, 'failed', 'b2c3d4e5-f6a7-8901-bcde-f12345678901'::uuid, '2024-10-15 16:45:00', '2024-10-15 16:45:05');

-- 마이그레이션 완료 메시지
DO $$
BEGIN
  RAISE NOTICE 'Seed data migration completed successfully!';
  RAISE NOTICE 'Created % user profiles', (SELECT COUNT(*) FROM user_profiles);
  RAISE NOTICE 'Created % performances', (SELECT COUNT(*) FROM performances);
  RAISE NOTICE 'Created % papers', (SELECT COUNT(*) FROM papers);
  RAISE NOTICE 'Created % students', (SELECT COUNT(*) FROM students);
  RAISE NOTICE 'Created % budgets', (SELECT COUNT(*) FROM budgets);
  RAISE NOTICE 'Created % upload records', (SELECT COUNT(*) FROM uploaded_files);
END $$;
