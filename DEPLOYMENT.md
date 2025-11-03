# 배포 가이드 (Hybrid Deployment)

## 배포 아키텍처

이 프로젝트는 **하이브리드 배포** 방식을 사용합니다:

```
┌─────────────────────────────────────────┐
│         Hybrid Deployment               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │    │  Frontend    │  │
│  │   (Railway)  │◄───┤  (Vercel)    │  │
│  │              │    │              │  │
│  │  Django API  │    │  React SPA   │  │
│  │  Port: 8000  │    │              │  │
│  └──────┬───────┘    └──────────────┘  │
│         │                               │
│         │                               │
│  ┌──────▼───────────────────────────┐  │
│  │  Supabase PostgreSQL + Auth      │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**백엔드**: Railway (Django REST API)
**프론트엔드**: Vercel (React SPA)
**데이터베이스**: Supabase (PostgreSQL)
**인증**: Supabase Auth

---

## 1. 백엔드 배포 (Railway)

### 1.1 Railway 프로젝트 생성

1. **Railway Dashboard 접속**
   - https://railway.app/dashboard

2. **New Project 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 레포지토리 선택

3. **Service 설정**
   - Service 이름: `backend` (또는 원하는 이름)
   - **Settings** > **Root Directory**: `/backend` 설정 (중요!)
   - Railway가 자동으로 `backend/nixpacks.toml`과 `backend/railway.json`을 감지합니다

### 1.2 환경변수 설정 (필수)

Railway Dashboard > Backend Service > **Variables** 탭에서 다음 환경변수를 추가:

#### 기본 설정 (필수)
```bash
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
```

#### SECRET_KEY 생성 및 설정
로컬에서 다음 명령어 실행:
```bash
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

생성된 키를 Railway Variables에 추가:
```bash
SECRET_KEY=<생성된-시크릿-키-50자-이상>
```

#### 데이터베이스 설정 (Supabase)
```bash
# DATABASE_URL 방식 (권장)
DATABASE_URL=postgresql://postgres.atdtzgamsgpnkzjlktlo:JGu6OVp6vIVBibMM@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
```

#### ALLOWED_HOSTS 설정
```bash
# 첫 배포 시: Railway의 모든 도메인 허용
ALLOWED_HOSTS=.railway.app,localhost,127.0.0.1

# 배포 완료 후 특정 도메인으로 변경 (권장):
# ALLOWED_HOSTS=backend-production-xxxx.up.railway.app,localhost,127.0.0.1
```

**중요**:
- 첫 배포 시에는 Railway 도메인이 아직 생성되지 않았으므로 `.railway.app` (모든 Railway 하위 도메인 허용)을 사용합니다
- 배포 완료 후 Settings > Networking에서 생성된 도메인을 확인한 뒤, 해당 도메인으로 변경하는 것이 보안상 권장됩니다

#### CORS 설정 (프론트엔드 도메인 - 배포 후 업데이트)
```bash
# 초기값 (로컬 개발용)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Vercel 배포 후 업데이트할 값:
# CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
```

#### Supabase 설정
```bash
SUPABASE_URL=https://atdtzgamsgpnkzjlktlo.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF0ZHR6Z2Ftc2dwbmt6amxrdGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMTU2NDksImV4cCI6MjA3NzU5MTY0OX0.WzhfhNjHSCEpSAjT8x5kw3gEhWisMAEtl5iYlnrVtgk
SUPABASE_JWT_SECRET=ADP1DHEVkX/mc8iNh8bJqjphRXDQr53DjoP76jr9jKjI/8PKD3L8reukRErm0beZF1mMZGnl0weXYyRwTs05zg==
```

### 1.3 배포 확인

1. **Deploy Logs 확인**
   - Railway Dashboard > Deployments 탭
   - 빌드 및 배포 로그 확인

2. **헬스체크 확인**
   - 배포 완료 후 녹색 체크 표시 확인
   - `/api/health/` 엔드포인트 자동 체크

3. **API 테스트**
   ```bash
   curl https://your-backend.up.railway.app/api/health/
   # 응답: {"status":"healthy","service":"university-dashboard-api"}
   ```

4. **도메인 확인**
   - Railway가 자동으로 생성한 도메인 확인
   - 예: `backend-production-xxxx.up.railway.app`
   - **이 도메인을 복사해서 프론트엔드 환경변수에 사용합니다**

---

## 2. 프론트엔드 배포 (Vercel)

### 2.1 Vercel 프로젝트 생성

1. **Vercel Dashboard 접속**
   - https://vercel.com/dashboard

2. **New Project 생성**
   - "Add New..." > "Project" 클릭
   - GitHub 레포지토리 선택

3. **프로젝트 설정**
   - Framework Preset: **Vite** (자동 감지됨)
   - **Root Directory**: `frontend` ← **폴더 아이콘 클릭 후 선택 (중요!)**
   - Build Command: `npm run build` (자동 설정됨)
   - Output Directory: `dist` (자동 설정됨)
   - Install Command: `npm install` (자동 설정됨)

