# UC-004: 데이터 조회 및 필터링 (4가지 CSV 타입)

## Primary Actor
- 인증된 대학교 직원 (관리자 또는 일반 사용자)

## Precondition
- 사용자가 로그인되어 있어야 함
- 데이터베이스에 4가지 타입 중 하나 이상의 데이터가 존재해야 함

## Trigger
- Navigation Bar에서 "Data" 메뉴 클릭

## Main Scenario

1. 사용자가 데이터 조회 페이지에 접근함
2. 시스템이 JWT 토큰을 검증함
3. 시스템이 기본 필터 조건으로 데이터를 요청함
   - 데이터 유형: 전체 (4가지 타입 모두)
   - 페이지: 1
   - 페이지 크기: 20
   - 정렬: 날짜/연도 내림차순
4. Backend가 데이터베이스에서 데이터를 조회함 (페이지네이션 적용)
   - department_kpi, publication, research_project, student 테이블 UNION 또는 개별 조회
5. Backend가 총 결과 수와 함께 JSON 응답을 반환함
6. Frontend가 데이터 테이블과 필터 UI를 렌더링함
7. 시스템이 다음 요소를 표시함
   - **필터 옵션**
     - 데이터 유형: 전체, 학과 KPI, 논문 목록, 연구 과제, 학생 명단
     - 기간: 연도 선택 (2020~2030)
     - 단과대학 선택
     - 학과 선택
     - 검색어 입력
   - **데이터 테이블** (데이터 유형에 따라 동적 컬럼)
     - **학과 KPI**: 평가년도, 단과대학, 학과, 취업률, 교원 수, 기술이전 수입, 학술대회
     - **논문 목록**: 논문ID, 게재일, 학과, 논문제목, 주저자, 학술지명, 저널등급, Impact Factor
     - **연구 과제**: 집행ID, 과제번호, 과제명, 연구책임자, 총연구비, 집행일자, 집행금액, 상태
     - **학생 명단**: 학번, 이름, 학과, 학년, 과정구분, 학적상태, 입학년도, 지도교수
   - **페이지네이션** (이전, 다음, 페이지 번호)
   - **총 결과 수**
   - **[CSV 다운로드]** 버튼

**Result**: 사용자가 테이블 형식으로 4가지 데이터 유형을 조회하고 필터링할 수 있음

## Alternative Scenarios

### 4a. 데이터 없음
4a1. Backend가 데이터베이스에서 데이터를 찾지 못함
4a2. Backend가 빈 배열을 반환함
4a3. Frontend가 빈 상태 UI를 표시함
4a4-1. 관리자: "조회 가능한 데이터가 없습니다" + [Excel 업로드] 버튼
4a4-2. 일반 사용자: "조회 가능한 데이터가 없습니다"

### 필터링 시나리오

### 8. 사용자가 필터를 적용함
8.1. 사용자가 데이터 유형을 선택함 (예: "논문 목록")
8.2. 사용자가 기간을 선택함 (예: "2024년")
8.3. 사용자가 단과대학을 선택함 (예: "공과대학")
8.4. 사용자가 학과를 선택함 (예: "컴퓨터공학과")
8.5. 사용자가 검색어를 입력함 (예: "Deep Learning")
8.6. 사용자가 [적용] 버튼을 클릭함
8.7. 시스템이 쿼리 파라미터를 업데이트함
8.8. 시스템이 필터링된 데이터를 요청함
8.9. Backend가 필터 조건에 맞는 데이터를 조회함
   - **학과 KPI**: WHERE evaluation_year=2024 AND college='공과대학' AND department='컴퓨터공학과'
   - **논문 목록**: WHERE EXTRACT(YEAR FROM publication_date)=2024 AND college='공과대학' AND paper_title LIKE '%Deep Learning%'
   - **연구 과제**: WHERE EXTRACT(YEAR FROM execution_date)=2024 AND department='컴퓨터공학과' AND project_name LIKE '%Deep Learning%'
   - **학생 명단**: WHERE admission_year=2024 AND college='공과대학' AND department='컴퓨터공학과'
8.10. Frontend가 필터링된 결과를 테이블에 표시함

