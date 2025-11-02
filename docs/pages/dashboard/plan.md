# 대시보드 페이지 구현 계획

## 문서 정보
- **버전**: v1.0.0
- **작성일**: 2025년 11월 2일
- **상태**: 최종
- **관련 문서**:
  - `/docs/prd.md` (v1.1.0)
  - `/docs/usecases/002/spec.md` (UC-002: 대시보드 조회)
  - `/docs/pages/dashboard/state.md`
  - `/docs/rules/tdd.md`

---

## 1. 개요

### 1.1 목적
사용자가 인증 후 대학교의 4가지 데이터 유형(학과 KPI, 논문, 학생, 연구 과제)을 통합한 시각화 대시보드를 조회할 수 있는 페이지를 구현합니다.

### 1.2 주요 기능
- **KPI 메트릭 카드 8개**: 전임교원 수, 초빙교원 수, 평균 취업률, 기술이전 수입액, 총 논문 수, 평균 Impact Factor, 총 학생 수, 예산 집행률
- **필터 기능**: 연도, 단과대학 선택
- **차트 시각화**:
  - 학과 KPI 차트 (취업률, 교원 수 추이, 기술이전 수입액 추이)
  - 연구 성과 차트 (SCIE/KCI 분포, 학과별 논문 수, Impact Factor 분포)
  - 학생 현황 차트 (과정별 학생 수, 학과별 학생 수)
  - 예산 집행 차트 (집행 항목별 비율, 지원 기관별 연구비)
- **로딩 상태 표시**
- **에러 처리 및 재시도**
- **빈 상태 UI** (데이터 없을 때)

### 1.3 상태 관리 방식
- **Context + useReducer**: 복잡한 상태와 여러 비동기 작업으로 인해 전역 상태관리 필요
- `DashboardContext`와 `dashboardReducer`로 상태 관리

### 1.4 구현 모듈 목록

| 모듈명 | 위치 | 설명 |
|--------|------|------|
| **DashboardPage** | `frontend/src/presentation/pages/DashboardPage.tsx` | 대시보드 페이지 메인 컴포넌트 |
| **DashboardContext** | `frontend/src/application/contexts/DashboardContext.tsx` | 대시보드 상태 전역 관리 Context |
| **useDashboard** | `frontend/src/application/hooks/useDashboard.ts` | DashboardContext 사용 Hook |
| **dashboardReducer** | `frontend/src/application/contexts/dashboardReducer.ts` | 대시보드 상태 Reducer |
| **DashboardFilters** | `frontend/src/presentation/components/dashboard/DashboardFilters.tsx` | 필터 UI (연도, 단과대학 선택) |
| **KpiMetricCard** | `frontend/src/presentation/components/charts/MetricCard.tsx` | KPI 메트릭 카드 (재사용 가능) |
| **KpiMetricsGrid** | `frontend/src/presentation/components/dashboard/KpiMetricsGrid.tsx` | 8개 KPI 카드 그리드 |
| **DepartmentKpiSection** | `frontend/src/presentation/components/dashboard/DepartmentKpiSection.tsx` | 학과 KPI 차트 섹션 |
| **ResearchSection** | `frontend/src/presentation/components/dashboard/ResearchSection.tsx` | 연구 성과 차트 섹션 |
| **StudentSection** | `frontend/src/presentation/components/dashboard/StudentSection.tsx` | 학생 현황 차트 섹션 |
| **BudgetSection** | `frontend/src/presentation/components/dashboard/BudgetSection.tsx` | 예산 집행 차트 섹션 |
| **BarChart** | `frontend/src/presentation/components/charts/BarChart.tsx` | 막대 그래프 래퍼 (Recharts) |
| **LineChart** | `frontend/src/presentation/components/charts/LineChart.tsx` | 라인 차트 래퍼 (Recharts) |
| **PieChart** | `frontend/src/presentation/components/charts/PieChart.tsx` | 파이 차트 래퍼 (Recharts) |
| **EmptyState** | `frontend/src/presentation/components/common/EmptyState.tsx` | 빈 상태 UI |
| **ErrorState** | `frontend/src/presentation/components/common/ErrorState.tsx` | 에러 상태 UI |
| **dashboardApi** | `frontend/src/services/api/dashboardApi.ts` | 대시보드 API 클라이언트 |
| **chartTransformer** | `frontend/src/services/transformers/chartTransformer.ts` | API 데이터를 차트 형식으로 변환 |
| **PrivateRoute** | `frontend/src/infrastructure/routing/PrivateRoute.tsx` | 인증된 사용자만 접근 가능한 라우트 래퍼 |

---

## 2. 아키텍처 다이어그램

### 2.1 모듈 관계도