### 2.2 환경변수 설정 (필수)

Vercel Dashboard > Your Project > **Settings** > **Environment Variables**에서 추가:

#### API URL (백엔드 Railway 도메인)
```bash
VITE_API_URL=https://your-backend.up.railway.app/api
```

#### Supabase 설정
```bash
VITE_SUPABASE_URL=https://atdtzgamsgpnkzjlktlo.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF0ZHR6Z2Ftc2dwbmt6amxrdGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMTU2NDksImV4cCI6MjA3NzU5MTY0OX0.WzhfhNjHSCEpSAjT8x5kw3gEhWisMAEtl5iYlnrVtgk
```

**중요**: 환경변수 설정 후 **"Redeploy"** 버튼을 클릭하여 재배포해야 적용됩니다.

### 2.3 배포 확인

1. **Deployment 로그 확인**
   - Vercel Dashboard > Deployments 탭
   - 빌드 및 배포 로그 확인

2. **도메인 확인**
   - Vercel이 자동으로 생성한 도메인 확인
   - 예: `your-project.vercel.app`

3. **웹사이트 접속 테스트**
   - 브라우저에서 도메인 접속
   - 로그인, 대시보드 등 주요 기능 테스트

---

## 3. CORS 설정 업데이트 (중요!)

프론트엔드 배포 완료 후, **백엔드 CORS 설정을 반드시 업데이트**해야 합니다.

### 3.1 Railway에서 CORS_ALLOWED_ORIGINS 업데이트

Railway Dashboard > Backend Service > **Variables**:

```bash
# Vercel 도메인을 추가
CORS_ALLOWED_ORIGINS=https://your-project.vercel.app,http://localhost:5173
```

**형식 주의**:
- 쉼표(`,`)로 구분
- 공백 없이
- `https://` 포함 (Vercel은 자동으로 HTTPS 제공)
- localhost는 개발용으로 유지 가능

### 3.2 재배포 확인

- 환경변수 저장 시 Railway가 자동으로 재배포됩니다
- Deploy Logs에서 재배포 완료 확인

---

## 4. 전체 배포 플로우 요약

### 단계별 체크리스트

#### ✅ 1단계: 백엔드 배포 (Railway)
- [ ] Railway 프로젝트 생성
- [ ] Root Directory를 `/backend`로 설정
- [ ] 환경변수 설정 (SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS 등)
  - **ALLOWED_HOSTS**: `.railway.app,localhost,127.0.0.1` (첫 배포 시)
- [ ] 배포 완료 및 헬스체크 성공 확인
- [ ] 백엔드 도메인 확인 및 복사 (예: backend-production-xxxx.up.railway.app)
- [ ] *(선택) ALLOWED_HOSTS를 특정 도메인으로 변경* (보안 강화)

#### ✅ 2단계: 프론트엔드 배포 (Vercel)
- [ ] Vercel 프로젝트 생성
- [ ] Root Directory를 `frontend`로 설정
- [ ] 환경변수 설정 (VITE_API_URL에 백엔드 도메인 입력)
- [ ] 배포 완료 확인
- [ ] 프론트엔드 도메인 확인 및 복사 (예: your-project.vercel.app)

#### ✅ 3단계: CORS 설정 (Railway)
- [ ] Railway 환경변수 `CORS_ALLOWED_ORIGINS`에 Vercel 도메인 추가
- [ ] 재배포 완료 확인

#### ✅ 4단계: 테스트
- [ ] 프론트엔드 접속 확인
- [ ] 로그인 기능 테스트
- [ ] API 호출 테스트 (CORS 에러 없는지 확인)
- [ ] 데이터 업로드/조회 테스트

---

## 5. 환경변수 전체 목록

### Backend (Railway)

| 변수명 | 설명 | 필수 | 예시 |
|--------|------|------|------|
| `DJANGO_SETTINGS_MODULE` | Django 설정 모듈 | ✅ | `config.settings.production` |
| `SECRET_KEY` | Django 시크릿 키 | ✅ | `django-insecure-xxx...` (50자 이상) |
| `DEBUG` | 디버그 모드 | ✅ | `False` |
| `DATABASE_URL` | PostgreSQL 연결 URL | ✅ | `postgresql://user:pass@host:5432/db` |
| `ALLOWED_HOSTS` | 허용 도메인 | ✅ | `.railway.app` (첫 배포) 또는 `backend-xxx.railway.app` (배포 후) |
| `CORS_ALLOWED_ORIGINS` | CORS 허용 도메인 | ✅ | `https://your-app.vercel.app` |
| `SUPABASE_URL` | Supabase 프로젝트 URL | ✅ | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase Anon Key | ✅ | `eyJhbGci...` |
| `SUPABASE_JWT_SECRET` | Supabase JWT Secret | ✅ | `ADP1DHE...` |
| `SENTRY_DSN` | Sentry 에러 추적 (선택) | ❌ | `https://xxx@sentry.io/xxx` |

