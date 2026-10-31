@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
echo Ejecuta primero instalar.bat
pause
exit /b 1
)
.venv\Scripts\python.exe clase.py presentar
if errorlevel 1 pause
