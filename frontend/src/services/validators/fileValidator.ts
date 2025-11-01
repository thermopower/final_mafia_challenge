/**
 * File Validator
 *
 * 클라이언트 측 파일 검증
 */

export interface ValidationResult {
  valid: boolean;
  error?: string;
}

export const fileValidator = {
  /**
   * 파일 형식 검증
   */
  validateFileType(file: File): ValidationResult {
    const allowedExtensions = ['.xlsx', '.xls'];
    const fileExtension = file.name
      .substring(file.name.lastIndexOf('.'))
      .toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
      return {
        valid: false,
        error: 'Excel 파일(.xlsx, .xls)만 업로드 가능합니다',
      };
    }

    return { valid: true };
  },

  /**
   * 파일 크기 검증
   */
  validateFileSize(file: File, maxSizeMB: number = 10): ValidationResult {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;

    if (file.size > maxSizeBytes) {
      const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      return {
        valid: false,
        error: `파일 크기가 ${maxSizeMB}MB를 초과합니다. (현재: ${fileSizeMB}MB)`,
      };
    }

    return { valid: true };
  },

  /**
   * 전체 검증
   */
  validateFile(file: File): ValidationResult {
    const typeValidation = this.validateFileType(file);
    if (!typeValidation.valid) {
      return typeValidation;
    }

    const sizeValidation = this.validateFileSize(file);
    if (!sizeValidation.valid) {
      return sizeValidation;
    }

    return { valid: true };
  },
};