### 8a. 검색 결과 없음
8a1. Backend가 필터 조건에 맞는 데이터를 찾지 못함
8a2. Frontend가 "검색 결과가 없습니다" 메시지를 표시함
8a3. Frontend가 [필터 초기화] 버튼을 제공함

### 데이터 상세 조회 시나리오

### 9. 사용자가 특정 행의 [보기] 버튼을 클릭함
9.1. 시스템이 데이터 유형을 확인함
9.2. 시스템이 상세 정보 모달을 표시함
9.3. 모달에 모든 필드 정보가 데이터 유형에 따라 표시됨
   - **학과 KPI**: 평가년도, 단과대학, 학과, 취업률, 전임교원 수, 초빙교원 수, 기술이전 수입액, 국제학술대회 개최 횟수, 업로드 일시, 업로드 사용자
   - **논문 목록**: 논문ID, 게재일, 단과대학, 학과, 논문제목, 주저자, 참여저자, 학술지명, 저널등급, Impact Factor, 과제연계여부, 업로드 일시, 업로드 사용자
   - **연구 과제**: 집행ID, 과제번호, 과제명, 연구책임자, 소속학과, 지원기관, 총연구비, 집행일자, 집행항목, 집행금액, 상태, 비고, 업로드 일시, 업로드 사용자
   - **학생 명단**: 학번, 이름, 단과대학, 학과, 학년, 과정구분, 학적상태, 성별, 입학년도, 지도교수, 이메일, 업로드 일시, 업로드 사용자
9.4. 관리자인 경우 [수정], [삭제] 버튼이 표시됨
9.5. 사용자가 [닫기] 버튼을 클릭하여 모달을 닫음

### 페이지네이션 시나리오

### 10. 사용자가 다음 페이지를 요청함
10.1. 사용자가 페이지 번호 또는 [다음] 버튼을 클릭함
10.2. 시스템이 해당 페이지의 데이터를 요청함
10.3. Backend가 페이지네이션을 적용하여 데이터를 반환함
10.4. Frontend가 테이블을 새 데이터로 업데이트함

## Edge Cases

- **정렬**: 사용자가 테이블 헤더를 클릭하면 해당 컬럼 기준으로 오름차순/내림차순 정렬됨
- **다중 필터**: 여러 필터를 동시에 적용 가능 (AND 조건)
- **검색어 자동완성**: 검색어 입력 시 디바운싱 적용 (500ms 후 자동 검색)
- **URL 상태 동기화**: 필터 조건이 URL 쿼리 파라미터에 저장되어 공유 및 북마크 가능
- **데이터 수정/삭제**: 관리자만 가능, 일반 사용자는 버튼 미표시
- **동적 컬럼**: 선택한 데이터 유형에 따라 테이블 컬럼이 자동으로 변경됨

## Business Rules

### 공통 규칙
- BR-001: 모든 로그인 사용자는 4가지 타입의 데이터 조회 가능함
- BR-002: 데이터 수정/삭제는 관리자만 가능함
- BR-003: 기본 페이지 크기는 20행이며, 사용자가 50 또는 100으로 변경 가능함
- BR-004: 기본 정렬은 날짜/연도 내림차순 (최신 데이터 우선)
- BR-005: 페이지네이션은 오프셋 기반을 사용함
- BR-006: 데이터 조회 API 응답 시간은 평균 500ms 이내여야 함 (NFR)
- BR-007: 검색 디바운싱은 500ms 적용됨

### 데이터 유형별 필터 규칙
- BR-101: **학과 KPI**: 평가년도, 단과대학, 학과로 필터링 가능
- BR-102: **논문 목록**: 게재일(연도), 단과대학, 학과, 저널등급, 과제연계여부로 필터링 가능
- BR-103: **연구 과제**: 집행일자(연도), 지원기관, 상태, 연구책임자로 필터링 가능
- BR-104: **학생 명단**: 입학년도, 단과대학, 학과, 과정구분, 학적상태로 필터링 가능

