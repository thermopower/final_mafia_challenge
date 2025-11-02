# Railway 배포 가이드

## 현재 상황
빌드는 성공했지만 헬스체크가 실패하는 상황입니다.

## 문제 원인
Railway 환경변수가 설정되지 않아 Django 앱이 시작되지 않습니다.

---

## Railway 환경변수 설정 (필수)

Railway Dashboard > Your Project > Variables 탭에서 다음 환경변수를 추가하세요:

### 1. Django 기본 설정

```bash
# Django Settings Module
DJANGO_SETTINGS_MODULE=config.settings.production

# Secret Key (50자 이상의 랜덤 문자열 생성 필요)
# Python으로 생성: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your-generated-secret-key-here-minimum-50-characters-long

# Debug (프로덕션에서는 반드시 False)
DEBUG=False

# Allowed Hosts (Railway가 자동으로 제공하는 도메인 변수 사용)
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}},localhost,127.0.0.1
```

### 2. Database (Supabase PostgreSQL) - 필수!

**중요**: Database 설정은 **반드시** 다음 두 방법 중 하나를 선택해야 합니다.

#### 방법 1: DATABASE_URL 사용 (권장)

```bash
# Database URL (Supabase Connection Pooler - Session Mode)
DATABASE_URL=postgresql://postgres.atdtzgamsgpnkzjlktlo:JGu6OVp6vIVBibMM@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
```

#### 방법 2: 개별 DB 변수 사용

DATABASE_URL을 설정하지 **않으면** 다음 변수들을 **모두** 설정해야 합니다:

```bash
DB_NAME=postgres
DB_USER=postgres.atdtzgamsgpnkzjlktlo
DB_PASSWORD=JGu6OVp6vIVBibMM
DB_HOST=aws-1-ap-southeast-2.pooler.supabase.com
DB_PORT=5432
```

**주의**: DATABASE_URL이 설정되면 개별 DB 변수는 무시됩니다.

### 3. Supabase Auth

```bash
# Supabase URL
SUPABASE_URL=https://atdtzgamsgpnkzjlktlo.supabase.co

# Supabase Anon Key
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF0ZHR6Z2Ftc2dwbmt6amxrdGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMTU2NDksImV4cCI6MjA3NzU5MTY0OX0.WzhfhNjHSCEpSAjT8x5kw3gEhWisMAEtl5iYlnrVtgk

# Supabase JWT Secret
SUPABASE_JWT_SECRET=ADP1DHEVkX/mc8iNh8bJqjphRXDQr53DjoP76jr9jKjI/8PKD3L8reukRErm0beZF1mMZGnl0weXYyRwTs05zg==
```

### 4. CORS (Frontend URL 설정)

```bash
# 프론트엔드 배포 후 URL을 여기에 추가
# 예: CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.railway.app
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 5. Security (선택사항)

```bash
# SSL Redirect (HTTPS 강제 - Railway는 자동으로 HTTPS 제공)
SECURE_SSL_REDIRECT=True

# Sentry DSN (에러 모니터링 - 선택사항)
# SENTRY_DSN=https://your-sentry-dsn-here
```

---

## 환경변수 설정 방법

### Railway Dashboard에서 설정:

1. **Railway Dashboard 접속**
   - https://railway.app/dashboard

2. **프로젝트 선택**
   - 배포한 프로젝트 클릭

3. **Variables 탭 이동**
   - 상단 메뉴에서 "Variables" 클릭

4. **환경변수 추가** (필수 순서대로)

   **최소 필수 변수 (반드시 설정해야 함):**
   1. `DJANGO_SETTINGS_MODULE` = `config.settings.production`
   2. `SECRET_KEY` = (생성된 시크릿 키)
   3. `DATABASE_URL` = `postgresql://postgres.atdtzgamsgpnkzjlktlo:JGu6OVp6vIVBibMM@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres`
   4. `ALLOWED_HOSTS` = `${{RAILWAY_PUBLIC_DOMAIN}},localhost,127.0.0.1`
   5. `DEBUG` = `False`

   **Supabase 변수 (인증 기능 사용 시 필수):**
   6. `SUPABASE_URL` = `https://atdtzgamsgpnkzjlktlo.supabase.co`
   7. `SUPABASE_ANON_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   8. `SUPABASE_JWT_SECRET` = `ADP1DHEVkX/mc8iNh8bJqjphRXDQr53Djo...`

5. **자동 재배포**
   - 환경변수를 저장하면 Railway가 자동으로 재배포합니다
   - 재배포 완료 후 헬스체크가 성공해야 합니다

6. **DATABASE_URL 확인**
   - 가장 흔한 에러: DATABASE_URL 누락
   - 반드시 위의 전체 URL을 정확히 입력하세요
   - 공백이나 줄바꿈이 있으면 안 됩니다

---

## SECRET_KEY 생성 방법

로컬에서 다음 명령어를 실행하여 SECRET_KEY를 생성하세요:

```bash
# Windows (PowerShell)
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 또는 Python shell에서
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

