@echo off
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 goto error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Instalacion terminada. Abre presentar.bat
pause
exit /b 0
:error
echo Revisa que Python 3 este instalado y que tengas conexion a internet.
pause
exit /b 1