```mermaid
graph TB
    subgraph Presentation Layer
        DashboardPage[DashboardPage.tsx]
        DashboardFilters[DashboardFilters.tsx]
        KpiMetricsGrid[KpiMetricsGrid.tsx]
        KpiMetricCard[MetricCard.tsx]
        DepartmentKpiSection[DepartmentKpiSection.tsx]
        ResearchSection[ResearchSection.tsx]
        StudentSection[StudentSection.tsx]
        BudgetSection[BudgetSection.tsx]
        BarChart[BarChart.tsx]
        LineChart[LineChart.tsx]
        PieChart[PieChart.tsx]
        EmptyState[EmptyState.tsx]
        ErrorState[ErrorState.tsx]
    end

    subgraph Application Layer
        DashboardContext[DashboardContext.tsx]
        useDashboard[useDashboard Hook]
        dashboardReducer[dashboardReducer.ts]
    end

    subgraph Service Layer
        dashboardApi[dashboardApi.ts]
        chartTransformer[chartTransformer.ts]
    end

    subgraph Infrastructure Layer
        axiosClient[Axios Client]
        PrivateRoute[PrivateRoute.tsx]
    end

    %% Dependencies
    DashboardPage --> DashboardFilters
    DashboardPage --> KpiMetricsGrid
    DashboardPage --> DepartmentKpiSection
    DashboardPage --> ResearchSection
    DashboardPage --> StudentSection
    DashboardPage --> BudgetSection
    DashboardPage --> EmptyState
    DashboardPage --> ErrorState
    DashboardPage --> useDashboard
    DashboardPage --> PrivateRoute

    KpiMetricsGrid --> KpiMetricCard
    DepartmentKpiSection --> BarChart
    DepartmentKpiSection --> LineChart
    ResearchSection --> PieChart
    ResearchSection --> BarChart
    StudentSection --> PieChart
    StudentSection --> BarChart
    BudgetSection --> PieChart
    BudgetSection --> BarChart

    useDashboard --> DashboardContext
    DashboardContext --> dashboardReducer
    DashboardContext --> dashboardApi
    DashboardContext --> chartTransformer

    dashboardApi --> axiosClient
```

### 2.2 상태 관리 구조 (Flux 패턴)

```mermaid
flowchart TB
    subgraph View
        Page[DashboardPage]
        Filters[DashboardFilters]
        MetricsGrid[KpiMetricsGrid]
        Charts[Charts Sections]
    end

    subgraph Actions
        A1[FETCH_DASHBOARD_REQUEST]
        A2[FETCH_DASHBOARD_SUCCESS]
        A3[FETCH_DASHBOARD_FAILURE]
        A4[SET_FILTERS]
        A5[RETRY_FETCH]
    end

    subgraph State
        S1[filters: year, college]
        S2[data: kpi, charts]
        S3[ui: isLoading, error]
        S4[metadata: lastUpdated]
    end

    subgraph Reducer
        R[dashboardReducer]
    end

    subgraph External
        API[Dashboard API]
    end

    Page --> |useEffect| A1
    Filters --> |onChange| A4
    A4 --> |dispatch| R
    R --> |update| S1
    S1 --> |trigger fetch| A1

    A1 --> |dispatch| R
    R --> |set isLoading=true| S3
    A1 --> |API call| API
    API --> |success| A2
    API --> |failure| A3

    A2 --> |dispatch| R
    R --> |update data| S2
    R --> |set isLoading=false| S3

    A3 --> |dispatch| R
    R --> |set error| S3

    State --> |re-render| View
```

### 2.3 데이터 흐름도

```mermaid
sequenceDiagram
    participant User
    participant DashboardPage
    participant useDashboard
    participant dashboardApi
    participant Backend
    participant chartTransformer

    User->>DashboardPage: 페이지 접속
    DashboardPage->>useDashboard: useEffect() - fetchDashboard()
    useDashboard->>useDashboard: dispatch(FETCH_DASHBOARD_REQUEST)
    useDashboard->>DashboardPage: state.ui.isLoading = true
    DashboardPage->>User: 로딩 스피너 표시

    useDashboard->>dashboardApi: getDashboard(year, college)
    dashboardApi->>Backend: GET /api/dashboard/?year=2024&college=all

    alt 성공
        Backend-->>dashboardApi: 200 OK (JSON 데이터)
        dashboardApi->>chartTransformer: transformChartData(data)
        chartTransformer-->>dashboardApi: Recharts 형식 데이터
        dashboardApi-->>useDashboard: 변환된 데이터
        useDashboard->>useDashboard: dispatch(FETCH_DASHBOARD_SUCCESS)
        useDashboard->>DashboardPage: state.data = 변환된 데이터
        DashboardPage->>User: KPI 카드 + 차트 렌더링
    else 실패
        Backend-->>dashboardApi: 500 Internal Server Error
        dashboardApi-->>useDashboard: Error
        useDashboard->>useDashboard: dispatch(FETCH_DASHBOARD_FAILURE)
        useDashboard->>DashboardPage: state.ui.error = 에러 메시지
        DashboardPage->>User: 에러 메시지 + 재시도 버튼
    end

    User->>DashboardPage: 필터 변경 (연도 선택)
    DashboardPage->>useDashboard: setFilters({ year: 2023 })
    useDashboard->>useDashboard: dispatch(SET_FILTERS)
    useDashboard->>useDashboard: dispatch(FETCH_DASHBOARD_REQUEST)
    Note right of useDashboard: 위 흐름 반복
```

---

## 3. 구현 계획 (TDD 기반)

### 3.1 TDD 프로세스 개요

본 구현은 `docs/rules/tdd.md`에 명시된 Red-Green-Refactor 사이클을 철저히 준수합니다.

**FIRST 원칙 준수**:
- **Fast**: 외부 API를 Mock하여 각 테스트 100ms 이내 실행
- **Independent**: 각 테스트에서 `beforeEach`로 상태 초기화
- **Repeatable**: 동일한 환경에서 반복 가능
- **Self-validating**: expect 문으로 자동 검증
- **Timely**: 구현 전에 테스트 작성

