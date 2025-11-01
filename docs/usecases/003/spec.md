# UC-003: Excel 파일 업로드

## Primary Actor
- 관리자 (Admin)

## Precondition
- 사용자가 관리자 권한으로 로그인되어 있어야 함
- 사용자가 업로드할 Excel 파일(.xlsx 또는 .xls)을 준비하고 있어야 함
- Excel 파일은 시스템이 요구하는 컬럼 구조를 따라야 함

## Trigger
- Navigation Bar에서 "Upload" 메뉴 클릭

## Main Scenario

1. 사용자가 업로드 페이지에 접근함
2. 시스템이 권한을 검증함 (관리자 여부)
3. 시스템이 업로드 폼과 과거 업로드 이력 테이블을 표시함
4. 사용자가 데이터 유형을 선택함 (실적/논문/학생/예산)
5. 사용자가 Excel 파일을 드래그 앤 드롭하거나 파일 선택 다이얼로그에서 선택함
6. 사용자가 "업로드" 버튼을 클릭함
7. 시스템이 클라이언트 측 검증을 수행함
   - 파일 확장자 확인 (.xlsx, .xls)
   - 파일 크기 확인 (최대 10MB)
   - 데이터 유형 선택 여부 확인
8. 시스템이 프로그레스 바를 표시하고 파일을 Backend로 전송함
9. Backend가 파일을 수신하고 임시 디렉토리에 저장함
10. Backend가 Excel 파일을 파싱함 (openpyxl)
    - 헤더 행 인식
    - 데이터 행 파싱
11. Backend가 데이터를 검증함
    - 필수 컬럼 존재 여부 확인
    - 데이터 타입 검증 (날짜, 숫자 등)
    - 중복 데이터 검사
12. Backend가 검증된 데이터를 데이터베이스에 배치 삽입함 (Bulk Create)
13. Backend가 파일 메타데이터를 저장함
    - 파일명, 데이터 유형, 업로드 일시, 업로드 사용자, 처리된 행 수, 상태
14. Backend가 성공 응답을 반환함
15. Frontend가 프로그레스 바를 100%로 업데이트함
16. 시스템이 성공 메시지를 표시함: "파일이 성공적으로 업로드되었습니다. (N행 처리됨)"
17. 시스템이 업로드 이력 테이블을 갱신함
18. 시스템이 [대시보드 보기] 버튼을 표시함

**Result**: Excel 파일의 데이터가 데이터베이스에 저장되고 대시보드에서 조회 가능해짐

## Alternative Scenarios

### 2a. 일반 사용자 접근
2a1. 시스템이 사용자가 관리자 권한이 없음을 감지함
2a2. 시스템이 403 Forbidden 페이지를 표시함
2a3. "관리자만 접근할 수 있습니다" 메시지와 [대시보드로 돌아가기] 버튼 표시
2a4. 사용 종료

### 7a. 파일 형식 오류
7a1. 시스템이 파일 확장자가 .xlsx 또는 .xls가 아님을 감지함
7a2. 시스템이 "Excel 파일(.xlsx, .xls)만 업로드 가능합니다" 메시지 표시
7a3. 사용자가 올바른 파일을 선택함
7a4. Main Scenario의 6단계로 돌아감

### 7b. 파일 크기 초과
7b1. 시스템이 파일 크기가 10MB를 초과함을 감지함
7b2. 시스템이 "파일 크기가 10MB를 초과합니다. (현재: NMB)" 메시지 표시
7b3. 사용자가 파일 크기를 줄이거나 다른 파일을 선택함
7b4. Main Scenario의 6단계로 돌아감

### 10a. Excel 파일 손상
10a1. Backend가 openpyxl 파싱 중 오류 발생
10a2. Backend가 400 Bad Request 응답 반환
10a3. Frontend가 "파일이 손상되었거나 올바른 Excel 형식이 아닙니다" 메시지 표시
10a4. 사용자가 파일을 수정하거나 다른 파일을 선택함
10a5. Main Scenario의 6단계로 돌아감

### 11a. 필수 컬럼 누락
11a1. Backend가 필수 컬럼이 누락되었음을 감지함
11a2. Backend가 400 Bad Request 응답 반환
11a3. Frontend가 다음 메시지를 표시함
     ```
     필수 컬럼이 누락되었습니다:
     - 금액 (필수)
     현재 파일의 컬럼: 날짜, 카테고리, 비고
     ```
