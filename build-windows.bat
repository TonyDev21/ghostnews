@echo off
echo ====================================
echo   GHOST NEWS - Compilador Windows
echo ====================================
echo.

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no está instalado
    echo Descarga Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado
    echo Descarga Python desde: https://python.org/
    pause
    exit /b 1
)

cd /d "%~dp0electron-app"

echo Instalando dependencias de Node.js...
call npm install

echo.
echo Selecciona el tipo de build:
echo 1. Instalador NSIS (.exe)
echo 2. Aplicación portable (.exe)
echo 3. Ambos
echo.
set /p choice="Ingresa tu opción (1-3): "

if "%choice%"=="1" goto nsis
if "%choice%"=="2" goto portable
if "%choice%"=="3" goto both
echo Opción inválida
pause
exit /b 1

:nsis
echo.
echo Compilando instalador NSIS...
call npm run build -- --win nsis --x64
goto end

:portable
echo.
echo Compilando aplicación portable...
call npm run build -- --win portable --x64
goto end

:both
echo.
echo Compilando ambas versiones...
call npm run build -- --win --x64
goto end

:end
echo.
echo ====================================
echo   Compilación completada!
echo ====================================
echo Los archivos están en: electron-app\dist\
explorer "dist"
pause
