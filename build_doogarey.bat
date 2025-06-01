@echo off
REM Build script for Doogarey Agent Zero on Windows

echo 🚀 Building Doogarey Agent Zero Docker Image
echo =============================================

REM Set variables
set IMAGE_NAME=agent-zero-doogarey
set TAG=%1
if "%TAG%"=="" set TAG=latest

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do if not "%%I"=="" set datetime=%%I
set CACHE_DATE=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%:%datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%

echo 📦 Building image: %IMAGE_NAME%:%TAG%
echo 🕒 Cache date: %CACHE_DATE%

REM Build the Docker image
docker build ^
  -f Dockerfile.doogarey ^
  -t "%IMAGE_NAME%:%TAG%" ^
  --build-arg BRANCH=local ^
  --build-arg CACHE_DATE="%CACHE_DATE%" ^
  .

if %ERRORLEVEL% EQU 0 (
  echo ✅ Build completed successfully!
  echo 🏷️  Image: %IMAGE_NAME%:%TAG%
  echo.
  echo To run the container:
  echo docker run -d -p 50001:80 --name agent-zero-doogarey %IMAGE_NAME%:%TAG%
  echo.
  echo To push to a registry:
  echo docker tag %IMAGE_NAME%:%TAG% your-registry.com/%IMAGE_NAME%:%TAG%
  echo docker push your-registry.com/%IMAGE_NAME%:%TAG%
) else (
  echo ❌ Build failed!
  exit /b 1
)