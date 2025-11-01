/**
 * useDataView Hook
 *
 * 데이터 조회 및 필터링 상태 관리
 */

import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { dataApi } from '@/services/api/dataApi';
import type { DataFilter, PaginatedData } from '@/domain/models/DataView';
import { useDebounce } from './useDebounce';

/**
 * 데이터 조회 훅
 *
 * @param initialFilters 초기 필터 값
 * @returns 데이터 조회 상태 및 제어 함수
 */
export const useDataView = (initialFilters?: DataFilter) => {
  const [searchParams, setSearchParams] = useSearchParams();

  // URL 쿼리 파라미터에서 초기값 로드
  const [filters, setFilters] = useState<DataFilter>({
    type: (searchParams.get('type') as any) || initialFilters?.type,
    year: searchParams.get('year') ? Number(searchParams.get('year')) : initialFilters?.year,
    search: searchParams.get('search') || initialFilters?.search || '',
    ordering: searchParams.get('ordering') || initialFilters?.ordering || '-date',
  });

  const [page, setPage] = useState<number>(
    searchParams.get('page') ? Number(searchParams.get('page')) : 1
  );

  const [pageSize, setPageSize] = useState<number>(
    searchParams.get('page_size') ? Number(searchParams.get('page_size')) : 20
  );

  const [data, setData] = useState<PaginatedData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // 검색어 디바운싱 (300ms)
  const debouncedSearch = useDebounce(filters.search, 300);

  // 데이터 fetch 함수
  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await dataApi.getData(
        { ...filters, search: debouncedSearch },
        page,
        pageSize
      );
      setData(result);
    } catch (err: any) {
      setError(err.response?.data?.error || '데이터를 불러오는 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  // URL 쿼리 파라미터 동기화
  useEffect(() => {
    const params: Record<string, string> = {
      page: page.toString(),
      page_size: pageSize.toString(),
    };

    if (filters.type) params.type = filters.type;
    if (filters.year) params.year = filters.year.toString();
    if (filters.search) params.search = filters.search;
    if (filters.ordering) params.ordering = filters.ordering;

    setSearchParams(params, { replace: true });
  }, [filters, page, pageSize, setSearchParams]);

  // 필터나 페이지 변경 시 데이터 재조회
  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedSearch, filters.type, filters.year, filters.ordering, page, pageSize]);

  return {
    data,
    loading,
    error,
    filters,
    setFilters,
    page,
    setPage,
    pageSize,
    setPageSize,
    refetch: fetchData,
  };
};
