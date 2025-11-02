# 로컬 개발 환경 설정 가이드

이 문서는 프로젝트를 로컬 환경에서 실행하고 테스트하는 방법을 안내합니다.

## 사전 요구사항

### 필수 설치 항목
1. **Python 3.11+** - [Python 다운로드](https://www.python.org/downloads/)
2. **Node.js 18+** - [Node.js 다운로드](https://nodejs.org/)
3. **PostgreSQL** (선택사항 - Supabase 사용 시 불필요)
4. **Git** - [Git 다운로드](https://git-scm.com/downloads)

### Supabase 프로젝트 설정
1. [Supabase](https://supabase.com/)에서 무료 계정 생성
2. 새 프로젝트 생성
3. 프로젝트 설정에서 다음 정보 확인:
   - Project URL (Settings > API)
   - Anon/Public Key (Settings > API)
   - JWT Secret (Settings > API)
   - Database 연결 정보 (Settings > Database)

---

## 백엔드 설정 (Django)

### 1. Python 가상환경 생성 및 활성화

```bash
# Windows
cd backend
python -m venv venv
venv\Scripts\activate

# Mac/Linux
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 패키지 설치

```bash
pip install -r requirements/development.txt
```

### 3. 환경 변수 설정

#### ℹ️ 로컬 개발 환경의 데이터베이스

**현재 설정: SQLite 사용 (권장)**

로컬 개발 환경에서는 **SQLite**를 사용하도록 설정되어 있습니다.

**왜 SQLite를 사용하나요?**
- ✅ 설정 불필요 (Python 내장)
- ✅ 빠르고 간단함
- ✅ Supabase IPv6 연결 문제 회피
  - Supabase Direct Connection은 IPv6만 지원
  - 로컬 환경에서 IPv6 연결이 안 되는 경우가 많음

**프로덕션 환경과의 차이:**
- **로컬**: SQLite (`backend/db.sqlite3`)
- **프로덕션 (Railway)**: Supabase PostgreSQL (Connection Pooler 사용)

#### 환경 변수 파일 생성 (최소 설정)

`.env` 파일을 backend 디렉토리에 생성:

```bash
# backend/.env
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=your-local-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase (인증에만 사용)
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
SUPABASE_JWT_SECRET=[YOUR-JWT-SECRET]

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Security (Local Development)
SECURE_SSL_REDIRECT=False
```

**중요**: `[YOUR-PROJECT-REF]`, `[YOUR-ANON-KEY]`, `[YOUR-JWT-SECRET]`를 실제 Supabase 프로젝트 정보로 교체하세요.

#### PostgreSQL을 로컬에서도 사용하고 싶다면? (선택사항)

`.env` 파일에 추가:

```bash
# Database (Supabase Connection Pooler - 로컬에서도 사용 가능)
# ⚠️ Direct Connection(db.*.supabase.co)은 IPv6 문제로 작동하지 않을 수 있음
DATABASE_URL=postgresql://postgres.[PROJECT-ID]:[PASSWORD]@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
```

그리고 `config/settings/development.py`에서 SQLite 설정을 주석 처리하고 PostgreSQL 설정을 활성화하세요.

### 4. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 관리자 계정 생성 (선택사항)

```bash
python manage.py createsuperuser
```

### 6. 개발 서버 실행

```bash
python manage.py runserver
```

서버가 `http://localhost:8000`에서 실행됩니다.

#### API 엔드포인트 확인

- Admin: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/
- Dashboard API: http://localhost:8000/api/dashboard/
- Upload API: http://localhost:8000/api/uploads/

---

## 프론트엔드 설정 (React)

### 1. Node.js 패키지 설치

```bash
cd frontend
npm install
```

### 2. 환경 변수 설정

`.env` 파일을 frontend 디렉토리에 생성:

```bash
# frontend/.env
VITE_API_URL=http://localhost:8000/api

# Supabase
VITE_SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
VITE_SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
```

**중요**: `[YOUR-PROJECT-REF]`, `[YOUR-ANON-KEY]`를 실제 Supabase 프로젝트 정보로 교체하세요.

### 3. 개발 서버 실행

```bash
npm run dev
```

프론트엔드가 `http://localhost:5173`에서 실행됩니다.

---

## 로컬 테스트 워크플로우

### 1. 두 서버 모두 실행

**Terminal 1 - 백엔드**:
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
python manage.py runserver
```

**Terminal 2 - 프론트엔드**:
```bash
cd frontend
npm run dev
```

### 2. 브라우저에서 접속

- 프론트엔드: http://localhost:5173
- 백엔드 Admin: http://localhost:8000/admin/

### 3. 기능 테스트

1. **사용자 등록 및 로그인**
   - Supabase Auth를 통한 인증 테스트

2. **파일 업로드**
   - Excel 파일 업로드 기능 테스트

3. **대시보드 조회**
   - 데이터 시각화 차트 확인

---

## 데이터베이스 관리

### Supabase 대시보드 사용

1. [Supabase Dashboard](https://app.supabase.com/)에 로그인
2. 프로젝트 선택
3. Table Editor에서 데이터 직접 확인/수정 가능
4. SQL Editor에서 커스텀 쿼리 실행 가능

### Django Admin 사용

1. http://localhost:8000/admin/ 접속
2. 슈퍼유저 계정으로 로그인
3. 모델 데이터 CRUD 작업 수행

---

## 샘플 데이터 추가

### 방법 1: Django Admin을 통한 수동 추가

1. http://localhost:8000/admin/ 접속
2. 각 모델에 대해 수동으로 데이터 추가

### 방법 2: 시드 스크립트 실행 (작성 필요)

```bash
python manage.py shell
```

```python
from apps.dashboard.persistence.models import Performance, Paper, Student, Budget
from decimal import Decimal

# 샘플 데이터 생성
Performance.objects.create(
    year=2024,
    department="컴퓨터공학과",
    metric_name="연구비 수주액",
    value=Decimal("50000000"),
    unit="원"
)
```

---

## 문제 해결

### 백엔드 오류

#### 1. `ModuleNotFoundError: No module named 'xyz'`
```bash
pip install -r requirements/development.txt
```

#### 2. 데이터베이스 연결 오류 (IPv6 문제)

**증상**:
```
django.db.utils.OperationalError: could not connect to server
could not translate host name to address
Network is unreachable
```

**원인**: Supabase Direct Connection(`db.*.supabase.co`)은 IPv6만 지원하며, 로컬 환경에서 IPv6 연결이 안 되는 경우가 많습니다.

**해결 방법**:

1. **SQLite 사용 (권장)** - 기본 설정
   - `config/settings/development.py`에서 이미 SQLite로 설정되어 있음
   - 데이터베이스 설정 불필요

2. **PostgreSQL을 꼭 사용해야 한다면**:
   - Supabase Connection Pooler 사용
   - `.env`에 다음 추가:
     ```bash
     DATABASE_URL=postgresql://postgres.[PROJECT-ID]:password@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
     ```
   - `config/settings/development.py`에서 PostgreSQL 설정 활성화

3. **확인 사항**:
   - Supabase 프로젝트가 활성 상태인지 확인
   - 방화벽이 PostgreSQL 포트(5432, 6543)를 차단하지 않는지 확인

#### 3. CORS 오류
- `config/settings/development.py`의 `CORS_ALLOWED_ORIGINS`에 프론트엔드 URL이 포함되어 있는지 확인

### 프론트엔드 오류

#### 1. `Cannot find module 'xyz'`
```bash
npm install
```

#### 2. API 연결 오류
- 백엔드 서버가 실행 중인지 확인
- `.env` 파일의 `VITE_API_URL`이 정확한지 확인

#### 3. Supabase Auth 오류
- `.env` 파일의 Supabase 설정이 정확한지 확인
- Supabase 프로젝트의 Authentication 설정 확인

---

## 개발 팁

### 1. Hot Reload
- Django: 코드 변경 시 자동으로 서버가 재시작됩니다
- React: 코드 변경 시 브라우저가 자동으로 새로고침됩니다

### 2. 디버깅

**Django**:
```python
# views.py
import pdb; pdb.set_trace()  # 브레이크포인트 설정
```

**React**:
```typescript
console.log('디버깅:', data);
debugger;  // 브레이크포인트 설정
```

### 3. Django Debug Toolbar

개발 모드에서 자동으로 활성화됩니다:
- http://localhost:8000/ 접속 시 우측에 디버그 패널 표시
- SQL 쿼리, 성능, 캐시 정보 확인 가능

### 4. 로그 확인

**Django**:
```bash
# settings에서 LOGGING 설정 확인
tail -f logs/django.log  # 로그 파일 실시간 확인
```

---

## 테스트 실행

### 백엔드 테스트

```bash
cd backend
pytest
# 또는
python manage.py test
```

### 프론트엔드 테스트

```bash
cd frontend
npm test
```

---

## 다음 단계

1. ✅ 로컬 환경 설정 완료
2. 📝 기능 개발 및 테스트
3. 🚀 배포 준비 (DEPLOYMENT.md 참고)

---

## 추가 리소스

- [Django 공식 문서](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React 공식 문서](https://react.dev/)
- [Vite 공식 문서](https://vitejs.dev/)
- [Supabase 공식 문서](https://supabase.com/docs)
- [Material-UI 공식 문서](https://mui.com/)

---

## 도움이 필요하신가요?

문제가 발생하면 다음을 확인하세요:
1. 모든 환경 변수가 올바르게 설정되었는지
2. 필요한 서비스(PostgreSQL, Node.js, Python)가 실행 중인지
3. 방화벽이나 보안 소프트웨어가 포트를 차단하지 않는지

여전히 문제가 해결되지 않으면 이슈를 생성하거나 팀에 문의하세요.
