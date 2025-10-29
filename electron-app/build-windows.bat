@echo off
echo ==========================================
echo   GHOST NEWS - Compilador para Windows
echo ==========================================
echo.

echo Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no está instalado
    echo Descarga Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado
    echo Descarga Python desde: https://python.org/
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
npm install

echo.
echo ==========================================
echo Selecciona el tipo de compilación:
echo 1. Instalador Windows (.exe)
echo 2. Versión Portable (.exe)
echo 3. Ambos
echo ==========================================
set /p choice="Ingresa tu opción (1-3): "

if "%choice%"=="1" (
    echo Compilando instalador...
    npm run build-win-installer
) else if "%choice%"=="2" (
    echo Compilando versión portable...
    npm run build-win-portable
) else if "%choice%"=="3" (
    echo Compilando ambas versiones...
    npm run build-win
) else (
    echo Opción inválida
    pause
    exit /b 1
)

echo.
echo ==========================================
echo COMPILACIÓN COMPLETADA!
echo.
echo Los archivos están en la carpeta: dist\
echo ==========================================

echo.
echo Abriendo carpeta de distribución...
start explorer dist

pause
