/**
 * Upload Page
 *
 * Excel 파일 업로드 페이지
 */
import React from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress,
  Alert,
} from '@mui/material';
import { useFileUpload } from '@/application/hooks/useFileUpload';
import { DataType } from '@/domain/models/Upload';

const UploadPage: React.FC = () => {
  const {
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
  } = useFileUpload();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = () => {
    uploadFile();
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Excel 파일 업로드
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* 데이터 유형 선택 */}
          <FormControl fullWidth>
            <InputLabel>데이터 유형</InputLabel>
            <Select
              value={dataType}
              label="데이터 유형"
              onChange={(e) => setDataType(e.target.value as DataType)}
              disabled={uploading}
            >
              <MenuItem value="performance">실적</MenuItem>
              <MenuItem value="paper">논문</MenuItem>
              <MenuItem value="student">학생</MenuItem>
              <MenuItem value="budget">예산</MenuItem>
            </Select>
          </FormControl>

          {/* 파일 선택 */}
          <Box>
            <Button variant="outlined" component="label" disabled={uploading}>
              파일 선택
              <input type="file" hidden onChange={handleFileChange} accept=".xlsx,.xls" />
            </Button>
            {file && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                선택된 파일: {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </Typography>
            )}
          </Box>

          {/* 업로드 버튼 */}
          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={!file || !dataType || uploading}
          >
            {uploading ? '업로드 중...' : '업로드'}
          </Button>

          {/* 프로그레스 바 */}
          {uploading && (
            <Box>
              <LinearProgress variant="determinate" value={progress} />
              <Typography variant="body2" align="center" sx={{ mt: 1 }}>
                {progress}%
              </Typography>
            </Box>
          )}

          {/* 에러 메시지 */}
          {error && (
            <Alert severity="error" onClose={reset}>
              {error.error}
              {error.details && (
                <Box sx={{ mt: 1 }}>
                  {error.details.missing_columns && (
                    <Typography variant="body2">
                      누락된 컬럼: {error.details.missing_columns.join(', ')}
                    </Typography>
                  )}
                  {error.details.invalid_rows && (
                    <Box>
                      <Typography variant="body2">데이터 형식 오류:</Typography>
                      {error.details.invalid_rows.slice(0, 5).map((err, idx) => (
                        <Typography key={idx} variant="caption" display="block">
                          - {err.row}행 {err.column}: {err.message}
                        </Typography>
                      ))}
                    </Box>
                  )}
                </Box>
              )}
            </Alert>
          )}

          {/* 성공 메시지 */}
          {result && (
            <Alert severity="success" onClose={reset}>
              업로드 성공! {result.rows_processed}행이 처리되었습니다.
            </Alert>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default UploadPage;
