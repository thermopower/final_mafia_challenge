/**
 * useFileUpload Hook
 *
 * 파일 업로드 상태 관리 및 로직
 */
import { useState } from 'react';
import { uploadApi } from '@/services/api/uploadApi';
import { fileValidator } from '@/services/validators/fileValidator';
import { UploadResult, UploadError, DataType } from '@/domain/models/Upload';

export const useFileUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [dataType, setDataType] = useState<DataType | ''>('');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<UploadError | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const uploadFile = async () => {
    if (!file || !dataType) {
      setError({ error: '파일과 데이터 유형을 선택해주세요' });
      return;
    }

    // 클라이언트 측 검증
    const validation = fileValidator.validateFile(file);
    if (!validation.valid) {
      setError({ error: validation.error || '파일 검증 실패' });
      return;
    }

    setUploading(true);
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('data_type', dataType);

      const response = await uploadApi.uploadExcel(formData, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / (progressEvent.total || 1)
        );
        setProgress(percentCompleted);
      });

      setResult(response);
      setProgress(100);
    } catch (err: any) {
      if (err.response?.data) {
        setError(err.response.data);
      } else {
        setError({ error: '업로드 중 오류가 발생했습니다' });
      }
      setProgress(0);
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setDataType('');
    setProgress(0);
    setError(null);
    setResult(null);
  };

  return {
    file,
    setFile,
    dataType,
    setDataType,
    uploading,
    progress,
    error,
    result,
    uploadFile,
    reset,
  };
};
