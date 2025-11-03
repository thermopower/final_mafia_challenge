# 🎓 대학교 데이터 시각화 대시보드

Django REST Framework + React + Supabase를 활용한 종합 데이터 시각화 대시보드 프로젝트

---

## 📖 프로젝트 개요

이 프로젝트는 대학교 내 다양한 데이터(연구 실적, 예산, 학생 정보 등)를 수집, 관리, 시각화하는 웹 애플리케이션입니다.

### 주요 기능

- 📊 **실시간 대시보드**: 다양한 차트와 메트릭을 통한 데이터 시각화
- 📁 **엑셀 파일 업로드**: 대량 데이터 일괄 업로드
- 🔐 **사용자 인증**: Supabase Auth 기반 안전한 로그인
- 📈 **데이터 분석**: 연구 실적, 예산 집행, 학생 통계 등 분석
- 🎨 **반응형 UI**: Material-UI 기반 모던 인터페이스

---

## 🏗️ 기술 스택

### Backend
- **Framework**: Django 5.x + Django REST Framework
- **Language**: Python 3.11+
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Supabase Auth (JWT)
- **Deployment**: Railway

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts
- **Deployment**: Vercel

### Infrastructure
- **Database & Auth**: Supabase
- **CI/CD**: GitHub Actions
- **Hosting**: Railway (Backend) + Vercel (Frontend)

---

## 🚀 빠른 시작

### 전제 조건
- Python 3.11+
- Node.js 18+
- Supabase 계정

### 1. Supabase 설정
1. [Supabase](https://supabase.com/)에서 새 프로젝트 생성
2. 프로젝트 URL, Anon Key, JWT Secret 확인

### 2. 백엔드 설정

```bash
# Windows
cd backend
setup_local.bat
run_server.bat

# Mac/Linux
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver
```

### 3. 프론트엔드 설정

```bash
# Windows
cd frontend
setup_local.bat
run_dev.bat

# Mac/Linux
cd frontend
npm install
npm run dev
```

### 4. 접속

- **프론트엔드**: http://localhost:5173
- **백엔드 API**: http://localhost:8000/api/
- **관리자 페이지**: http://localhost:8000/admin/

---

## 📚 문서

- **[QUICKSTART.md](./QUICKSTART.md)** - 5분 안에 시작하기
- **[LOCAL_SETUP.md](./LOCAL_SETUP.md)** - 상세한 로컬 개발 환경 설정
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - 프로덕션 배포 가이드
- **[CLAUDE.md](./CLAUDE.md)** - 프로젝트 아키텍처 및 설계 원칙
- **[docs/](./docs/)** - 설계 문서 및 API 스펙

---

## 🏛️ 아키텍처

### Backend (Layered Architecture)

```
Presentation Layer (API Views)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Data Access)
        ↓
Persistence Layer (ORM Models)
```

### Frontend (Component-based Architecture)

```
Pages (Routes)
  ↓
Components (UI)
  ↓
Hooks (State & Logic)
  ↓
Services (API)
```

### SOLID 원칙 준수
- **Single Responsibility**: 각 레이어는 단일 책임
- **Open/Closed**: 확장에는 열려있고 수정에는 닫혀있음
- **Liskov Substitution**: Repository 교체 가능
- **Interface Segregation**: 필요한 메서드만 노출
- **Dependency Inversion**: 추상화에 의존

자세한 내용은 [CLAUDE.md](./CLAUDE.md)를 참고하세요.

---

## 📁 프로젝트 구조

```
final_mafia_challenge/
├── backend/                    # Django 백엔드
│   ├── config/                 # Django 프로젝트 설정
│   ├── apps/                   # Django 앱들
│   │   ├── dashboard/          # 대시보드 기능
│   │   ├── uploads/            # 파일 업로드 기능
│   │   └── accounts/           # 사용자 계정 기능
│   ├── infrastructure/         # 인프라 레이어
│   ├── requirements/           # Python 의존성
│   └── manage.py               # Django 관리 스크립트
│
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── presentation/       # UI 컴포넌트
│   │   ├── application/        # Hooks & Context
│   │   ├── domain/             # 도메인 모델
│   │   ├── services/           # API 서비스
│   │   └── infrastructure/     # 인프라 설정
│   ├── public/                 # 정적 파일
│   └── package.json            # npm 의존성
│
├── docs/                       # 설계 문서
│   ├── architecture/           # 아키텍처 문서
│   ├── userflow/              # 사용자 플로우
│   ├── usecases/              # 유스케이스
│   └── dataflow/              # 데이터 플로우
│
├── QUICKSTART.md              # 빠른 시작 가이드
├── LOCAL_SETUP.md             # 로컬 설정 가이드
├── DEPLOYMENT.md              # 배포 가이드
└── CLAUDE.md                  # 아키텍처 문서
```

---

## 🧪 테스트

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

## 🚢 배포 (Hybrid Deployment)

이 프로젝트는 **하이브리드 배포** 방식을 사용합니다:
- **백엔드**: Railway (Django REST API)
- **프론트엔드**: Vercel (React SPA)
- **데이터베이스**: Supabase (PostgreSQL)

### 배포 순서

#### 1. 백엔드 배포 (Railway)
```bash
# Railway Dashboard에서:
1. New Project 생성
2. Root Directory를 `/backend`로 설정
3. 환경변수 설정 (SECRET_KEY, DATABASE_URL, CORS_ALLOWED_ORIGINS)
4. 자동 배포 완료
```

#### 2. 프론트엔드 배포 (Vercel)
```bash
# Vercel Dashboard에서:
1. New Project 생성
2. Root Directory를 `frontend`로 설정
3. 환경변수 설정 (VITE_API_URL, VITE_SUPABASE_URL)
4. 자동 배포 완료
```

#### 3. CORS 설정
```bash
# Railway Variables에서:
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
```

자세한 내용은 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참고하세요.

---

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

---

## 👥 팀

- **Backend Developer**: Django + DRF + Supabase
- **Frontend Developer**: React + TypeScript + MUI
- **DevOps**: Railway + Vercel

---

## 📧 연락처

프로젝트에 대한 질문이나 제안사항이 있으시면 Issues를 생성해주세요.

---

## 🙏 감사의 말

- [Django](https://www.djangoproject.com/)
- [React](https://react.dev/)
- [Supabase](https://supabase.com/)
- [Railway](https://railway.app/)
- [Vercel](https://vercel.com/)

---

**Happy Coding! 🎉**