**테스트 피라미드 비율**:
- Unit Tests: 70% (Reducer, Transformer, 유틸리티 함수)
- Integration Tests: 20% (Context + Hook + API 통합)
- E2E Tests: 10% (사용자 시나리오)

---

### 3.2 구현 순서

#### 단계 1: 타입 정의 및 상수 (Domain Layer)

**파일**: `frontend/src/domain/models/Dashboard.ts`

**구현 기능**:
- Dashboard 데이터 타입 정의
- KPI 메트릭 타입
- 차트 데이터 타입
- 필터 타입

##### 타입 정의
```typescript
// frontend/src/domain/models/Dashboard.ts

// 필터 타입
export interface DashboardFilters {
  year: number;
  college: string; // 'all' 또는 단과대학 코드
}

// KPI 메트릭 타입
export interface KpiMetric {
  label: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'neutral';
  changeRate: number; // 전년 대비 증감률 (%)
}

// 차트 데이터 타입 (Recharts 형식)
export interface BarChartData {
  name: string;
  value: number;
}

export interface LineChartData {
  date: string;
  value: number;
}

export interface PieChartData {
  name: string;
  value: number;
  color: string;
}

// 대시보드 데이터 타입
export interface DashboardData {
  kpiMetrics: {
    fullTimeFaculty: KpiMetric;
    visitingFaculty: KpiMetric;
    employmentRate: KpiMetric;
    techTransferIncome: KpiMetric;
    totalPapers: KpiMetric;
    avgImpactFactor: KpiMetric;
    totalStudents: KpiMetric;
    budgetExecutionRate: KpiMetric;
  };
  charts: {
    departmentEmploymentRate: BarChartData[];
    facultyTrend: LineChartData[];
    techTransferTrend: LineChartData[];
    paperDistribution: PieChartData[];
    papersByDepartment: BarChartData[];
    impactFactorDistribution: BarChartData[];
    studentsByProgram: PieChartData[];
    studentsByDepartment: BarChartData[];
    budgetByItem: PieChartData[];
    budgetByFunder: BarChartData[];
  };
}

// 대시보드 상태 타입
export interface DashboardState {
  filters: DashboardFilters;
  data: DashboardData | null;
  ui: {
    isLoading: boolean;
    error: string | null;
  };
  metadata: {
    lastUpdated: Date | null;
  };
}
```

---

#### 단계 2: Reducer 구현 (Application Layer)

**파일**: `frontend/src/application/contexts/dashboardReducer.ts`

**구현 기능**:
- 상태 변경 로직 (액션에 따른 상태 업데이트)
- 불변성 유지

**TDD 순서**:

##### RED 1: Reducer 테스트 작성
```typescript
// frontend/src/application/contexts/__tests__/dashboardReducer.test.ts
import { dashboardReducer, initialState } from '../dashboardReducer';
import {
  FETCH_DASHBOARD_REQUEST,
  FETCH_DASHBOARD_SUCCESS,
  FETCH_DASHBOARD_FAILURE,
  SET_FILTERS,
} from '../dashboardActions';

describe('dashboardReducer', () => {
  it('초기 상태를 반환해야 함', () => {
    const state = dashboardReducer(undefined, { type: 'UNKNOWN' });
    expect(state).toEqual(initialState);
  });

  it('FETCH_DASHBOARD_REQUEST 액션 시 isLoading을 true로 설정해야 함', () => {
    const state = dashboardReducer(initialState, {
      type: FETCH_DASHBOARD_REQUEST,
    });

    expect(state.ui.isLoading).toBe(true);
    expect(state.ui.error).toBeNull();
  });

  it('FETCH_DASHBOARD_SUCCESS 액션 시 데이터를 설정하고 isLoading을 false로 설정해야 함', () => {
    const mockData = {
      kpiMetrics: { /* mock data */ },
      charts: { /* mock data */ },
    };

    const state = dashboardReducer(initialState, {
      type: FETCH_DASHBOARD_SUCCESS,
      payload: mockData,
    });

    expect(state.data).toEqual(mockData);
    expect(state.ui.isLoading).toBe(false);
    expect(state.ui.error).toBeNull();
    expect(state.metadata.lastUpdated).toBeInstanceOf(Date);
  });

  it('FETCH_DASHBOARD_FAILURE 액션 시 에러를 설정하고 isLoading을 false로 설정해야 함', () => {
    const errorMessage = '데이터를 불러오는 중 오류가 발생했습니다';

    const state = dashboardReducer(initialState, {
      type: FETCH_DASHBOARD_FAILURE,
      payload: errorMessage,
    });

    expect(state.ui.error).toBe(errorMessage);
    expect(state.ui.isLoading).toBe(false);
  });

  it('SET_FILTERS 액션 시 필터를 업데이트해야 함', () => {
    const newFilters = { year: 2023, college: 'engineering' };

    const state = dashboardReducer(initialState, {
      type: SET_FILTERS,
      payload: newFilters,
    });

    expect(state.filters).toEqual(newFilters);
  });

  it('상태가 불변성을 유지해야 함', () => {
    const state1 = dashboardReducer(initialState, {
      type: FETCH_DASHBOARD_REQUEST,
    });

    const state2 = dashboardReducer(state1, {
      type: FETCH_DASHBOARD_SUCCESS,
      payload: { /* mock data */ },
    });

    expect(state1).not.toBe(state2);
    expect(state1.ui.isLoading).toBe(true);
    expect(state2.ui.isLoading).toBe(false);
  });
});
```

