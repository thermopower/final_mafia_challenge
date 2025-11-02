@echo off
echo ========================================
echo 로컬 프론트엔드 환경 설정 스크립트
echo ========================================
echo.

REM Node.js 확인
echo [1/3] Node.js 버전 확인 중...
node --version
if errorlevel 1 (
    echo ⚠️  Node.js가 설치되어 있지 않습니다!
    echo 👉 https://nodejs.org/ 에서 Node.js를 설치해주세요.
    pause
    exit /b 1
)
npm --version
echo Node.js 설치 확인 완료!
echo.

REM 환경 변수 확인
echo [2/3] 환경 변수 확인 중...
if not exist .env (
    echo ⚠️  .env 파일이 없습니다!
    echo 📝 .env 파일을 생성하고 Supabase 정보를 입력해주세요.
    echo 👉 .env.example 파일을 참고하세요.
    pause
) else (
    echo ✅ .env 파일이 존재합니다.
)
echo.

REM 의존성 설치
echo [3/3] npm 패키지 설치 중 (시간이 걸릴 수 있습니다)...
npm install
echo 패키지 설치 완료!
echo.

echo ========================================
echo 🎉 프론트엔드 설정이 완료되었습니다!
echo ========================================
echo.
echo 다음 명령어로 개발 서버를 실행하세요:
echo     npm run dev
echo.
echo 서버 주소: http://localhost:5173
echo.
pause
