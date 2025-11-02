# Railway 통합 배포 가이드

Django Backend와 React Frontend를 Railway에서 모두 배포하는 완전한 가이드입니다.

---

## 목차

1. [사전 준비](#사전-준비)
2. [Supabase 설정](#supabase-설정)
3. [Backend 배포 (Django)](#backend-배포-django)
4. [Frontend 배포 (React)](#frontend-배포-react)
5. [환경 변수 설정](#환경-변수-설정)
6. [도메인 설정](#도메인-설정)
7. [배포 후 테스트](#배포-후-테스트)
8. [트러블슈팅](#트러블슈팅)

---

## 사전 준비

### 1. 필요한 계정
- [Railway](https://railway.app/) 계정 (GitHub 계정으로 로그인)
- [Supabase](https://supabase.com/) 계정
- GitHub 계정 (코드 저장소)

### 2. 로컬 환경 확인
```bash
# Git이 설치되어 있는지 확인
git --version

# Python 3.11 설치 확인
python --version

# Node.js 18+ 설치 확인
node --version
npm --version
```

### 3. GitHub 저장소 푸시
```bash
# 로컬 코드를 GitHub에 Push
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Supabase 설정

### 1. Supabase 프로젝트 생성
1. [Supabase Dashboard](https://app.supabase.com/)에 로그인
2. **New Project** 클릭
3. 프로젝트 정보 입력:
   - **Name**: `university-dashboard`
   - **Database Password**: 강력한 비밀번호 생성 (안전하게 보관!)
   - **Region**: `Northeast Asia (Seoul)` 선택
4. **Create new project** 클릭

### 2. Supabase 연결 정보 확인

#### ⚠️ 중요: Connection Pooler 사용 (Railway 배포 필수!)

**Railway는 IPv6 아웃바운드 연결을 지원하지 않습니다.** Supabase Direct Connection(`db.*.supabase.co`)은 IPv6만 지원하므로 Railway에서 연결이 실패합니다.

**해결책: Supabase Connection Pooler (Supavisor) 사용**
- ✅ IPv4 + IPv6 모두 지원
- ✅ Connection Pooling 제공 (성능 향상)
- ✅ 추가 비용 없음

#### Connection Pooler 정보 확인 방법

1. **Settings** → **Database** → **Connection Pooling** 섹션으로 이동
2. **Session mode** 탭 선택 (Django 권장)
3. 연결 문자열 복사:
   ```
   postgresql://postgres.[PROJECT-ID]:[PASSWORD]@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
   ```

**중요한 차이점:**
- **USER**: `postgres.[PROJECT-ID]` (프로젝트 ID 포함!)
- **HOST**: `aws-0-[REGION].pooler.supabase.com` (Pooler 주소)
- **PORT**: `5432` (Session mode)

#### 추가 정보 확인

**Settings** → **API**에서:
- **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
- **anon public key**: `eyJhbG...` (공개 JWT 키)
- **JWT Secret**: (Show를 눌러 확인)

---

## Backend 배포 (Django)

### 1. Railway 프로젝트 생성
1. [Railway Dashboard](https://railway.app/dashboard)에 로그인
2. **New Project** → **Deploy from GitHub repo** 선택
3. GitHub 저장소 선택 후 Railway에 권한 허용
4. 저장소 선택 후 **Deploy Now** 클릭

### 2. Backend Service 설정
1. Railway 프로젝트에서 **New** → **GitHub Repo** 클릭
2. 저장소 선택 후 **Add variables** 클릭

#### Root Directory 설정
- **Settings** → **Service Settings** → **Root Directory** = `backend`

#### Build 설정 (자동 감지로 생략 가능)
Railway가 `.python-version`과 `requirements` 파일을 자동으로 감지합니다.

수동으로 설정하고 싶다면:
- **Build Command**: (비워둠 - Nixpacks 자동 감지)
- **Start Command**: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application`

### 3. Backend 환경 변수 설정
**Variables** 탭에서 다음 환경 변수를 추가:

```bash
# Django 배포 설정
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=여기에-랜덤-시크릿-키-생성-필요-50자
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}},your-custom-domain.com

# Database (Supabase Connection Pooler - Session Mode)
# ⚠️ 반드시 Connection Pooler 사용! (Direct Connection은 Railway에서 작동 안 함)
DATABASE_URL=postgresql://postgres.[PROJECT-ID]:YOUR_PASSWORD@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres

# 개별 변수 (선택사항 - DATABASE_URL 사용 시 불필요)
DB_NAME=postgres
DB_USER=postgres.[PROJECT-ID]
DB_PASSWORD=YOUR_SUPABASE_DB_PASSWORD
DB_HOST=aws-0-ap-northeast-2.pooler.supabase.com
DB_PORT=5432

# Supabase Auth
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=your-jwt-secret

# CORS (Frontend URL - 배포 후 업데이트)
CORS_ALLOWED_ORIGINS=https://your-frontend.railway.app,http://localhost:3000

# Security (Production)
SECURE_SSL_REDIRECT=True

# Sentry (선택사항 - 에러 모니터링)
SENTRY_DSN=
```

**SECRET_KEY 생성 방법:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Backend 배포 확인
1. Railway가 배포 로그를 보여줍니다 (Deployments 탭)
2. 배포 완료 후 **Settings** → **Generate Domain** 클릭
3. 생성된 도메인 확인: `https://your-backend.railway.app`
4. Health Check 테스트:
   ```bash
   curl https://your-backend.railway.app/api/health/
   # 응답: {"status":"healthy","service":"university-dashboard-api"}
   ```

---

## Frontend 배포 (React)

### 1. Frontend Service 생성
1. 같은 Railway 프로젝트에서 **New** → **GitHub Repo** 클릭
2. 같은 저장소 선택 (monorepo 구조)

### 2. Frontend Service 설정
#### Root Directory 설정
- **Settings** → **Service Settings** → **Root Directory** = `frontend`

#### Build 설정
Railway가 `package.json`을 자동으로 감지하지만, 확인 필요:
- **Build Command**: `npm run build`
- **Start Command**: (비워둠 - Docker 사용)

#### Dockerfile 사용 (권장)
Railway가 루트 디렉토리(`frontend/`)에 있는 `Dockerfile`을 자동으로 감지합니다.

만약 Dockerfile을 사용하지 않고 싶다면 다음으로 변경:
- **Start Command**: `npx serve -s dist -l $PORT`

### 3. Frontend 환경 변수 설정
**Variables** 탭에서 다음 환경 변수를 추가:

```bash
# API Backend URL (Backend 배포 완료 후 입력)
VITE_API_URL=https://your-backend.railway.app/api

# Supabase
VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Frontend 배포 확인
1. 배포 로그를 확인합니다
2. 배포 완료 후 **Settings** → **Generate Domain** 클릭
3. 생성된 도메인 확인: `https://your-frontend.railway.app`
4. 브라우저에서 접속 테스트

### 5. Backend CORS 업데이트
Frontend 도메인이 생성되었으므로 Backend 환경 변수를 업데이트:
1. Backend Service의 **Variables** 탭
2. `CORS_ALLOWED_ORIGINS` 업데이트:
   ```bash
   CORS_ALLOWED_ORIGINS=https://your-frontend.railway.app,http://localhost:3000
   ```
3. Backend 자동 재배포 (환경 변수 변경 시 자동 재배포됨)

---

## 환경 변수 설정

### Backend 필수 환경 변수 체크리스트
- [x] `DJANGO_SETTINGS_MODULE`
- [x] `SECRET_KEY`
- [x] `DEBUG`
- [x] `ALLOWED_HOSTS`
- [x] `DATABASE_URL`
- [x] `SUPABASE_URL`
- [x] `SUPABASE_ANON_KEY`
- [x] `SUPABASE_JWT_SECRET`
- [x] `CORS_ALLOWED_ORIGINS`

### Frontend 필수 환경 변수 체크리스트
- [x] `VITE_API_URL`
- [x] `VITE_SUPABASE_URL`
- [x] `VITE_SUPABASE_ANON_KEY`

---

## 도메인 설정

### Custom Domain 연결 (선택사항)

#### Backend
1. Backend Service → **Settings** → **Domains**
2. **Custom Domain** 클릭
3. 도메인 입력 (예: `api.yourdomain.com`)
4. DNS 설정에 CNAME 레코드 추가:
   ```
   Type: CNAME
   Name: api
   Value: your-backend.railway.app
   ```

#### Frontend
1. Frontend Service → **Settings** → **Domains**
2. **Custom Domain** 클릭
3. 도메인 입력 (예: `dashboard.yourdomain.com` 또는 `yourdomain.com`)
4. DNS 설정에 CNAME 또는 A 레코드 추가

---

## 배포 후 테스트

### 1. Backend 테스트
```bash
# Health check
curl https://your-backend.railway.app/api/health/

# Admin 페이지 접속
https://your-backend.railway.app/admin/

# API 문서 확인
https://your-backend.railway.app/api/docs/
```

### 2. Frontend 테스트
- 브라우저에서 `https://your-frontend.railway.app` 접속
- 개발자 도구(F12) → Network 탭 확인
  - API 호출이 정상적으로 Backend로 전송되는지 확인
  - CORS 에러가 발생하지 않는지 확인

### 3. Database 연결 확인
```bash
# Railway CLI 설치 (선택사항)
npm i -g @railway/cli

# Railway 로그인
railway login

# Backend 프로젝트 연결
railway link

# Django shell 실행
railway run python manage.py shell

# 데이터베이스 연결 테스트
>>> from django.db import connection
>>> connection.ensure_connection()
>>> print("Database connected!")
```

### 4. 추가 데이터베이스 설정
```bash
# Superuser 생성
railway run python manage.py createsuperuser

# Migrations 확인
railway run python manage.py showmigrations

# Static files 확인
railway run python manage.py collectstatic --noinput
```

---

## 트러블슈팅

### 문제 1: 배포 실패 (Build Error)

**증상**: Railway 배포 로그에 에러 발생

**해결 방법**:
```bash
# 1. requirements.txt 확인
cd backend/requirements
cat base.txt production.txt

# 2. 로컬에서 설치 테스트
pip install -r production.txt

# 3. Python 버전 확인
cat backend/.python-version  # 3.11이어야 함
```

### 문제 2: Database 연결 실패 (IPv6 문제)

**증상**:
```
django.db.utils.OperationalError: could not connect to server
Network is unreachable
could not translate host name to address
```

**원인**: Railway는 IPv6 아웃바운드 연결을 지원하지 않으며, Supabase Direct Connection은 IPv6만 지원합니다.

**해결 방법**:
1. ✅ **Connection Pooler 사용 (권장)**
   - Supabase Dashboard → Settings → Database → Connection Pooling
   - **Session mode** 선택
   - 연결 문자열 복사:
     ```bash
     postgresql://postgres.[PROJECT-ID]:password@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
     ```
   - Railway 환경 변수 `DATABASE_URL`에 입력

2. **연결 문자열 형식 확인**:
   ```bash
   # ❌ 잘못된 형식 (Direct Connection - Railway에서 작동 안 함)
   postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

   # ✅ 올바른 형식 (Connection Pooler - Railway에서 작동)
   postgresql://postgres.xxxxx:password@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
   ```

3. **USER 형식 확인**:
   - Direct Connection: `postgres`
   - Connection Pooler: `postgres.[PROJECT-ID]` ⚠️ 프로젝트 ID 포함 필수!

4. **대안 (추가 비용 발생)**:
   - Supabase IPv4 Add-on 구매 (월 $4)
   - Settings → Add-ons → IPv4 Address

### 문제 3: CORS 에러

**증상**: 브라우저 콘솔에서 `Access-Control-Allow-Origin` 에러

**해결 방법**:
1. Backend 환경 변수 확인:
   ```bash
   CORS_ALLOWED_ORIGINS=https://your-frontend.railway.app
   ```
2. Frontend URL이 정확한지 확인 (trailing slash 없이)
3. Backend 자동 재배포

### 문제 4: Static Files 404

**증상**: Admin 페이지 CSS가 로드되지 않음

**해결 방법**:
```bash
# WhiteNoise 설정 확인
# backend/config/settings/production.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# collectstatic 재실행
railway run python manage.py collectstatic --noinput --clear
```

### 문제 5: Frontend 빌드 실패

**증상**: Vite 빌드 중 에러 발생

**해결 방법**:
```bash
# 로컬에서 빌드 테스트
cd frontend
npm run build

# 타입 오류 확인
npm run type-check

# 수정 후 코드 재배포
git add .
git commit -m "Fix build errors"
git push
```

### 문제 6: 환경 변수가 인식 안됨

**증상**: Frontend에서 `import.meta.env.VITE_API_URL`이 undefined

**해결 방법**:
1. Railway Variables에서 `VITE_` 접두사 확인
2. 빌드 시점에 환경 변수가 적용되는지 확인
3. 재배포 (환경 변수 변경 후 반드시 재배포 필요)

---

## 유용한 Railway CLI 명령어

```bash
# Railway 로그인
railway login

# 프로젝트 연결
railway link

# 로그 확인
railway logs

# 환경 변수 확인
railway variables

# 프로젝트 정보
railway service

# 로컬에서 Railway 환경 변수로 실행
railway run python manage.py migrate
```

---

## 배포 체크리스트

### Backend
- [x] `.python-version` 파일 존재
- [x] `requirements/production.txt` 파일 존재
- [x] `Procfile` 또는 `railway.toml` 설정
- [x] `config/wsgi.py` 설정
- [x] `DJANGO_SETTINGS_MODULE=config.settings.production`
- [x] `SECRET_KEY` 설정
- [x] `ALLOWED_HOSTS` 설정
- [x] `DATABASE_URL` 설정
- [x] `CORS_ALLOWED_ORIGINS` 설정
- [x] WhiteNoise 설정
- [x] Health check 엔드포인트 (`/api/health/`)

### Frontend
- [x] `package.json` 존재
- [x] `vite.config.ts` 설정
- [x] `Dockerfile` (권장) 또는 빌드 명령어 설정
- [x] `nginx.conf` (Docker 사용 시)
- [x] `VITE_API_URL` 환경 변수
- [x] `VITE_SUPABASE_URL` 환경 변수
- [x] `VITE_SUPABASE_ANON_KEY` 환경 변수

### Database (Supabase)
- [x] Supabase 프로젝트 생성
- [x] Database 비밀번호 저장
- [x] Connection pooling 설정 (선택사항)
- [x] Migrations 실행

---

## 추가 리소스

- [Railway 공식 문서](https://docs.railway.app/)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Vite 배포 가이드](https://vitejs.dev/guide/static-deploy.html)
- [Supabase 문서](https://supabase.com/docs)

---

## 지원

문제가 발생하면 다음을 확인하세요:
1. Railway 배포 로그
2. Backend Django 로그 (`railway logs`)
3. Frontend 브라우저 콘솔
4. GitHub Actions (CI/CD 설정 시)

**Happy Deploying! 🚀**
