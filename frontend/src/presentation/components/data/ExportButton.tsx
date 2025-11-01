/**
 * ExportButton - CSV 내보내기 버튼 컴포넌트
 *
 * 책임:
 * - CSV 내보내기 기능 제공
 * - 내보내기 상태 표시
 * - 에러 처리
 */
import React from 'react';
import { Button, CircularProgress, Snackbar, Alert } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import { useExport } from '@/application/hooks/useExport';
import type { DataFilter } from '@/domain/models/DataView';

interface ExportButtonProps {
  filters: DataFilter;
  variant?: 'text' | 'outlined' | 'contained';
  disabled?: boolean;
}

export const ExportButton: React.FC<ExportButtonProps> = ({
  filters,
  variant = 'outlined',
  disabled = false,
}) => {
  const { exporting, error, exportToCSV } = useExport();
  const [showError, setShowError] = React.useState(false);

  const handleExport = async () => {
    try {
      await exportToCSV(filters);
    } catch (err) {
      setShowError(true);
    }
  };

  const handleCloseError = () => {
    setShowError(false);
  };

  return (
    <>
      <Button
        variant={variant}
        color="primary"
        onClick={handleExport}
        disabled={disabled || exporting}
        startIcon={exporting ? <CircularProgress size={20} /> : <DownloadIcon />}
      >
        {exporting ? 'Exporting...' : 'Export CSV'}
      </Button>

      {/* Error Snackbar */}
      <Snackbar
        open={showError && error !== null}
        autoHideDuration={6000}
        onClose={handleCloseError}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </>
  );
};
