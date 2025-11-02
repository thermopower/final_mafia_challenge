/**
 * Dashboard 도메인 모델
 *
 * 백엔드 API 응답 타입 정의
 * 실제 CSV 데이터 타입과 database.md 스키마에 맞춰 작성
 */

// ==================== 대시보드 전체 요약 ====================

export interface DashboardSummary {
  kpi_summary: KPISummary;
  publication_stats: PublicationStats;
  student_stats: StudentStats;
  budget_summary: BudgetSummary;
}

// ==================== 학과 KPI 관련 ====================

export interface KPISummary {
  avg_employment_rate: number;  // 평균 취업률 (%)
  total_full_time_faculty: number;  // 전임교원 총 인원
  total_visiting_faculty: number;  // 초빙교원 총 인원
  total_tech_transfer_income: number;  // 기술이전 수입 총액 (억원)
  total_intl_conferences: number;  // 국제학술대회 개최 총 횟수
  by_college: KPIByCollege[];  // 단과대학별 집계
}

export interface KPIByCollege {
  college: string;  // 단과대학명
  avg_employment_rate: number;  // 평균 취업률
  total_faculty: number;  // 총 교원 수 (전임 + 초빙)
}

export interface DepartmentKPI {
  id: number;
  evaluation_year: number;  // 평가년도
  college: string;  // 단과대학
  department: string;  // 학과
  employment_rate: number;  // 졸업생 취업률 (%)
  full_time_faculty: number;  // 전임교원 수 (명)
  visiting_faculty: number;  // 초빙교원 수 (명)
  tech_transfer_income: number;  // 기술이전 수입액 (억원)
  intl_conferences: number;  // 국제학술대회 개최 횟수
}

// ==================== 논문 관련 ====================

export interface PublicationStats {
  total_papers: number;  // 총 논문 수
  scie_count: number;  // SCIE 논문 수
  kci_count: number;  // KCI 논문 수
  avg_impact_factor: number;  // 평균 Impact Factor (SCIE만)
  project_linked_ratio: number;  // 과제 연계 논문 비율 (0~1)
  by_department: PublicationByDepartment[];  // 학과별 논문 수
}

export interface PublicationByDepartment {
  department: string;  // 학과명
  count: number;  // 논문 수
}

export interface Publication {
  id: number;
  paper_id: string;  // 논문 ID (PUB-YY-NNN)
  publication_date: string;  // 게재일 (YYYY-MM-DD)
  college: string;  // 단과대학
  department: string;  // 학과
  paper_title: string;  // 논문 제목
  lead_author: string;  // 주저자
  co_authors: string | null;  // 참여저자 (세미콜론 구분)
  journal_name: string;  // 학술지명
  journal_grade: 'SCIE' | 'KCI';  // 저널 등급
  impact_factor: number | null;  // Impact Factor
  project_linked: 'Y' | 'N';  // 과제연계여부
}

// ==================== 학생 관련 ====================

export interface StudentStats {
  total_students: number;  // 총 학생 수
  by_program: StudentByProgram[];  // 과정별 학생 수
  by_status: StudentByStatus[];  // 학적 상태별 학생 수
  by_department: StudentByDepartment[];  // 학과별 학생 수
}

export interface StudentByProgram {
  program_type: string;  // 과정 구분 (학사/석사/박사)
  count: number;  // 학생 수
}

export interface StudentByStatus {
  enrollment_status: string;  // 학적 상태 (재학/휴학/졸업)
  count: number;  // 학생 수
}

export interface StudentByDepartment {
  department: string;  // 학과명
  count: number;  // 학생 수
}

export interface Student {
  id: number;
  student_id: string;  // 학번 (YYYYMMNNN)
  name: string;  // 이름
  college: string;  // 단과대학
  department: string;  // 학과
  grade: number;  // 학년 (0~4)
  program_type: '학사' | '석사' | '박사';  // 과정 구분
  enrollment_status: '재학' | '휴학' | '졸업';  // 학적 상태
  gender: '남' | '여';  // 성별
  admission_year: number;  // 입학년도
  advisor: string | null;  // 지도교수
  email: string;  // 이메일
}

// ==================== 예산 관련 ====================

export interface BudgetSummary {
  total_budget: number;  // 총 연구비 (원)
  total_execution: number;  // 총 집행액 (원)
  execution_rate: number;  // 집행률 (0~1)
  by_item: BudgetByItem[];  // 집행 항목별 집계
  by_agency: BudgetByAgency[];  // 지원 기관별 집계
}

export interface BudgetByItem {
  execution_item: string;  // 집행 항목명
  total_amount: number;  // 총 집행액 (원)
}

export interface BudgetByAgency {
  funding_agency: string;  // 지원 기관명
  total_budget: number;  // 총 연구비 (원)
}

export interface ResearchProject {
  id: number;
  execution_id: string;  // 집행 ID (T2324NNN)
  project_number: string;  // 과제번호
  project_name: string;  // 과제명
  principal_investigator: string;  // 연구책임자
  department: string;  // 소속학과
  funding_agency: string;  // 지원기관
  total_budget: number;  // 총 연구비 (원)
  execution_date: string;  // 집행일자 (YYYY-MM-DD)
  execution_item: string;  // 집행 항목
  execution_amount: number;  // 집행 금액 (원)
  status: '집행완료' | '처리중';  // 상태
  remarks: string | null;  // 비고
}

// ==================== KPI 메트릭 ====================

export interface KPIMetric {
  value: number;  // 지표 값
  unit: string;  // 단위 (%, 명, 억원 등)
  change_rate: number;  // 전년 대비 증감률 (%)
  trend: 'up' | 'down' | 'neutral';  // 추세 방향
}
