/**
 * DataView Domain Models
 *
 * 데이터 조회 및 필터링 관련 타입 정의
 */

export type DataType = 'performance' | 'paper' | 'student' | 'budget';

export interface UnifiedDataItem {
  id: number;
  type: DataType;
  date: string;  // ISO 8601 format
  title: string;
  amount: number | null;
  category: string | null;
  description: string | null;
  uploaded_at: string;  // ISO 8601 format
  uploaded_by: string;
  extra_fields?: Record<string, any>;
}

export interface PaginatedData {
  count: number;
  next: string | null;
  previous: string | null;
  results: UnifiedDataItem[];
}

export interface DataFilter {
  type?: DataType;
  year?: number;
  search?: string;
  ordering?: string;  // '-date' | 'date' | '-amount' | 'amount'
}

export interface DataViewState {
  data: PaginatedData | null;
  loading: boolean;
  error: string | null;
}