생성된 키를 복사하여 Railway Variables에 `SECRET_KEY`로 추가하세요.

---

## 도메인 생성 (Generate Domain)

Railway는 자동으로 도메인을 생성하지만, 수동으로 생성하려면:

1. **Railway Dashboard > Settings 탭**
2. **Networking 섹션**
3. **Generate Domain 버튼 클릭**

생성된 도메인은 `your-app-name.up.railway.app` 형식입니다.

**중요**: 도메인이 생성되면 `ALLOWED_HOSTS`에 자동으로 추가됩니다 (`${{RAILWAY_PUBLIC_DOMAIN}}` 변수 사용).

---

## 배포 확인

환경변수 설정 후:

1. **Deploy Logs 확인**
   - Railway Dashboard > Deployments 탭
   - 최신 배포 로그 확인
   - 에러가 없는지 확인

2. **헬스체크 확인**
   - 배포 완료 후 헬스체크가 성공하는지 확인
   - 성공 시: 초록색 체크 표시

3. **API 테스트**
   ```bash
   # 생성된 도메인으로 테스트
   curl https://your-app-name.up.railway.app/api/health/

   # 응답 예시:
   # {"status":"healthy","service":"university-dashboard-api"}
   ```

---

## 문제 해결

### 헬스체크 실패 시

1. **Deploy Logs 확인**
   - 에러 메시지 확인
   - 환경변수 누락 여부 확인

2. **일반적인 에러**
   - `SECRET_KEY` 누락
   - `DATABASE_URL` 오류 (DB 연결 실패)
   - `ALLOWED_HOSTS` 설정 오류

3. **로그에서 찾아야 할 것**
   ```
   django.core.exceptions.ImproperlyConfigured
   KeyError: 'SECRET_KEY'
   OperationalError: could not connect to database
   DisallowedHost at /
   ```

---

## Frontend 배포 (다음 단계)

Backend 배포 완료 후 Frontend를 별도로 배포하세요:

### 옵션 1: Vercel (권장)
1. GitHub 레포지토리 연결
2. Build Command: `cd frontend && npm run build`
3. Output Directory: `frontend/dist`
4. 환경변수 추가:
   ```
   VITE_API_URL=https://your-backend.up.railway.app/api
   VITE_SUPABASE_URL=https://atdtzgamsgpnkzjlktlo.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGci...
   ```

### 옵션 2: Railway (별도 서비스)
1. New Project 생성
2. frontend 폴더만 선택
3. 환경변수 설정 (위와 동일)

### Frontend 배포 후
Backend의 `CORS_ALLOWED_ORIGINS`에 Frontend URL 추가:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

---

## 요약

**지금 해야 할 일:**

1. ✅ 빌드 성공 (완료)
2. ⏳ Railway Variables에 환경변수 추가 (현재 단계)
   - 최소 필수: `SECRET_KEY`, `DATABASE_URL`, `DJANGO_SETTINGS_MODULE`, `ALLOWED_HOSTS`
3. ⏳ 재배포 대기
4. ⏳ 헬스체크 성공 확인
5. ⏳ API 엔드포인트 테스트

**도메인 생성은 필수가 아닙니다.** Railway가 자동으로 생성하거나, Settings에서 Generate Domain을 클릭하면 됩니다.

**핵심은 환경변수 설정입니다!**