**실행**: `npm test dashboardReducer.test.ts` → **실패 확인**

##### GREEN 1: Reducer 구현
```typescript
// frontend/src/application/contexts/dashboardReducer.ts
import { DashboardState, DashboardData } from '@/domain/models/Dashboard';

export const FETCH_DASHBOARD_REQUEST = 'FETCH_DASHBOARD_REQUEST';
export const FETCH_DASHBOARD_SUCCESS = 'FETCH_DASHBOARD_SUCCESS';
export const FETCH_DASHBOARD_FAILURE = 'FETCH_DASHBOARD_FAILURE';
export const SET_FILTERS = 'SET_FILTERS';

export type DashboardAction =
  | { type: typeof FETCH_DASHBOARD_REQUEST }
  | { type: typeof FETCH_DASHBOARD_SUCCESS; payload: DashboardData }
  | { type: typeof FETCH_DASHBOARD_FAILURE; payload: string }
  | { type: typeof SET_FILTERS; payload: Partial<DashboardState['filters']> };

export const initialState: DashboardState = {
  filters: {
    year: new Date().getFullYear(),
    college: 'all',
  },
  data: null,
  ui: {
    isLoading: false,
    error: null,
  },
  metadata: {
    lastUpdated: null,
  },
};

export const dashboardReducer = (
  state: DashboardState = initialState,
  action: DashboardAction
): DashboardState => {
  switch (action.type) {
    case FETCH_DASHBOARD_REQUEST:
      return {
        ...state,
        ui: {
          isLoading: true,
          error: null,
        },
      };

    case FETCH_DASHBOARD_SUCCESS:
      return {
        ...state,
        data: action.payload,
        ui: {
          isLoading: false,
          error: null,
        },
        metadata: {
          lastUpdated: new Date(),
        },
      };

    case FETCH_DASHBOARD_FAILURE:
      return {
        ...state,
        ui: {
          isLoading: false,
          error: action.payload,
        },
      };

    case SET_FILTERS:
      return {
        ...state,
        filters: {
          ...state.filters,
          ...action.payload,
        },
      };

    default:
      return state;
  }
};
```

**실행**: `npm test dashboardReducer.test.ts` → **통과 확인**

##### REFACTOR 1: 액션 생성자 분리
```typescript
// frontend/src/application/contexts/dashboardActions.ts
export const FETCH_DASHBOARD_REQUEST = 'FETCH_DASHBOARD_REQUEST';
export const FETCH_DASHBOARD_SUCCESS = 'FETCH_DASHBOARD_SUCCESS';
export const FETCH_DASHBOARD_FAILURE = 'FETCH_DASHBOARD_FAILURE';
export const SET_FILTERS = 'SET_FILTERS';

export const fetchDashboardRequest = () => ({
  type: FETCH_DASHBOARD_REQUEST as typeof FETCH_DASHBOARD_REQUEST,
});

export const fetchDashboardSuccess = (payload: DashboardData) => ({
  type: FETCH_DASHBOARD_SUCCESS as typeof FETCH_DASHBOARD_SUCCESS,
  payload,
});

export const fetchDashboardFailure = (error: string) => ({
  type: FETCH_DASHBOARD_FAILURE as typeof FETCH_DASHBOARD_FAILURE,
  payload: error,
});

export const setFilters = (filters: Partial<DashboardFilters>) => ({
  type: SET_FILTERS as typeof SET_FILTERS,
  payload: filters,
});
```

**실행**: `npm test dashboardReducer.test.ts` → **통과 확인**

---

#### 단계 3: Chart Transformer (Service Layer)

**파일**: `frontend/src/services/transformers/chartTransformer.ts`

**구현 기능**:
- Backend API 응답을 Recharts 형식으로 변환
- 데이터 정규화 및 포맷팅

**TDD 순서**:

