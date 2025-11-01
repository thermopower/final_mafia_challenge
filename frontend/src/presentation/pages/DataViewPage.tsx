/**
 * DataViewPage
 *
 * 데이터 조회 및 필터링 페이지
 */

import React from 'react';
import { Box, Typography, Paper, Alert } from '@mui/material';
import { useDataView } from '@/application/hooks/useDataView';
import { SearchBar } from '../components/data/SearchBar';
import { FilterPanel } from '../components/data/FilterPanel';
import { DataTable } from '../components/data/DataTable';
import { Pagination } from '../components/data/Pagination';
import { Loading } from '../components/common/Loading';
import { ExportButton } from '../components/data/ExportButton';

export const DataViewPage: React.FC = () => {
  const {
    data,
    loading,
    error,
    filters,
    setFilters,
    page,
    setPage,
    pageSize,
    setPageSize,
  } = useDataView();

  return (
    <Box sx={{ p: 3 }}>
      {/* 페이지 제목 및 Export 버튼 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          데이터 조회
        </Typography>
        <ExportButton filters={filters} disabled={loading} />
      </Box>

      {/* 검색 및 필터 */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* 검색 바 */}
          <SearchBar
            value={filters.search || ''}
            onChange={(value) => {
              setFilters({ ...filters, search: value });
              setPage(1); // 검색 시 첫 페이지로 이동
            }}
          />

          {/* 필터 패널 */}
          <FilterPanel
            filters={filters}
            onFilterChange={(newFilters) => {
              setFilters(newFilters);
              setPage(1); // 필터 변경 시 첫 페이지로 이동
            }}
          />
        </Box>
      </Paper>

      {/* 오류 메시지 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* 로딩 상태 */}
      {loading && <Loading message="데이터를 불러오는 중..." />}

      {/* 데이터 테이블 */}
      {!loading && data && (
        <>
          <DataTable data={data.results} />

          {/* 페이지네이션 */}
          {data.count > 0 && (
            <Pagination
              totalCount={data.count}
              page={page}
              pageSize={pageSize}
              onPageChange={setPage}
              onPageSizeChange={setPageSize}
            />
          )}
        </>
      )}
    </Box>
  );
};
