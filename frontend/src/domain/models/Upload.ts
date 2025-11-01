/**
 * Upload 도메인 모델
 */

export interface UploadResult {
  id: number;
  filename: string;
  data_type: string;
  file_size: number;
  rows_processed: number;
  rows_failed: number;
  uploaded_at: string;
  uploaded_by: string;
  status: 'pending' | 'processing' | 'success' | 'failed' | 'partial';
  error_message?: string | null;
  completed_at?: string | null;
}

export interface UploadError {
  error: string;
  details?: {
    missing_columns?: string[];
    current_columns?: string[];
    invalid_rows?: Array<{
      row: number;
      column: string;
      value: string;
      message: string;
    }>;
    duplicates?: Array<{
      row: number;
      key: string;
      message: string;
    }>;
  };
}

export interface PaginatedUploadHistory {
  count: number;
  next: string | null;
  previous: string | null;
  results: UploadResult[];
}

export type DataType = 'performance' | 'paper' | 'student' | 'budget';
