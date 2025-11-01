/**
 * Pagination Component
 *
 * 페이지네이션 UI
 */

import React from 'react';
import { Box, Pagination as MuiPagination, FormControl, Select, MenuItem, SelectChangeEvent, Typography } from '@mui/material';

interface PaginationProps {
  totalCount: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
}

export const Pagination: React.FC<PaginationProps> = ({
  totalCount,
  page,
  pageSize,
  onPageChange,
  onPageSizeChange,
}) => {
  const totalPages = Math.ceil(totalCount / pageSize);

  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    onPageChange(value);
  };

  const handlePageSizeChange = (event: SelectChangeEvent) => {
    onPageSizeChange(Number(event.target.value));
    onPageChange(1); // 페이지 크기 변경 시 첫 페이지로 이동
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        mt: 3,
        flexWrap: 'wrap',
        gap: 2,
      }}
    >
      {/* 총 결과 수 표시 */}
      <Typography variant="body2" color="text.secondary">
        총 {totalCount.toLocaleString()}건
      </Typography>

      {/* 페이지네이션 */}
      <MuiPagination
        count={totalPages}
        page={page}
        onChange={handlePageChange}
        color="primary"
        showFirstButton
        showLastButton
      />

      {/* 페이지 크기 선택 */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Typography variant="body2">페이지당</Typography>
        <FormControl size="small">
          <Select value={pageSize.toString()} onChange={handlePageSizeChange}>
            <MenuItem value="20">20개</MenuItem>
            <MenuItem value="50">50개</MenuItem>
            <MenuItem value="100">100개</MenuItem>
          </Select>
        </FormControl>
      </Box>
    </Box>
  );
};
