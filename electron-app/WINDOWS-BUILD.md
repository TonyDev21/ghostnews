# 🪟 GHOST NEWS - Windows Desktop App

## 📦 **Aplicación Desktop para Windows**

### 🚀 **Cómo compilar para Windows:**

#### **Método 1: En máquina Windows**
```cmd
# Clonar el repositorio
git clone https://github.com/TonyDev21/ghostnews.git
cd ghostnews\electron-app

# Instalar dependencias
npm install

# Compilar para Windows
npm run build-win

# O compilar versión portable
npm run build-win-portable
```

#### **Método 2: Usando GitHub Actions (Recomendado)**
1. Subir este código a GitHub
2. Configurar GitHub Actions
3. Compilación automática para Windows en la nube

### 📋 **Archivos que se generarán:**
- `GHOST NEWS-1.0.0-x64.exe` - Instalador Windows
- `GHOST NEWS-1.0.0-portable.exe` - Versión portable

### ✅ **Características Windows:**
- ✅ Instalador NSIS profesional
- ✅ Accesos directos en Escritorio y Menú Inicio
- ✅ Integración completa con Windows
- ✅ Desinstalador incluido
- ✅ Versión portable (sin instalación)

### 🎯 **Requisitos del sistema:**
- Windows 10/11 (64-bit)
- Python 3.8+ (se incluye automáticamente)
- 200 MB de espacio libre

### 📁 **Estructura de la App:**
```
GHOST NEWS/
├── GHOST NEWS.exe          # Ejecutable principal
├── resources/              # Recursos de la app
│   ├── app.asar           # Código empaquetado
│   └── python/            # Backend Python integrado
├── locales/               # Idiomas
└── [archivos de Electron]
```

### 🔧 **Scripts de desarrollo:**
```bash
npm start                   # Ejecutar en modo desarrollo
npm run build-win          # Compilar instalador
npm run build-win-portable # Compilar versión portable
npm run pack               # Solo empaquetar (sin instalador)
```

### 🎉 **Resultado final:**
- App desktop nativa de Windows
- Sin necesidad de navegador
- Instalación profesional
- Funciona offline
- Menús nativos de Windows

¡Tu **GHOST NEWS** será una aplicación Windows completa! 💼
