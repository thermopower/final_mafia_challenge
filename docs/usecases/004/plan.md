# UC-004: 데이터 조회 및 필터링 - 구현 계획

## 1. 개요

### 1.1 기능 요약
- **목적**: 모든 로그인 사용자가 업로드된 데이터를 테이블 형식으로 조회하고 필터링
- **핵심 기능**:
  - 페이지네이션 (기본 20건, 50/100건 선택 가능)
  - 필터링 (데이터 유형, 기간, 검색어)
  - 정렬 (테이블 헤더 클릭)
  - 검색어 디바운싱 (500ms)
  - 상세 정보 모달
  - 관리자 전용 수정/삭제 기능
- **사용자**: 모든 로그인 사용자

### 1.2 아키텍처 원칙
- **Layered Architecture**: Infrastructure → Presentation → Service → Repository → Domain → Persistence
- **SOLID 원칙 준수**
- **TDD**: Red-Green-Refactor
- **공통 모듈 최대 활용**

---

## 2. Backend 구현

### 2.1 Backend 모듈 구조

#### 2.1.1 Presentation Layer

**API 엔드포인트**:
```
GET /api/data/
Query Parameters:
  - page: int (기본값: 1)
  - page_size: int (기본값: 20, 허용값: 20/50/100)
  - ordering: str (기본값: -date, 허용값: date/-date/amount/-amount)
  - type: str (optional, 예: performance/paper/student/budget)
  - year: int (optional)
  - search: str (optional, 최소 2자)

Response 200 OK:
{
  "count": 150,
  "next": "/api/data/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "type": "performance",
      "date": "2024-01-15",
      "title": "연구과제 A",
      "amount": 1000000,
      "category": "실적A",
      "description": "설명...",
      "uploaded_at": "2024-11-01T10:30:00Z",
      "uploaded_by": "admin@university.ac.kr"
    },
    ...
  ]
}

GET /api/data/{id}/
Response 200 OK:
{
  "id": 1,
  "type": "performance",
  "date": "2024-01-15",
  "title": "연구과제 A",
  "amount": 1000000,
  "category": "실적A",
  "description": "설명...",
  "uploaded_at": "2024-11-01T10:30:00Z",
  "uploaded_by": "admin@university.ac.kr"
}
```

#### 2.1.2 Service Layer

**주요 메서드**:
```python
class DataQueryService:
    def get_filtered_data(self, filters: Dict, page: int, page_size: int, ordering: str) -> PaginatedDataResult:
        """필터링 및 페이지네이션 적용된 데이터 조회"""
        pass

    def search_data(self, search_query: str, data_type: str) -> List[Data]:
        """검색어로 데이터 조회"""
        pass
```

#### 2.1.3 Repository Layer

**주요 메서드**:
```python
class DataRepository:
    def get_all_with_filters(self, filters: Dict, page: int, page_size: int, ordering: str) -> PaginatedResult:
        """필터 및 페이지네이션 적용"""
        pass

    def search_by_keyword(self, keyword: str, data_type: str) -> List[Data]:
        """키워드 검색 (title, description, category)"""
        pass
```

---

## 3. Frontend 구현

### 3.1 Frontend 모듈 구조

#### 3.1.1 Application Layer

**주요 훅**:
```typescript
// useDataQuery.ts
export const useDataQuery = (initialFilters?: Filters) => {
  const [data, setData] = useState<PaginatedData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>(initialFilters || defaultFilters);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [ordering, setOrdering] = useState('-date');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await dataApi.getData(filters, page, pageSize, ordering);
      setData(response);
    } catch (err) {
      setError('데이터를 불러오는 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filters, page, pageSize, ordering]);

  return { data, loading, error, filters, setFilters, page, setPage, pageSize, setPageSize, ordering, setOrdering, refetch: fetchData };
};
```

```typescript
// useSearchDebounce.ts
export const useSearchDebounce = (value: string, delay: number = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

#### 3.1.2 Presentation Layer

**파일**:
- `frontend/src/presentation/pages/DataViewPage.tsx`
- `frontend/src/presentation/components/data/DataTable.tsx`
- `frontend/src/presentation/components/data/FilterBar.tsx`
- `frontend/src/presentation/components/data/SearchBox.tsx`
- `frontend/src/presentation/components/data/Pagination.tsx`
- `frontend/src/presentation/components/data/DetailModal.tsx`

---

## 4. TDD 구현 계획

### 4.1 Backend TDD 시나리오

**Test Case 1: DataRepository - 필터링**
```python
@pytest.mark.django_db
class TestDataRepository:
    def test_get_all_with_type_filter_returns_filtered_data(self):
        PerformanceFactory.create_batch(5, year=2024)
        PaperFactory.create_batch(3, year=2024)

        repo = DataRepository()
        result = repo.get_all_with_filters({'type': 'performance'}, page=1, page_size=20, ordering='-date')

        assert result.count == 5

    def test_search_by_keyword_finds_matching_records(self):
        PerformanceFactory.create(title='연구과제 A')
        PerformanceFactory.create(title='기타 B')

        repo = DataRepository()
        result = repo.search_by_keyword('연구과제', 'performance')

        assert len(result) == 1
        assert result[0].title == '연구과제 A'
