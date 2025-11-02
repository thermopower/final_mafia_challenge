@echo off
echo ========================================
echo 로컬 백엔드 환경 설정 스크립트
echo ========================================
echo.

REM 가상환경 확인 및 생성
if not exist venv (
    echo [1/5] Python 가상환경 생성 중...
    python -m venv venv
    echo 가상환경 생성 완료!
) else (
    echo [1/5] 가상환경이 이미 존재합니다.
)
echo.

REM 가상환경 활성화
echo [2/5] 가상환경 활성화 중...
call venv\Scripts\activate.bat
echo.

REM 의존성 설치
echo [3/5] Python 패키지 설치 중 (시간이 걸릴 수 있습니다)...
pip install --upgrade pip
pip install -r requirements\development.txt
echo 패키지 설치 완료!
echo.

REM 환경 변수 확인
echo [4/5] 환경 변수 확인 중...
if not exist .env (
    echo ⚠️  .env 파일이 없습니다!
    echo 📝 .env 파일을 생성하고 Supabase 정보를 입력해주세요.
    echo 👉 .env.example 파일을 참고하세요.
    pause
) else (
    echo ✅ .env 파일이 존재합니다.
)
echo.

REM 마이그레이션
echo [5/5] 데이터베이스 마이그레이션 실행 중...
python manage.py makemigrations
python manage.py migrate
echo 마이그레이션 완료!
echo.

echo ========================================
echo 🎉 백엔드 설정이 완료되었습니다!
echo ========================================
echo.
echo 다음 명령어로 서버를 실행하세요:
echo     python manage.py runserver
echo.
echo 서버 주소: http://localhost:8000
echo Admin: http://localhost:8000/admin/
echo API: http://localhost:8000/api/
echo.
pause