### Frontend (Vercel)

| 변수명 | 설명 | 필수 | 예시 |
|--------|------|------|------|
| `VITE_API_URL` | 백엔드 API URL | ✅ | `https://backend-xxx.railway.app/api` |
| `VITE_SUPABASE_URL` | Supabase 프로젝트 URL | ✅ | `https://xxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Supabase Anon Key | ✅ | `eyJhbGci...` |

---

## 6. 문제 해결

### 백엔드 배포 실패

#### 헬스체크 실패
```
Error: Health check timeout
```

**해결 방법**:
1. Deploy Logs에서 에러 확인
2. 환경변수 누락 확인 (특히 `SECRET_KEY`, `DATABASE_URL`)
3. Railway Dashboard에서 환경변수 재확인

#### 데이터베이스 연결 오류
```
django.db.utils.OperationalError: could not connect to server
```

**해결 방법**:
1. `DATABASE_URL`이 올바른지 확인
2. Supabase 연결 문자열이 정확한지 확인
3. Supabase가 정상 작동 중인지 확인

### 프론트엔드 배포 실패

#### API 호출 CORS 에러
```
Access to fetch at 'https://backend.railway.app/api/...' has been blocked by CORS policy
```

**해결 방법**:
1. Railway의 `CORS_ALLOWED_ORIGINS`에 Vercel 도메인이 추가되었는지 확인
2. `https://`를 포함했는지 확인 (http가 아님)
3. 쉼표 구분자에 공백이 없는지 확인

#### 환경변수 적용 안됨
```
VITE_API_URL is undefined
```

**해결 방법**:
1. Vercel Dashboard > Settings > Environment Variables에서 변수 확인
2. 환경변수 추가 후 **반드시 Redeploy** 실행
3. 변수명이 `VITE_` 접두사로 시작하는지 확인

### 인증 오류

#### Supabase 토큰 검증 실패
```
Invalid JWT token
```

**해결 방법**:
1. 백엔드의 `SUPABASE_JWT_SECRET`이 정확한지 확인
2. 프론트엔드의 `VITE_SUPABASE_ANON_KEY`가 정확한지 확인
3. Supabase Dashboard에서 키를 다시 복사하여 확인

---

## 7. 로컬 개발 환경

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/development.txt
cp .env.example .env
# .env 파일 수정 (Supabase 정보 입력)
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
# .env.local 파일 수정 (백엔드 URL 입력)
npm run dev
```

---

## 8. CI/CD (자동 배포)

### Railway
- **main** 브랜치에 push하면 자동 배포
- Pull Request 생성 시 Preview 환경 자동 생성

### Vercel
- **main** 브랜치에 push하면 프로덕션 자동 배포
- Pull Request 생성 시 Preview 배포 자동 생성
- Preview URL에서 변경사항 미리 확인 가능

---

## 9. 모니터링

### Railway
- Dashboard > Deployments: 배포 로그 확인
- Dashboard > Metrics: CPU, 메모리, 네트워크 사용량 확인

### Vercel
- Dashboard > Analytics: 페이지 뷰, 성능 메트릭 확인
- Dashboard > Logs: 함수 로그 확인

### Supabase
- Dashboard > Database: 데이터베이스 상태 확인
- Dashboard > Auth: 사용자 인증 로그 확인

---

## 10. 비용

### Railway
- 무료 티어: $5/월 크레딧
- Hobby Plan: $5/월 (500시간 실행)
- 예상 비용: 백엔드 서비스 1개 - 무료 티어로 충분

### Vercel
- Hobby Plan: 무료
- 대역폭 제한: 100GB/월
- 빌드 시간: 100시간/월
- 예상 비용: 무료 (대부분의 프로젝트에 충분)

### Supabase
- Free Plan: 무료
- 데이터베이스: 500MB
- API 요청: 무제한
- 예상 비용: 무료

**총 예상 비용: $0/월** (무료 티어 사용 시)

---

## 11. 보안 체크리스트

- [ ] `DEBUG=False` 설정 (프로덕션)
- [ ] `SECRET_KEY` 50자 이상의 강력한 랜덤 문자열 사용
- [ ] `ALLOWED_HOSTS` 정확하게 설정
- [ ] `CORS_ALLOWED_ORIGINS` 신뢰할 수 있는 도메인만 추가
- [ ] Supabase JWT Secret 노출 금지 (.env 파일 gitignore)
- [ ] HTTPS 사용 (Railway, Vercel 자동 제공)
- [ ] 환경변수를 코드에 하드코딩하지 않음
- [ ] `.env` 파일을 Git에 커밋하지 않음

---

## 12. 추가 자료

- [Railway 공식 문서](https://docs.railway.app/)
- [Vercel 공식 문서](https://vercel.com/docs)
- [Supabase 공식 문서](https://supabase.com/docs)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)

---

## 문의

배포 중 문제가 발생하면:
1. Deploy Logs 확인
2. 환경변수 설정 재확인
3. 이 문서의 문제 해결 섹션 참조