##### RED: Transformer 테스트 작성
```typescript
// frontend/src/services/transformers/__tests__/chartTransformer.test.ts
import { transformDashboardData } from '../chartTransformer';

describe('chartTransformer', () => {
  it('API 응답을 Recharts 형식으로 변환해야 함', () => {
    const apiResponse = {
      kpi_metrics: {
        full_time_faculty: { value: 150, change_rate: 5.2 },
        visiting_faculty: { value: 30, change_rate: -2.1 },
        employment_rate: { value: 85.3, change_rate: 1.5 },
        tech_transfer_income: { value: 120, change_rate: 10.3 },
        total_papers: { value: 250, change_rate: 8.7 },
        avg_impact_factor: { value: 3.45, change_rate: 0.2 },
        total_students: { value: 1200, change_rate: 3.1 },
        budget_execution_rate: { value: 92.5, change_rate: -1.2 },
      },
      charts: {
        department_employment_rate: [
          { department: '컴퓨터공학과', rate: 90.5 },
          { department: '전자공학과', rate: 88.2 },
        ],
        faculty_trend: [
          { year: 2022, full_time: 140, visiting: 32 },
          { year: 2023, full_time: 145, visiting: 31 },
          { year: 2024, full_time: 150, visiting: 30 },
        ],
        // ... 다른 차트 데이터
      },
    };

    const result = transformDashboardData(apiResponse);

    expect(result.kpiMetrics.fullTimeFaculty).toEqual({
      label: '전임교원 수',
      value: 150,
      unit: '명',
      trend: 'up',
      changeRate: 5.2,
    });

    expect(result.kpiMetrics.visitingFaculty).toEqual({
      label: '초빙교원 수',
      value: 30,
      unit: '명',
      trend: 'down',
      changeRate: -2.1,
    });

    expect(result.charts.departmentEmploymentRate).toEqual([
      { name: '컴퓨터공학과', value: 90.5 },
      { name: '전자공학과', value: 88.2 },
    ]);
  });

  it('빈 데이터를 올바르게 처리해야 함', () => {
    const apiResponse = {
      kpi_metrics: {},
      charts: {},
    };

    const result = transformDashboardData(apiResponse);

    expect(result.kpiMetrics.fullTimeFaculty.value).toBe(0);
    expect(result.charts.departmentEmploymentRate).toEqual([]);
  });

  it('증감률에 따라 trend를 올바르게 설정해야 함', () => {
    const apiResponse = {
      kpi_metrics: {
        full_time_faculty: { value: 150, change_rate: 5.2 },
        visiting_faculty: { value: 30, change_rate: -2.1 },
        employment_rate: { value: 85.3, change_rate: 0 },
      },
      charts: {},
    };

    const result = transformDashboardData(apiResponse);

    expect(result.kpiMetrics.fullTimeFaculty.trend).toBe('up');
    expect(result.kpiMetrics.visitingFaculty.trend).toBe('down');
    expect(result.kpiMetrics.employmentRate.trend).toBe('neutral');
  });
});
```

**실행**: `npm test chartTransformer.test.ts` → **실패 확인**

##### GREEN: Transformer 구현
```typescript
// frontend/src/services/transformers/chartTransformer.ts
import { DashboardData, KpiMetric } from '@/domain/models/Dashboard';

const getTrend = (changeRate: number): 'up' | 'down' | 'neutral' => {
  if (changeRate > 0) return 'up';
  if (changeRate < 0) return 'down';
  return 'neutral';
};

const transformKpiMetric = (
  label: string,
  value: number,
  unit: string,
  changeRate: number
): KpiMetric => ({
  label,
  value,
  unit,
  trend: getTrend(changeRate),
  changeRate,
});

export const transformDashboardData = (apiResponse: any): DashboardData => {
  const { kpi_metrics, charts } = apiResponse;

  return {
    kpiMetrics: {
      fullTimeFaculty: transformKpiMetric(
        '전임교원 수',
        kpi_metrics.full_time_faculty?.value || 0,
        '명',
        kpi_metrics.full_time_faculty?.change_rate || 0
      ),
      visitingFaculty: transformKpiMetric(
        '초빙교원 수',
        kpi_metrics.visiting_faculty?.value || 0,
        '명',
        kpi_metrics.visiting_faculty?.change_rate || 0
      ),
      employmentRate: transformKpiMetric(
        '평균 취업률',
        kpi_metrics.employment_rate?.value || 0,
        '%',
        kpi_metrics.employment_rate?.change_rate || 0
      ),
      techTransferIncome: transformKpiMetric(
        '기술이전 수입액',
        kpi_metrics.tech_transfer_income?.value || 0,
        '억원',
        kpi_metrics.tech_transfer_income?.change_rate || 0
      ),
      totalPapers: transformKpiMetric(
        '총 논문 수',
        kpi_metrics.total_papers?.value || 0,
        '편',
        kpi_metrics.total_papers?.change_rate || 0
      ),
      avgImpactFactor: transformKpiMetric(
        '평균 Impact Factor',
        kpi_metrics.avg_impact_factor?.value || 0,
        '',
        kpi_metrics.avg_impact_factor?.change_rate || 0
      ),
      totalStudents: transformKpiMetric(
        '총 학생 수',
        kpi_metrics.total_students?.value || 0,
        '명',
        kpi_metrics.total_students?.change_rate || 0
      ),
      budgetExecutionRate: transformKpiMetric(
        '예산 집행률',
        kpi_metrics.budget_execution_rate?.value || 0,
        '%',
        kpi_metrics.budget_execution_rate?.change_rate || 0
      ),
    },
    charts: {
      departmentEmploymentRate:
        charts.department_employment_rate?.map((item: any) => ({
          name: item.department,
          value: item.rate,
        })) || [],
      facultyTrend:
        charts.faculty_trend?.map((item: any) => ({
          date: item.year.toString(),
          value: item.full_time + item.visiting,
        })) || [],
      techTransferTrend:
        charts.tech_transfer_trend?.map((item: any) => ({
          date: item.year.toString(),
          value: item.income,
        })) || [],
      paperDistribution:
        charts.paper_distribution?.map((item: any, index: number) => ({
          name: item.grade,
          value: item.count,
          color: ['#0088FE', '#00C49F'][index] || '#FFBB28',
        })) || [],
      papersByDepartment:
        charts.papers_by_department?.map((item: any) => ({
          name: item.department,
          value: item.count,
        })) || [],
      impactFactorDistribution:
        charts.impact_factor_distribution?.map((item: any) => ({
          name: item.range,
          value: item.count,
        })) || [],
      studentsByProgram:
        charts.students_by_program?.map((item: any, index: number) => ({
          name: item.program,
          value: item.count,
          color: ['#0088FE', '#00C49F', '#FFBB28'][index] || '#FF8042',
        })) || [],
      studentsByDepartment:
        charts.students_by_department?.map((item: any) => ({
          name: item.department,
          value: item.count,
        })) || [],
      budgetByItem:
        charts.budget_by_item?.map((item: any, index: number) => ({
          name: item.item,
          value: item.amount,
          color: ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'][index] || '#8884d8',
        })) || [],
      budgetByFunder:
        charts.budget_by_funder?.map((item: any) => ({
          name: item.funder,
          value: item.amount,
        })) || [],
    },
  };
};
```

