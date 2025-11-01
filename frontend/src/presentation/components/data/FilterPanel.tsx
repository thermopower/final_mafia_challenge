/**
 * FilterPanel Component
 *
 * 필터 옵션 UI (데이터 유형, 연도)
 */

import React from 'react';
import { Box, FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';
import type { DataType, DataFilter } from '@/domain/models/DataView';

interface FilterPanelProps {
  filters: DataFilter;
  onFilterChange: (filters: DataFilter) => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({ filters, onFilterChange }) => {
  const handleTypeChange = (event: SelectChangeEvent) => {
    const value = event.target.value;
    onFilterChange({
      ...filters,
      type: value === 'all' ? undefined : (value as DataType),
    });
  };

  const handleYearChange = (event: SelectChangeEvent) => {
    const value = event.target.value;
    onFilterChange({
      ...filters,
      year: value === 'all' ? undefined : Number(value),
    });
  };

  const handleOrderingChange = (event: SelectChangeEvent) => {
    onFilterChange({
      ...filters,
      ordering: event.target.value,
    });
  };

  // 현재 연도부터 과거 5년
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 5 }, (_, i) => currentYear - i);

  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
      {/* 데이터 유형 필터 */}
      <FormControl size="small" sx={{ minWidth: 150 }}>
        <InputLabel>데이터 유형</InputLabel>
        <Select
          value={filters.type || 'all'}
          label="데이터 유형"
          onChange={handleTypeChange}
        >
          <MenuItem value="all">전체</MenuItem>
          <MenuItem value="performance">실적</MenuItem>
          <MenuItem value="paper">논문</MenuItem>
          <MenuItem value="student">학생</MenuItem>
          <MenuItem value="budget">예산</MenuItem>
        </Select>
      </FormControl>

      {/* 연도 필터 */}
      <FormControl size="small" sx={{ minWidth: 120 }}>
        <InputLabel>연도</InputLabel>
        <Select
          value={filters.year?.toString() || 'all'}
          label="연도"
          onChange={handleYearChange}
        >
          <MenuItem value="all">전체</MenuItem>
          {years.map((year) => (
            <MenuItem key={year} value={year}>
              {year}년
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* 정렬 필터 */}
      <FormControl size="small" sx={{ minWidth: 150 }}>
        <InputLabel>정렬</InputLabel>
        <Select
          value={filters.ordering || '-date'}
          label="정렬"
          onChange={handleOrderingChange}
        >
          <MenuItem value="-date">날짜 (최신순)</MenuItem>
          <MenuItem value="date">날짜 (오래된순)</MenuItem>
          <MenuItem value="-amount">금액 (높은순)</MenuItem>
          <MenuItem value="amount">금액 (낮은순)</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
};