11a4. 사용자가 파일을 수정함
11a5. Main Scenario의 6단계로 돌아감

### 11b. 데이터 타입 오류
11b1. Backend가 데이터 타입 검증에 실패함
11b2. Backend가 오류 행 정보와 함께 400 Bad Request 응답 반환
11b3. Frontend가 다음 메시지를 표시함
     ```
     데이터 형식 오류:
     - 5행 금액: "백만원"은 숫자가 아닙니다
     - 12행 날짜: "작년"은 날짜 형식이 아닙니다 (YYYY-MM-DD 필요)

     오류 행을 제외하고 업로드하시겠습니까?
     ```
11b4. 사용자가 [제외하고 업로드] 또는 [취소] 선택
11b5-1. [제외하고 업로드]: Backend가 유효한 행만 저장, Main Scenario의 14단계로 진행
11b5-2. [취소]: Main Scenario의 6단계로 돌아감

### 11c. 중복 데이터
11c1. Backend가 이미 존재하는 데이터를 감지함
11c2. Frontend가 다음 메시지를 표시함
     ```
     중복 데이터 발견:
     - 15행: 2024-11-01 실적 데이터는 이미 존재합니다

     중복 데이터를 덮어쓰시겠습니까?
     ```
11c3. 사용자가 [덮어쓰기], [건너뛰기], 또는 [취소] 선택
11c4-1. [덮어쓰기]: Backend가 기존 데이터 업데이트, Main Scenario의 12단계로 진행
11c4-2. [건너뛰기]: Backend가 중복 행 제외하고 저장, Main Scenario의 12단계로 진행
11c4-3. [취소]: Main Scenario의 6단계로 돌아감

### 8a. 네트워크 오류
8a1. 업로드 중 네트워크 연결이 끊김
8a2. 시스템이 최대 3회 자동 재시도함
8a3-1. 재시도 성공 시 Main Scenario의 9단계로 진행
8a3-2. 재시도 실패 시 "업로드 중 오류가 발생했습니다" 메시지 표시 + [재시도] 버튼
8a4. 사용자가 [재시도] 클릭 시 Main Scenario의 6단계로 돌아감

### 12a. 트랜잭션 오류
12a1. 데이터베이스 저장 중 오류 발생
12a2. Backend가 트랜잭션 롤백 수행
12a3. Backend가 500 Internal Server Error 응답 반환
12a4. Frontend가 "업로드 중 오류가 발생했습니다. 데이터가 저장되지 않았습니다" 메시지 표시
12a5. Main Scenario의 6단계로 돌아감

## Edge Cases

- **대용량 파일**: 10만 행 이상의 파일 업로드 시 백그라운드 처리 및 이메일 알림 제공
- **업로드 중단**: 사용자가 브라우저를 닫거나 새로고침 시 임시 파일 자동 삭제
- **동시 업로드**: 여러 관리자가 동시에 파일 업로드 가능 (각 트랜잭션 독립적 처리)
- **파일명 한글**: 한글 파일명 지원 (UTF-8 인코딩)
- **특수문자 처리**: 데이터에 특수문자(%, 쉼표 등) 포함 시 자동 파싱

## Business Rules

- BR-001: Excel 파일 업로드는 관리자만 가능함
- BR-002: 지원 파일 형식은 .xlsx, .xls임
- BR-003: 최대 파일 크기는 10MB임
- BR-004: 데이터 유형은 실적/논문/학생/예산 중 하나를 선택해야 함
- BR-005: 각 데이터 유형별 필수 컬럼은 다음과 같음
  - **실적**: 날짜, 금액, 카테고리
  - **논문**: 제목, 저자, 게재일, 분야
  - **학생**: 학번, 이름, 학과, 학년
  - **예산**: 항목, 금액, 카테고리
