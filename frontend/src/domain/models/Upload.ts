/**
 * Upload 도메인 모델
 *
 * CSV 파일 업로드 관련 타입 정의
 */

// CSV 데이터 타입 (4가지)
export type DataType =
  | 'department_kpi'      // 학과 KPI 데이터
  | 'publication'         // 논문 목록
  | 'research_project'    // 연구 과제 데이터
  | 'student_roster';     // 학생 명단

// 업로드 상태
export type UploadStatus =
  | 'success'   // 전체 성공
  | 'partial'   // 부분 성공
  | 'failed';   // 전체 실패

// 업로드 응답
export interface UploadResponse {
  id: number;
  file_name: string;
  data_type: DataType;
  rows_processed: number;  // 처리된 행 수
  status: UploadStatus;
  error_message?: string;  // 오류 메시지 (실패 시)
  uploaded_at: string;     // 업로드 시각 (ISO 8601)
}

// 업로드 이력
export interface UploadHistory {
  id: number;
  file_name: string;
  data_type: DataType;
  rows_processed: number;
  status: UploadStatus;
  error_message: string | null;
  uploaded_by: string;
  uploaded_at: string;
}

// 업로드 요청
export interface UploadRequest {
  file: File;
  data_type: DataType;
}

// 파일 검증 결과
export interface FileValidationResult {
  is_valid: boolean;
  errors: string[];  // 오류 메시지 목록
}
