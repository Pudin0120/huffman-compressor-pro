@echo off
REM Huffman Compressor Pro - Setup Script for Windows

setlocal enabledelayedexpansion

echo ===================================================
echo   Huffman Compressor Pro - Setup
echo ===================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no esta instalado
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js no esta instalado
    exit /b 1
)

echo ✅ Python: 
python --version

echo ✅ Node.js: 
node --version

echo ✅ npm: 
npm --version

echo.
echo Configurando Backend...
cd backend

if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -q

cd ..

echo Configurando Frontend...
cd frontend

call npm install -q

cd ..

echo.
echo ===================================================
echo   ✅ Setup Completado
echo ===================================================
echo.
echo Para ejecutar la aplicacion:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --reload
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo Docs API: http://localhost:8000/docs
echo.

pause