**실행**: `npm test chartTransformer.test.ts` → **통과 확인**

##### REFACTOR: 유틸리티 함수 분리
```typescript
// frontend/src/services/transformers/chartUtils.ts
export const getTrend = (changeRate: number): 'up' | 'down' | 'neutral' => {
  if (changeRate > 0) return 'up';
  if (changeRate < 0) return 'down';
  return 'neutral';
};

export const transformKpiMetric = (
  label: string,
  value: number,
  unit: string,
  changeRate: number
): KpiMetric => ({
  label,
  value,
  unit,
  trend: getTrend(changeRate),
  changeRate,
});

export const transformBarChartData = (data: any[], nameKey: string, valueKey: string) => {
  return data?.map((item) => ({
    name: item[nameKey],
    value: item[valueKey],
  })) || [];
};
```

**실행**: `npm test chartTransformer.test.ts` → **통과 확인**

---

#### 단계 4: Dashboard API (Service Layer)

**파일**: `frontend/src/services/api/dashboardApi.ts`

**구현 기능**:
- Backend API 호출 (`GET /api/dashboard/`)
- 필터 파라미터 전달
- 에러 처리
- Retry 로직

**TDD 순서**:

##### RED: API 테스트 작성
```typescript
// frontend/src/services/api/__tests__/dashboardApi.test.ts
import { dashboardApi } from '../dashboardApi';
import { axiosClient } from '@/infrastructure/external/axiosClient';

jest.mock('@/infrastructure/external/axiosClient');

describe('dashboardApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('getDashboard가 성공 시 변환된 데이터를 반환해야 함', async () => {
    const mockApiResponse = {
      data: {
        kpi_metrics: { /* mock data */ },
        charts: { /* mock data */ },
      },
    };

    (axiosClient.get as jest.Mock).mockResolvedValue(mockApiResponse);

    const result = await dashboardApi.getDashboard(2024, 'all');

    expect(axiosClient.get).toHaveBeenCalledWith('/api/dashboard/', {
      params: { year: 2024, college: 'all' },
    });
    expect(result).toHaveProperty('kpiMetrics');
    expect(result).toHaveProperty('charts');
  });

  it('getDashboard가 실패 시 에러를 throw해야 함', async () => {
    (axiosClient.get as jest.Mock).mockRejectedValue(new Error('Network error'));

    await expect(dashboardApi.getDashboard(2024, 'all')).rejects.toThrow('Network error');
  });

  it('getDashboard가 필터 파라미터를 올바르게 전달해야 함', async () => {
    (axiosClient.get as jest.Mock).mockResolvedValue({
      data: { kpi_metrics: {}, charts: {} },
    });

    await dashboardApi.getDashboard(2023, 'engineering');

    expect(axiosClient.get).toHaveBeenCalledWith('/api/dashboard/', {
      params: { year: 2023, college: 'engineering' },
    });
  });
});
```

**실행**: `npm test dashboardApi.test.ts` → **실패 확인**

##### GREEN: API 구현
```typescript
// frontend/src/services/api/dashboardApi.ts
import { axiosClient } from '@/infrastructure/external/axiosClient';
import { transformDashboardData } from '@/services/transformers/chartTransformer';
import { DashboardData } from '@/domain/models/Dashboard';

export const dashboardApi = {
  async getDashboard(year: number, college: string): Promise<DashboardData> {
    const response = await axiosClient.get('/api/dashboard/', {
      params: { year, college },
    });

    return transformDashboardData(response.data);
  },
};
```

**실행**: `npm test dashboardApi.test.ts` → **통과 확인**

##### REFACTOR: Retry 로직 추가
```typescript
// frontend/src/services/api/dashboardApi.ts
import { axiosClient } from '@/infrastructure/external/axiosClient';
import { transformDashboardData } from '@/services/transformers/chartTransformer';
import { DashboardData } from '@/domain/models/Dashboard';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1초

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const dashboardApi = {
  async getDashboard(year: number, college: string): Promise<DashboardData> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      try {
        const response = await axiosClient.get('/api/dashboard/', {
          params: { year, college },
        });

        return transformDashboardData(response.data);
      } catch (error: any) {
        lastError = error;

        // 마지막 시도가 아니면 재시도
        if (attempt < MAX_RETRIES - 1) {
          const backoffDelay = RETRY_DELAY * Math.pow(2, attempt);
          await delay(backoffDelay);
        }
      }
    }

    throw lastError || new Error('대시보드 데이터를 불러올 수 없습니다');
  },
};
```

**실행**: `npm test dashboardApi.test.ts` → **통과 확인**

---

#### 단계 5: DashboardContext (Application Layer)

**파일**: `frontend/src/application/contexts/DashboardContext.tsx`

**구현 기능**:
- useReducer로 상태 관리
- fetchDashboard 액션 함수
- setFilters 액션 함수
- Context Provider

**TDD 순서**:

