/**
 * DataTable Component
 *
 * 데이터 테이블 UI
 */

import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Typography,
} from '@mui/material';
import type { UnifiedDataItem } from '@/domain/models/DataView';
import { formatters } from '@/utils/formatters';

interface DataTableProps {
  data: UnifiedDataItem[];
  loading?: boolean;
}

export const DataTable: React.FC<DataTableProps> = ({ data, loading }) => {
  // 데이터 유형별 색상
  const getTypeColor = (type: string): 'primary' | 'success' | 'warning' | 'info' => {
    const mapping: Record<string, 'primary' | 'success' | 'warning' | 'info'> = {
      performance: 'primary',
      paper: 'success',
      student: 'warning',
      budget: 'info',
    };
    return mapping[type] || 'primary';
  };

  // 데이터 유형별 한글 라벨
  const getTypeLabel = (type: string): string => {
    const mapping: Record<string, string> = {
      performance: '실적',
      paper: '논문',
      student: '학생',
      budget: '예산',
    };
    return mapping[type] || type;
  };

  if (loading) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body1">데이터를 불러오는 중...</Typography>
      </Paper>
    );
  }

  if (data.length === 0) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body1">조회 가능한 데이터가 없습니다</Typography>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>유형</TableCell>
            <TableCell>날짜</TableCell>
            <TableCell>제목/항목</TableCell>
            <TableCell align="right">금액</TableCell>
            <TableCell>카테고리</TableCell>
            <TableCell>업로드 사용자</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item) => (
            <TableRow key={`${item.type}-${item.id}`} hover>
              <TableCell>
                <Chip
                  label={getTypeLabel(item.type)}
                  color={getTypeColor(item.type)}
                  size="small"
                />
              </TableCell>
              <TableCell>{formatters.formatDate(item.date)}</TableCell>
              <TableCell>{item.title}</TableCell>
              <TableCell align="right">
                {item.amount !== null ? formatters.formatCurrency(item.amount) : '-'}
              </TableCell>
              <TableCell>{item.category || '-'}</TableCell>
              <TableCell>{item.uploaded_by}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
