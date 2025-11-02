# 🚀 빠른 시작 가이드

이 문서는 프로젝트를 **가장 빠르게** 로컬에서 실행하는 방법을 안내합니다.

---

## ⚡ 5분 안에 시작하기

### 📋 사전 준비 (한 번만)

1. **Supabase 프로젝트 생성**
   - [Supabase](https://supabase.com/)에서 무료 계정 생성
   - 새 프로젝트 생성
   - 프로젝트 설정 메모:
     ```
     Settings > API:
     - Project URL: https://xxxxx.supabase.co
     - Anon/Public Key: eyJhbGci...
     - JWT Secret: your-jwt-secret

     Settings > Database:
     - Host: db.xxxxx.supabase.co
     - Password: 프로젝트 생성 시 설정한 비밀번호
     ```

2. **필수 프로그램 설치**
   - [Python 3.11+](https://www.python.org/downloads/)
   - [Node.js 18+](https://nodejs.org/)

---

## 🔧 설정 단계

### 1️⃣ Supabase 정보 입력

#### ℹ️ 로컬 개발 환경 데이터베이스

**로컬에서는 SQLite 사용 (기본 설정)**
- 데이터베이스 연결 설정 불필요
- Supabase는 인증(Auth)에만 사용

**프로덕션(Railway)에서는 Supabase PostgreSQL 사용**
- Connection Pooler로 연결
- IPv6 문제 해결됨

#### 백엔드 설정
`backend/.env` 파일을 열고 Supabase 인증 정보만 입력:

```bash
# Supabase (인증에만 사용)
SUPABASE_URL=https://여기에_프로젝트_REF.supabase.co
SUPABASE_ANON_KEY=여기에_ANON_KEY
SUPABASE_JWT_SECRET=여기에_JWT_SECRET
```

**참고**: 데이터베이스 설정(`DATABASE_URL` 등)은 로컬에서 불필요합니다.

#### 프론트엔드 설정
`frontend/.env` 파일을 열고 다음 항목을 실제 값으로 교체:

```bash
VITE_SUPABASE_URL=https://여기에_프로젝트_REF.supabase.co
VITE_SUPABASE_ANON_KEY=여기에_ANON_KEY
```

---

### 2️⃣ 백엔드 설정 및 실행

#### Windows 사용자

```cmd
cd backend
setup_local.bat
```

설정이 완료되면:

```cmd
run_server.bat
```

#### Mac/Linux 사용자

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

✅ **백엔드 실행 확인**: http://localhost:8000/api/

---

### 3️⃣ 프론트엔드 설정 및 실행

**새 터미널을 열고** (백엔드는 계속 실행):

#### Windows 사용자

```cmd
cd frontend
setup_local.bat
```

설정이 완료되면:

```cmd
run_dev.bat
```

#### Mac/Linux 사용자

```bash
cd frontend
npm install
npm run dev
```

✅ **프론트엔드 실행 확인**: http://localhost:5173

---

## 🎯 다음 단계

### 1. 관리자 계정 생성 (선택사항)

백엔드 터미널에서:

```bash
python manage.py createsuperuser
```

이메일, 사용자명, 비밀번호를 입력하고 http://localhost:8000/admin/ 에서 로그인

### 2. 프론트엔드 접속

브라우저에서 http://localhost:5173 을 열어 애플리케이션 테스트

### 3. API 테스트

- http://localhost:8000/api/ - API 루트
- http://localhost:8000/api/dashboard/ - 대시보드 API
- http://localhost:8000/api/uploads/ - 업로드 API

---

## 🔄 다음 실행부터

### 백엔드 시작

```cmd
cd backend
run_server.bat
```

또는 수동으로:

```cmd
cd backend
venv\Scripts\activate
python manage.py runserver
```

### 프론트엔드 시작

```cmd
cd frontend
run_dev.bat
```

또는 수동으로:

```cmd
cd frontend
npm run dev
```

---

## 🆘 문제 해결

### 백엔드 문제

#### "No module named 'django'"
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements\development.txt
```

#### 데이터베이스 연결 오류
1. `.env` 파일의 Supabase 정보가 정확한지 확인
2. Supabase 프로젝트가 활성 상태인지 확인
3. [Supabase Dashboard](https://app.supabase.com/)에서 프로젝트 상태 확인

#### 포트 이미 사용 중
```cmd
# 다른 포트로 실행
python manage.py runserver 8001
```

### 프론트엔드 문제

#### "Cannot find module"
```cmd
cd frontend
npm install
```

#### API 연결 오류
1. 백엔드가 실행 중인지 확인 (http://localhost:8000)
2. `.env` 파일의 `VITE_API_URL`이 `http://localhost:8000/api`인지 확인
3. CORS 설정 확인 (백엔드 `.env`의 `CORS_ALLOWED_ORIGINS`)

#### 포트 이미 사용 중
Vite가 자동으로 다른 포트를 할당하거나, `vite.config.ts`에서 포트 변경:

```typescript
export default defineConfig({
  server: {
    port: 5174  // 다른 포트 번호
  }
})
```

---

## 📁 프로젝트 구조 확인

```
final_mafia_challenge/
├── backend/
│   ├── venv/                    # Python 가상환경
│   ├── config/                  # Django 설정
│   ├── apps/                    # Django 앱들
│   ├── .env                     # 환경 변수 (직접 생성)
│   ├── setup_local.bat          # 설정 스크립트
│   └── run_server.bat           # 실행 스크립트
│
├── frontend/
│   ├── node_modules/            # npm 패키지
│   ├── src/                     # React 소스 코드
│   ├── .env                     # 환경 변수 (직접 생성)
│   ├── setup_local.bat          # 설정 스크립트
│   └── run_dev.bat              # 실행 스크립트
│
├── docs/                        # 설계 문서
├── LOCAL_SETUP.md               # 상세 설정 가이드
├── QUICKSTART.md                # 이 파일
└── DEPLOYMENT.md                # 배포 가이드
```

---

## 📚 추가 문서

- **[LOCAL_SETUP.md](./LOCAL_SETUP.md)** - 상세한 로컬 설정 가이드
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - 프로덕션 배포 가이드
- **[CLAUDE.md](./CLAUDE.md)** - 프로젝트 아키텍처 문서

---

## ✅ 체크리스트

설정 전:
- [ ] Python 3.11+ 설치됨
- [ ] Node.js 18+ 설치됨
- [ ] Supabase 프로젝트 생성됨
- [ ] Supabase 정보 메모함

백엔드 설정:
- [ ] `backend/.env` 파일 생성 및 수정
- [ ] 가상환경 생성 및 활성화
- [ ] 패키지 설치
- [ ] 마이그레이션 실행
- [ ] 서버 실행 확인 (http://localhost:8000)

프론트엔드 설정:
- [ ] `frontend/.env` 파일 생성 및 수정
- [ ] npm 패키지 설치
- [ ] 개발 서버 실행 확인 (http://localhost:5173)

---

## 🎓 학습 리소스

- [Django 튜토리얼](https://docs.djangoproject.com/ko/5.0/intro/tutorial01/)
- [React 공식 문서](https://react.dev/learn)
- [Supabase 문서](https://supabase.com/docs)

---

**문제가 계속되면?**

1. 에러 메시지 전체 복사
2. `LOCAL_SETUP.md` 문서의 문제 해결 섹션 확인
3. GitHub Issues에 질문 등록

**Happy Coding! 🎉**