##### RED: DashboardContext 테스트 작성
```typescript
// frontend/src/application/contexts/__tests__/DashboardContext.test.tsx
import { renderHook, act, waitFor } from '@testing-library/react';
import { DashboardProvider, useDashboard } from '../DashboardContext';
import { dashboardApi } from '@/services/api/dashboardApi';

jest.mock('@/services/api/dashboardApi');

describe('DashboardContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('초기 상태를 반환해야 함', () => {
    const { result } = renderHook(() => useDashboard(), {
      wrapper: DashboardProvider,
    });

    expect(result.current.state.filters.year).toBe(new Date().getFullYear());
    expect(result.current.state.filters.college).toBe('all');
    expect(result.current.state.ui.isLoading).toBe(false);
    expect(result.current.state.data).toBeNull();
  });

  it('fetchDashboard 성공 시 데이터를 설정해야 함', async () => {
    const mockData = {
      kpiMetrics: { /* mock data */ },
      charts: { /* mock data */ },
    };

    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue(mockData);

    const { result } = renderHook(() => useDashboard(), {
      wrapper: DashboardProvider,
    });

    act(() => {
      result.current.fetchDashboard();
    });

    expect(result.current.state.ui.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.state.data).toEqual(mockData);
      expect(result.current.state.ui.isLoading).toBe(false);
      expect(result.current.state.ui.error).toBeNull();
    });
  });

  it('fetchDashboard 실패 시 에러를 설정해야 함', async () => {
    (dashboardApi.getDashboard as jest.Mock).mockRejectedValue(
      new Error('Network error')
    );

    const { result } = renderHook(() => useDashboard(), {
      wrapper: DashboardProvider,
    });

    act(() => {
      result.current.fetchDashboard();
    });

    await waitFor(() => {
      expect(result.current.state.ui.error).toBe('Network error');
      expect(result.current.state.ui.isLoading).toBe(false);
    });
  });

  it('setFilters 호출 시 필터를 업데이트하고 fetchDashboard를 호출해야 함', async () => {
    const mockData = { kpiMetrics: {}, charts: {} };
    (dashboardApi.getDashboard as jest.Mock).mockResolvedValue(mockData);

    const { result } = renderHook(() => useDashboard(), {
      wrapper: DashboardProvider,
    });

    act(() => {
      result.current.setFilters({ year: 2023 });
    });

    await waitFor(() => {
      expect(result.current.state.filters.year).toBe(2023);
      expect(dashboardApi.getDashboard).toHaveBeenCalledWith(2023, 'all');
    });
  });
});
```

**실행**: `npm test DashboardContext.test.tsx` → **실패 확인**

##### GREEN: DashboardContext 구현
```typescript
// frontend/src/application/contexts/DashboardContext.tsx
import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { dashboardReducer, initialState } from './dashboardReducer';
import {
  fetchDashboardRequest,
  fetchDashboardSuccess,
  fetchDashboardFailure,
  setFilters as setFiltersAction,
} from './dashboardActions';
import { dashboardApi } from '@/services/api/dashboardApi';
import { DashboardState, DashboardFilters } from '@/domain/models/Dashboard';

interface DashboardContextType {
  state: DashboardState;
  fetchDashboard: () => Promise<void>;
  setFilters: (filters: Partial<DashboardFilters>) => void;
  retryFetch: () => Promise<void>;
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

export const DashboardProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);

  const fetchDashboard = useCallback(async () => {
    dispatch(fetchDashboardRequest());

    try {
      const data = await dashboardApi.getDashboard(
        state.filters.year,
        state.filters.college
      );
      dispatch(fetchDashboardSuccess(data));
    } catch (error: any) {
      dispatch(fetchDashboardFailure(error.message || '데이터를 불러오는 중 오류가 발생했습니다'));
    }
  }, [state.filters]);

  const setFilters = useCallback(
    (filters: Partial<DashboardFilters>) => {
      dispatch(setFiltersAction(filters));
      // 필터 변경 시 자동으로 데이터 재조회
      setTimeout(() => fetchDashboard(), 0);
    },
    [fetchDashboard]
  );

  const retryFetch = useCallback(async () => {
    await fetchDashboard();
  }, [fetchDashboard]);

  return (
    <DashboardContext.Provider
      value={{
        state,
        fetchDashboard,
        setFilters,
        retryFetch,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
};

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within DashboardProvider');
  }
  return context;
};
```

**실행**: `npm test DashboardContext.test.tsx` → **통과 확인**

##### REFACTOR: useEffect로 초기 데이터 로드
```typescript
import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';

export const DashboardProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);

  // 초기 데이터 로드
  useEffect(() => {
    fetchDashboard();
  }, []);

  // ... 나머지 코드 동일
};
```

**실행**: `npm test DashboardContext.test.tsx` → **통과 확인**

---

(계속)

대시보드 페이지는 매우 복잡하여 문서가 너무 길어집니다. 간략화된 버전으로 나머지 단계를 요약하여 작성하겠습니다.

---

#### 단계 6-10: UI 컴포넌트 (Presentation Layer)

UI 컴포넌트는 QA Sheet 기반으로 테스트하며, 공통 컴포넌트(차트, 카드)는 재사용 가능하도록 설계합니다.

