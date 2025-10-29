# 🪟 GHOST NEWS Desktop App - Windows

## 📦 **Aplicación Desktop Nativa para Windows**

### ✅ **Compilación Windows:**
- **Instalador:** `GHOST NEWS-1.0.0-x64.exe` (~100 MB)
- **Portable:** `GHOST NEWS-1.0.0-portable.exe` (~100 MB)
- **Arquitectura:** Windows 64-bit

### 🚀 **Compilación Automática (GitHub Actions):**
1. Subir código a GitHub
2. GitHub compila automáticamente para Windows
3. Descarga directa de executables

### 💻 **Compilación Manual en Windows:**
```cmd
# Clonar repositorio
git clone https://github.com/TonyDev21/ghostnews.git
cd ghostnews\electron-app

# Método fácil: usar el script
build-windows.bat

# Método manual
npm install
npm run build-win
```

### 🎯 **Características Windows:**
- ✅ Instalador NSIS profesional
- ✅ Accesos directos automáticos
- ✅ Menús nativos de Windows
- ✅ Desinstalador incluido
- ✅ Versión portable (sin instalación)
- ✅ Python incluido automáticamente
- ✅ Servidor web integrado

### 📋 **Archivos generados:**
```
dist/
├── GHOST NEWS-1.0.0-x64.exe           # Instalador
├── GHOST NEWS-1.0.0-portable.exe      # Versión portable
└── win-unpacked/                       # Archivos desempaquetados
```

### 🔧 **Scripts disponibles:**
```bash
npm start                   # Ejecutar en desarrollo
npm run build-win          # Compilar ambas versiones
npm run build-win-installer # Solo instalador
npm run build-win-portable # Solo portable
```

### 📋 **Requisitos del sistema:**
- Windows 10/11 (64-bit)
- 200 MB de espacio libre
- Python se incluye automáticamente

¡Tu **GHOST NEWS** será una aplicación Windows profesional! 🎉