### 검색 규칙
- BR-201: 검색어는 데이터 유형별로 다음 필드에서 부분 일치 검색됨 (2자 이상)
  - **학과 KPI**: 단과대학, 학과
  - **논문 목록**: 논문제목, 주저자, 참여저자, 학술지명
  - **연구 과제**: 과제번호, 과제명, 연구책임자
  - **학생 명단**: 이름, 학과, 지도교수, 이메일

### CSV 다운로드 규칙
- BR-301: CSV 다운로드 시 현재 필터 조건이 적용된 데이터만 다운로드됨
- BR-302: CSV 파일명 형식: `{data_type}_export_{YYYYMMDD}.csv`
- BR-303: CSV 인코딩: UTF-8 with BOM (엑셀 호환성)
- BR-304: 10,000건 초과 시 비동기 처리 및 이메일 발송

## Sequence Diagram

```plantuml
@startuml
actor User
participant "FE\n(React)" as FE
participant "BE\n(Django)" as BE
database "Database\n(PostgreSQL)" as DB

User -> FE: 데이터 조회 페이지 접근
activate FE
FE --> User: 로딩 스피너 표시

FE -> BE: GET /api/data/\n?page=1&page_size=20&ordering=-date\n(Authorization: Bearer {token})
activate BE

BE -> BE: JWT 토큰 검증

BE -> DB: 데이터 조회\n(페이지네이션 적용)\nUNION ALL\n- department_kpi\n- publication\n- research_project\n- student
activate DB
DB --> BE: 데이터 반환\n(총 개수 포함)
deactivate DB

BE --> FE: 200 OK\nJSON (results, count, next, previous)
deactivate BE

FE --> User: 데이터 테이블 + 필터 UI 렌더링\n총 N건
deactivate FE

== 필터 적용 ==

User -> FE: 필터 선택\n- 데이터 유형: 논문 목록\n- 기간: 2024년\n- 검색어: "Deep Learning"\n[적용] 클릭
activate FE

FE -> FE: 쿼리 파라미터 생성

FE -> BE: GET /api/data/\n?type=publication&year=2024&search=Deep Learning\n(Authorization: Bearer {token})
activate BE

BE -> DB: 필터링된 데이터 조회\nSELECT * FROM publication\nWHERE EXTRACT(YEAR FROM publication_date)=2024\nAND paper_title LIKE '%Deep Learning%'
activate DB
DB --> BE: 필터링된 데이터 반환
deactivate DB

alt 검색 결과 없음
    BE --> FE: 200 OK\nJSON (results=[], count=0)
    FE --> User: "검색 결과가 없습니다"\n[필터 초기화] 버튼
else 검색 결과 있음
    BE --> FE: 200 OK\nJSON (results, count)
    deactivate BE
    FE --> User: 필터링된 테이블 표시\n총 M건
end

deactivate FE

== 데이터 상세 조회 ==

User -> FE: [보기] 버튼 클릭
activate FE
FE --> User: 상세 정보 모달 표시\n- 데이터 유형별 모든 필드\n- [닫기] 버튼

alt 관리자
    FE --> User: [수정] [삭제] 버튼 표시
end

deactivate FE

@enduml
```

## Post-conditions

### Success
- 사용자는 테이블 형식으로 4가지 데이터 유형을 확인할 수 있음
- 사용자는 필터를 통해 원하는 데이터를 찾을 수 있음
- 사용자는 페이지네이션을 통해 대량의 데이터를 탐색할 수 있음
- 사용자는 상세 정보 모달을 통해 각 항목의 세부 정보를 확인할 수 있음
- 관리자는 데이터를 수정하거나 삭제할 수 있음
- 사용자는 CSV 파일로 필터링된 데이터를 다운로드할 수 있음

### Failure
- 오류 메시지가 표시됨
- 사용자는 [다시 시도] 버튼을 통해 재시도할 수 있음

## Related Use Cases
- UC-002: 대시보드 조회 (대시보드에서 데이터 조회 페이지로 이동 가능)
- UC-003: Excel 파일 업로드 (업로드된 4가지 타입의 데이터를 조회 가능)
- UC-005: 데이터 내보내기 (조회한 데이터를 CSV로 다운로드)
