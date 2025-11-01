# UC-005: 데이터 내보내기 (CSV) - 구현 계획

## 1. 개요

### 1.1 기능 요약
- **목적**: 필터링된 데이터를 CSV 파일로 다운로드
- **핵심 기능**:
  - 현재 필터 조건으로 CSV 생성
  - UTF-8 with BOM 인코딩 (Excel 한글 호환)
  - 대용량 데이터 경고 (10,000건 초과)
  - 비동기 처리 (100,000건 초과)
- **사용자**: 모든 로그인 사용자

### 1.2 아키텍처 원칙
- **Layered Architecture**
- **SOLID 원칙**
- **TDD**

---

## 2. Backend 구현

### 2.1 API 엔드포인트

```
GET /api/data/export/csv/
Query Parameters:
  - type: str (optional)
  - year: int (optional)
  - search: str (optional)

Response 200 OK:
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="data_export_20241101_103000.csv"

날짜,유형,항목,금액,카테고리,설명
2024-01-15,실적,연구과제 A,1000000,실적A,"설명..."
...
```

### 2.2 Service Layer

**주요 메서드**:
```python
class DataExportService:
    def export_to_csv(self, filters: Dict) -> str:
        """CSV 파일 생성 및 경로 반환"""
        pass

    def _generate_csv_content(self, data: List[Data]) -> str:
        """CSV 콘텐츠 생성 (UTF-8 with BOM)"""
        pass

    def _get_headers(self, data_type: str) -> List[str]:
        """데이터 유형별 CSV 헤더"""
        pass
```

---

## 3. Frontend 구현

### 3.1 Service Layer

```typescript
export const dataApi = {
  async exportCSV(filters: Filters): Promise<Blob> {
    const response = await client.get('/data/export/csv/', {
      params: filters,
      responseType: 'blob'
    });
    return response.data;
  }
};
```

### 3.2 Application Layer

```typescript
export const useCSVExport = () => {
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const exportCSV = async (filters: Filters) => {
    setExporting(true);
    setError(null);

    try {
      const blob = await dataApi.exportCSV(filters);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `data_export_${new Date().toISOString().replace(/:/g, '-')}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('CSV 다운로드 중 오류가 발생했습니다');
    } finally {
      setExporting(false);
    }
  };

  return { exporting, error, exportCSV };
};
```

---

## 4. TDD 구현 계획

### 4.1 Backend TDD

**Test Case 1: DataExportService - CSV 생성**
```python
class TestDataExportService:
    def test_export_to_csv_generates_utf8_bom_file(self):
        data = [
            Data(date='2024-01-15', title='연구과제 A', amount=Decimal('1000000'))
        ]
        service = DataExportService()

        csv_content = service._generate_csv_content(data)

        assert csv_content.startswith('\ufeff')  # BOM
        assert '날짜' in csv_content
        assert '연구과제 A' in csv_content
```

**Test Case 2: DataExportViewSet - API**
```python
@pytest.mark.django_db
class TestDataExportViewSet:
    def test_export_csv_returns_file(self, api_client, auth_token):
        PerformanceFactory.create_batch(5, year=2024)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')

        response = api_client.get('/api/data/export/csv/', {'year': 2024})

        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv; charset=utf-8'
        assert 'attachment' in response['Content-Disposition']
```

### 4.2 Frontend TDD

**Test Case 3: useCSVExport 훅**
```typescript
import { renderHook, act } from '@testing-library/react';
import { useCSVExport } from '../useCSVExport';
import { dataApi } from '@/services/api/dataApi';

vi.mock('@/services/api/dataApi');

describe('useCSVExport', () => {
  it('exportCSV 호출 시 파일 다운로드를 트리거한다', async () => {
    const mockBlob = new Blob(['csv content'], { type: 'text/csv' });
    (dataApi.exportCSV as any).mockResolvedValue(mockBlob);

    const { result } = renderHook(() => useCSVExport());

    await act(async () => {
      await result.current.exportCSV({ year: 2024 });
    });

    expect(dataApi.exportCSV).toHaveBeenCalledWith({ year: 2024 });
    expect(result.current.exporting).toBe(false);
  });
});
```

---

## 5. 파일 생성 순서

### 5.1 Backend
```
1. Service Layer
   ├── backend/apps/data/tests/test_export_service.py
   └── backend/apps/data/services/data_export_service.py

2. Presentation Layer
   ├── backend/apps/data/tests/test_export_views.py
   └── backend/apps/data/presentation/views.py (export 엔드포인트 추가)
```

### 5.2 Frontend
```
1. Application Layer
   ├── frontend/src/application/hooks/__tests__/useCSVExport.test.ts
   └── frontend/src/application/hooks/useCSVExport.ts

2. Service Layer
   └── frontend/src/services/api/dataApi.ts (exportCSV 메서드 추가)
```

---

## 6. 성공 기준

### 6.1 Backend
- [ ] CSV 파일 UTF-8 with BOM 인코딩
- [ ] 필터 조건 적용 정상
- [ ] Content-Disposition 헤더 정상
- [ ] 한글 파일명 지원

### 6.2 Frontend
- [ ] CSV 다운로드 트리거 정상
- [ ] 브라우저 다운로드 정상 작동
- [ ] 대용량 데이터 경고 표시

---

## 7. 마무리

이 계획서는 UC-005 (데이터 내보내기) 기능을 TDD 원칙에 따라 구현하기 위한 가이드입니다.

**핵심 원칙**:
1. **UTF-8 with BOM** 인코딩으로 Excel 호환성 확보
2. **필터 조건 동기화**
3. **대용량 데이터 처리** (비동기 처리 및 이메일 알림)
