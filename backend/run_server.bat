@echo off
echo ========================================
echo Django 개발 서버 실행
echo ========================================
echo.

REM 가상환경 활성화
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✅ 가상환경 활성화 완료
) else (
    echo ⚠️  가상환경이 없습니다!
    echo 먼저 setup_local.bat을 실행해주세요.
    pause
    exit /b 1
)
echo.

REM .env 파일 확인
if not exist .env (
    echo ⚠️  .env 파일이 없습니다!
    echo 📝 .env 파일을 생성하고 Supabase 정보를 입력해주세요.
    pause
    exit /b 1
)

REM 서버 실행
echo 🚀 Django 서버를 시작합니다...
echo 👉 http://localhost:8000
echo 👉 Admin: http://localhost:8000/admin/
echo 👉 API: http://localhost:8000/api/
echo.
echo 🛑 종료하려면 Ctrl+C를 누르세요.
echo.
python manage.py runserver
