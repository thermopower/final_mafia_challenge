# 로컬 환경 구동 가이드

## ✅ 사전 요구사항

- **Python 3.13+** (현재 설치된 버전: 3.13.2)
- **Node.js 18+** (프론트엔드용)
- **Git**

## 🚀 백엔드 구동 방법

### 1. 백엔드 디렉토리로 이동

```bash
cd backend
```

### 2. 가상환경 활성화

**Windows PowerShell:**
```powershell
.\venv\Scripts\activate
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. 환경 변수 확인

`.env` 파일이 `backend/` 디렉토리에 있는지 확인하세요. 파일이 없다면 `.env.example`을 복사하여 생성하세요.

```bash
# .env 파일 생성 (Windows)
copy .env.example .env

# .env 파일 생성 (Linux/Mac)
cp .env.example .env
```

### 4. 데이터베이스 마이그레이션 확인

```bash
python manage.py showmigrations
```

모든 마이그레이션이 `[X]`로 표시되어 있으면 정상입니다.

### 5. Django 개발 서버 실행

```bash
python manage.py runserver
```

서버가 정상적으로 시작되면 다음과 같은 메시지가 표시됩니다:

```
Watching for file changes with StatReloader
Django version 5.0.1, using settings 'config.settings.development'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🌐 접속 가능한 엔드포인트

서버가 실행되면 다음 URL들을 브라우저에서 확인할 수 있습니다:

### 주요 엔드포인트

| 엔드포인트 | URL | 설명 |
|----------|-----|------|
| **Health Check** | http://127.0.0.1:8000/api/health/ | 서버 상태 확인 |
| **API 문서** | http://127.0.0.1:8000/api/docs/ | Swagger UI 기반 API 문서 |
| **API 스키마** | http://127.0.0.1:8000/api/schema/ | OpenAPI 스키마 (YAML) |
| **관리자 페이지** | http://127.0.0.1:8000/admin/ | Django 관리자 인터페이스 |

### API 엔드포인트

| 엔드포인트 | URL | 설명 |
|----------|-----|------|
| **파일 업로드** | http://127.0.0.1:8000/api/uploads/ | CSV 파일 업로드 |

## 📝 테스트 방법

### 1. Health Check 테스트

```bash
curl http://127.0.0.1:8000/api/health/
```

**예상 응답:**
```json
{"status": "healthy", "service": "university-dashboard-api"}
```

### 2. API 스키마 확인

```bash
curl http://127.0.0.1:8000/api/schema/
```

### 3. Swagger UI에서 API 테스트

브라우저에서 http://127.0.0.1:8000/api/docs/ 를 열어 Swagger UI를 통해 모든 API를 테스트할 수 있습니다.

## 🔧 문제 해결

### 문제 1: 포트가 이미 사용 중

**오류 메시지:**
```
Error: That port is already in use.
```

**해결 방법:**
다른 포트로 서버를 실행하세요:
```bash
python manage.py runserver 8001
```

### 문제 2: 모듈을 찾을 수 없음

**오류 메시지:**
```
ModuleNotFoundError: No module named 'xxx'
```

**해결 방법:**
의존성을 다시 설치하세요:
```bash
pip install -r requirements/development.txt
```

### 문제 3: 데이터베이스 연결 오류

**오류 메시지:**
```
django.db.utils.OperationalError: could not connect to server
```

**해결 방법:**
1. `.env` 파일의 데이터베이스 설정을 확인하세요
2. Supabase 연결 정보가 올바른지 확인하세요
3. 인터넷 연결을 확인하세요

### 문제 4: Python 프로세스가 종료되지 않음

**해결 방법 (Windows):**
```bash
taskkill /F /IM python.exe
```

**해결 방법 (Linux/Mac):**
```bash
pkill -9 python
```

## 📦 프론트엔드 구동 방법 (선택 사항)

프론트엔드를 함께 실행하려면:

### 1. 프론트엔드 디렉토리로 이동

```bash
cd frontend
```

### 2. 의존성 설치

```bash
npm install
```

### 3. 개발 서버 실행

```bash
npm run dev
```

프론트엔드는 기본적으로 http://localhost:5173 에서 실행됩니다.

## 🛠️ 개발 환경 설정

### VS Code 권장 확장 프로그램

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **Django** (Baptiste Darthenay)
- **REST Client** (Huachao Mao)

### 코드 포맷팅

```bash
# Black으로 코드 포맷팅
black .

# isort로 import 정렬
isort .

# Flake8로 코드 검사
flake8 .
```

## 📚 추가 리소스

- **프로젝트 구조**: `CLAUDE.md` 참조
- **API 문서**: `docs/` 디렉토리 참조
- **배포 가이드**: `DEPLOYMENT.md` 참조

## 🎯 다음 단계

1. ✅ 백엔드 서버 구동 완료
2. ⏭️ 프론트엔드 개발 서버 구동
3. ⏭️ API 엔드포인트 테스트
4. ⏭️ 데이터베이스 시딩 (필요시)

---

**문제가 발생하면 이슈를 생성하거나 팀에 문의하세요!** 🚀