- BR-006: 날짜 형식은 YYYY-MM-DD 또는 YYYY/MM/DD임
- BR-007: 금액은 숫자 또는 쉼표로 구분된 숫자 형식이어야 함 (예: 1,200,000)
- BR-008: 중복 데이터는 (날짜, 항목명) 조합으로 판단함
- BR-009: 업로드 이력은 30일간 보관됨
- BR-010: 트랜잭션은 전체 성공 또는 전체 롤백 원칙을 따름 (원자성)
- BR-011: 업로드 성공 시 대시보드 캐시를 자동으로 무효화함

## Sequence Diagram

```plantuml
@startuml
actor User
participant "FE\n(React)" as FE
participant "BE\n(Django)" as BE
participant "ExcelParser\n(Service)" as Parser
participant "DataValidator\n(Service)" as Validator
database "Database\n(PostgreSQL)" as DB

User -> FE: 업로드 페이지 접근
activate FE
FE -> FE: 관리자 권한 확인

alt 일반 사용자
    FE --> User: 403 Forbidden 페이지
    deactivate FE
else 관리자
    FE --> User: 업로드 폼 + 이력 테이블 표시
end

User -> FE: 데이터 유형 선택\nExcel 파일 선택\n업로드 버튼 클릭
FE -> FE: 클라이언트 측 검증\n(파일 형식, 크기)

alt 검증 실패
    FE --> User: 오류 메시지 표시
else 검증 성공
    FE --> User: 프로그레스 바 표시

    FE -> BE: POST /api/upload/excel/\nFormData (file, data_type)\n(Authorization: Bearer {token})
    activate BE

    BE -> BE: JWT 토큰 검증\n관리자 권한 확인

    BE -> BE: 파일 임시 저장

    BE -> Parser: parse(file_path)
    activate Parser
    Parser -> Parser: openpyxl로 Excel 열기\n헤더 행 인식\n데이터 행 파싱

    alt 파싱 오류 (파일 손상)
        Parser --> BE: Exception
        BE --> FE: 400 Bad Request
        FE --> User: "파일 손상" 오류 메시지
        deactivate Parser
        deactivate BE
        deactivate FE
    else 파싱 성공
        Parser --> BE: List[Dict] 데이터 반환
        deactivate Parser

        BE -> Validator: validate(data, data_type)
        activate Validator
        Validator -> Validator: 필수 컬럼 확인\n데이터 타입 검증\n중복 검사

        alt 검증 실패
            Validator --> BE: ValidationError\n(오류 행 정보 포함)
            BE --> FE: 400 Bad Request\n오류 상세 정보
            FE --> User: 오류 메시지\n(행 번호, 오류 내용)
            deactivate Validator
            deactivate BE
            deactivate FE
        else 검증 성공
            Validator --> BE: 검증 완료
            deactivate Validator

            BE -> DB: BEGIN TRANSACTION
            activate DB

            BE -> DB: Bulk Insert\n(performance/paper/student/budget)
            DB --> BE: 삽입 완료

            BE -> DB: 파일 메타데이터 저장\n(파일명, 업로드 일시, 행 수)
            DB --> BE: 저장 완료

            BE -> DB: COMMIT
            DB --> BE: 트랜잭션 성공
            deactivate DB

            BE --> FE: 201 Created\nJSON (id, filename, rows_processed)
            deactivate BE

            FE -> FE: 프로그레스 바 100%

            FE --> User: 성공 메시지\n"N행이 업로드되었습니다"\n업로드 이력 테이블 갱신\n[대시보드 보기] 버튼
            deactivate FE
        end
    end
end

@enduml
```

## Post-conditions

### Success
- Excel 파일의 데이터가 데이터베이스에 저장됨
- 파일 메타데이터가 업로드 이력에 기록됨
- 업로드 이력 테이블이 갱신됨
- 대시보드 캐시가 무효화되어 새 데이터가 즉시 반영됨
- 사용자는 [대시보드 보기] 버튼을 통해 결과를 확인할 수 있음

### Failure
- 데이터베이스에 데이터가 저장되지 않음 (트랜잭션 롤백)
- 임시 파일이 삭제됨
- 오류 메시지가 표시됨
- 사용자는 파일을 수정하거나 다시 시도할 수 있음

## Related Use Cases
- UC-002: 대시보드 조회 (업로드된 데이터가 대시보드에 표시됨)
- UC-004: 데이터 조회 (업로드된 데이터를 상세 조회 가능)