```

**Test Case 2: DataQueryService - 페이지네이션**
```python
class TestDataQueryService:
    def test_get_filtered_data_applies_pagination(self, mocker):
        mock_repo = mocker.Mock(spec=DataRepository)
        mock_repo.get_all_with_filters.return_value = PaginatedResult(count=50, results=[...])

        service = DataQueryService(data_repo=mock_repo)
        result = service.get_filtered_data({}, page=1, page_size=20, ordering='-date')

        assert result.count == 50
        assert len(result.results) <= 20
```

**Test Case 3: DataViewSet - API**
```python
@pytest.mark.django_db
class TestDataViewSet:
    def test_get_data_with_filters_returns_200(self, api_client, auth_token):
        PerformanceFactory.create_batch(5, year=2024)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

        response = api_client.get('/api/data/', {'year': 2024})

        assert response.status_code == 200
        assert response.data['count'] == 5
```

### 4.2 Frontend TDD 시나리오

**Test Case 4: useSearchDebounce 훅**
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useSearchDebounce } from '../useSearchDebounce';

describe('useSearchDebounce', () => {
  it('입력 후 500ms 지연하여 값을 업데이트한다', async () => {
    const { result, rerender } = renderHook(
      ({ value }) => useSearchDebounce(value, 500),
      { initialProps: { value: 'test' } }
    );

    expect(result.current).toBe('test');

    rerender({ value: 'updated' });
    expect(result.current).toBe('test'); // 아직 업데이트되지 않음

    await waitFor(() => expect(result.current).toBe('updated'), { timeout: 600 });
  });
});
```

**Test Case 5: DataTable 컴포넌트**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import DataTable from '../DataTable';

describe('DataTable', () => {
  it('데이터 행을 렌더링한다', () => {
    const data = [
      { id: 1, date: '2024-01-15', title: '연구과제 A', amount: 1000000 }
    ];

    render(<DataTable data={data} />);

    expect(screen.getByText('연구과제 A')).toBeInTheDocument();
    expect(screen.getByText('1,000,000')).toBeInTheDocument();
  });

  it('테이블 헤더 클릭 시 정렬을 변경한다', () => {
    const onSortMock = vi.fn();
    render(<DataTable data={[]} onSort={onSortMock} />);

    const dateHeader = screen.getByText('날짜');
    fireEvent.click(dateHeader);

    expect(onSortMock).toHaveBeenCalledWith('date');
  });
});
```

---

## 5. 파일 생성 순서 (TDD 기반)

### 5.1 Backend
```
1. Domain Layer
   └── backend/apps/data/domain/models.py

2. Repository Layer
   ├── backend/apps/data/tests/test_repositories.py
   └── backend/apps/data/repositories/data_repository.py

3. Service Layer
   ├── backend/apps/data/tests/test_services.py
   └── backend/apps/data/services/data_query_service.py

4. Presentation Layer
   ├── backend/apps/data/tests/test_views.py
   ├── backend/apps/data/presentation/serializers.py
   ├── backend/apps/data/presentation/views.py
   └── backend/apps/data/presentation/urls.py
```

### 5.2 Frontend
```
1. Domain Layer
   └── frontend/src/domain/models/Data.ts

2. Service Layer
   ├── frontend/src/services/api/__tests__/dataApi.test.ts
   └── frontend/src/services/api/dataApi.ts

3. Application Layer
   ├── frontend/src/application/hooks/__tests__/useDataQuery.test.ts
   ├── frontend/src/application/hooks/useDataQuery.ts
   ├── frontend/src/application/hooks/__tests__/useSearchDebounce.test.ts
   └── frontend/src/application/hooks/useSearchDebounce.ts

4. Presentation Layer
   ├── frontend/src/presentation/components/data/__tests__/DataTable.test.tsx
   ├── frontend/src/presentation/components/data/DataTable.tsx
   ├── frontend/src/presentation/components/data/FilterBar.tsx
   ├── frontend/src/presentation/components/data/Pagination.tsx
   └── frontend/src/presentation/pages/DataViewPage.tsx
```

---

## 6. 성공 기준

### 6.1 Backend
- [ ] 필터링 (데이터 유형, 기간) 정상 작동
- [ ] 검색 (title, description, category 부분 일치) 정상
- [ ] 페이지네이션 (오프셋 기반) 정상
- [ ] 정렬 (date, amount 오름차순/내림차순) 정상
- [ ] API 응답 시간 500ms 이내

### 6.2 Frontend
- [ ] 데이터 테이블 렌더링 정상
- [ ] 필터 적용 시 데이터 갱신 정상
- [ ] 검색 디바운싱 (500ms) 정상
- [ ] 페이지네이션 UI 정상
- [ ] URL 쿼리 파라미터 동기화 정상
- [ ] 상세 모달 정상
- [ ] 관리자 전용 수정/삭제 버튼 표시

---

## 7. 마무리

이 계획서는 UC-004 (데이터 조회 및 필터링) 기능을 TDD 원칙에 따라 구현하기 위한 가이드입니다.

**핵심 원칙**:
1. **테스트 먼저 작성**
2. **페이지네이션 및 필터링 로직 분리**
3. **검색 디바운싱**으로 성능 최적화
4. **URL 쿼리 파라미터 동기화**로 공유 가능한 링크 제공
