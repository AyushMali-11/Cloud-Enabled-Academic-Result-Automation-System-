@echo off
setlocal

echo ================================================
echo Reset PostgreSQL DB and seed sample data
echo ================================================

set PSQL_CMD=psql
if exist "C:\Program Files\PostgreSQL\18\bin\psql.exe" set PSQL_CMD="C:\Program Files\PostgreSQL\18\bin\psql.exe"
if exist "C:\Program Files\PostgreSQL\17\bin\psql.exe" set PSQL_CMD="C:\Program Files\PostgreSQL\17\bin\psql.exe"
if exist "C:\Program Files\PostgreSQL\16\bin\psql.exe" set PSQL_CMD="C:\Program Files\PostgreSQL\16\bin\psql.exe"

if not exist ".env" (
  echo [ERROR] .env file not found.
  echo Copy .env.example to .env and fill DB values first.
  pause
  exit /b 1
)

for /f "tokens=1,* delims==" %%A in (.env) do (
  if "%%A"=="DB_HOST" set DB_HOST=%%B
  if "%%A"=="DB_PORT" set DB_PORT=%%B
  if "%%A"=="DB_USER" set DB_USER=%%B
  if "%%A"=="DB_PASSWORD" set DB_PASSWORD=%%B
)

if "%DB_PORT%"=="" set DB_PORT=5432

set PGPASSWORD=%DB_PASSWORD%

echo.
echo [1/2] Creating database schema...
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d postgres -f database\schema.sql
if errorlevel 1 (
  echo [ERROR] Failed to run schema.sql
  echo Check PostgreSQL service and .env credentials.
  pause
  exit /b 1
)

echo.
echo [2/2] Seeding sample data...
python init_db.py
if errorlevel 1 (
  echo [ERROR] Failed to run init_db.py
  pause
  exit /b 1
)

echo.
echo Done! Start app with: python app.py
pause