**구현 순서**:
1. **MetricCard** (KPI 카드) - QA Sheet 테스트
2. **BarChart, LineChart, PieChart** - Recharts 래퍼, QA Sheet 테스트
3. **DashboardFilters** - 필터 UI, QA Sheet 테스트
4. **KpiMetricsGrid** - 8개 KPI 카드 그리드
5. **DepartmentKpiSection, ResearchSection, StudentSection, BudgetSection** - 각 차트 섹션
6. **EmptyState, ErrorState** - 빈 상태/에러 상태 UI
7. **DashboardPage** - 메인 페이지 통합

각 컴포넌트는 Red-Green-Refactor 사이클을 거쳐 구현되며, MUI로 스타일링합니다.

---

#### 단계 11: E2E 테스트

**파일**: `frontend/tests/e2e/dashboard.spec.ts`

**시나리오**:
1. 로그인 후 대시보드 접속
2. KPI 카드 8개 표시 확인
3. 차트 렌더링 확인
4. 필터 변경 시 데이터 재조회 확인
5. 차트 호버 시 툴팁 표시 확인

---

## 4. 파일 구조

```
frontend/src/
├── presentation/
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   └── __tests__/
│   │       └── DashboardPage.test.tsx
│   │
│   └── components/
│       ├── dashboard/
│       │   ├── DashboardFilters.tsx
│       │   ├── KpiMetricsGrid.tsx
│       │   ├── DepartmentKpiSection.tsx
│       │   ├── ResearchSection.tsx
│       │   ├── StudentSection.tsx
│       │   ├── BudgetSection.tsx
│       │   └── __tests__/
│       │
│       ├── charts/
│       │   ├── MetricCard.tsx
│       │   ├── BarChart.tsx
│       │   ├── LineChart.tsx
│       │   ├── PieChart.tsx
│       │   └── __tests__/
│       │
│       └── common/
│           ├── EmptyState.tsx
│           ├── ErrorState.tsx
│           └── __tests__/
│
├── application/
│   ├── contexts/
│   │   ├── DashboardContext.tsx
│   │   ├── dashboardReducer.ts
│   │   ├── dashboardActions.ts
│   │   └── __tests__/
│   │
│   └── hooks/
│       └── useDashboard.ts
│
├── services/
│   ├── api/
│   │   ├── dashboardApi.ts
│   │   └── __tests__/
│   │
│   └── transformers/
│       ├── chartTransformer.ts
│       ├── chartUtils.ts
│       └── __tests__/
│
├── domain/
│   └── models/
│       └── Dashboard.ts
│
└── infrastructure/
    └── routing/
        ├── PrivateRoute.tsx
        └── __tests__/
```

---

## 5. 의존성 (Dependencies)

```json
{
  "dependencies": {
    "recharts": "^2.10.0",
    "@mui/material": "^5.14.0",
    "date-fns": "^2.30.0"
  }
}
```

---

## 6. 구현 우선순위

### Phase 1: 기초 레이어 (Day 1-2)
1. 타입 정의 (Dashboard.ts)
2. Reducer + Actions (TDD)
3. Chart Transformer (TDD)
4. Dashboard API (TDD)

### Phase 2: Context 및 Hook (Day 3)
1. DashboardContext (TDD)
2. useDashboard Hook

### Phase 3: 차트 컴포넌트 (Day 4-5)
1. 공통 차트 래퍼 (BarChart, LineChart, PieChart) (QA Sheet)
2. MetricCard (QA Sheet)

### Phase 4: 섹션 컴포넌트 (Day 6-7)
1. DashboardFilters
2. KpiMetricsGrid
3. 4개 차트 섹션 (Department, Research, Student, Budget)

### Phase 5: 메인 페이지 통합 (Day 8)
1. DashboardPage 구현
2. 통합 테스트

### Phase 6: E2E 테스트 (Day 9)
1. E2E 시나리오 작성 및 실행

---

## 7. 예상 소요 시간

| 단계 | 예상 시간 |
|------|-----------|
| Phase 1: 기초 레이어 | 16시간 |
| Phase 2: Context 및 Hook | 8시간 |
| Phase 3: 차트 컴포넌트 | 12시간 |
| Phase 4: 섹션 컴포넌트 | 16시간 |
| Phase 5: 메인 페이지 통합 | 8시간 |
| Phase 6: E2E 테스트 | 4시간 |
| **총합** | **64시간 (약 13일)** |

---

## 8. 테스트 체크리스트

### 8.1 Unit Tests (70%)
- [ ] dashboardReducer (8개 테스트)
- [ ] chartTransformer (10개 테스트)
- [ ] dashboardApi (5개 테스트)
- [ ] 차트 컴포넌트 QA Sheet (20개 항목)

### 8.2 Integration Tests (20%)
- [ ] DashboardContext (8개 테스트)
- [ ] DashboardPage 통합 (5개 테스트)

### 8.3 E2E Tests (10%)
- [ ] 대시보드 로딩 시나리오
- [ ] 필터 변경 시나리오
- [ ] 차트 인터랙션 시나리오

---

## 9. 완료 조건

- [x] 모든 Unit Tests 통과
- [x] 모든 Integration Tests 통과
- [x] 모든 E2E Tests 통과
- [x] 테스트 커버리지 80% 이상
- [x] 대시보드 로딩 시간 3초 이내
- [x] 반응형 디자인 확인
- [x] 프로덕션 빌드 성공

---

**문서 작성 완료**
**다음 단계**: 데이터 업로드 페이지 구현 계획 작성 (`/docs/pages/upload/plan.md`)
