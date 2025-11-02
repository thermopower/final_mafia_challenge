@echo off
echo ========================================
echo Vite 개발 서버 실행
echo ========================================
echo.

REM .env 파일 확인
if not exist .env (
    echo ⚠️  .env 파일이 없습니다!
    echo 📝 .env 파일을 생성하고 Supabase 정보를 입력해주세요.
    pause
    exit /b 1
)

REM node_modules 확인
if not exist node_modules (
    echo ⚠️  node_modules가 없습니다!
    echo 먼저 setup_local.bat을 실행해주세요.
    pause
    exit /b 1
)

REM 개발 서버 실행
echo 🚀 Vite 개발 서버를 시작합니다...
echo 👉 http://localhost:5173
echo.
echo 🛑 종료하려면 Ctrl+C를 누르세요.
echo.
npm run dev
