# GHOST NEWS 👻📰

### ✅ Lo que necesitas:
- Windows 10/11
- Python 3.8+ (el instalador te ayudará si no lo tienes)

### 🎯 ¿Qué hace la aplicación?

GHOST NEWS es un analizador de noticias que:
- ✅ Extrae noticias de cualquier sitio web
- ✅ Categoriza automáticamente el contenido  
- ✅ Tiene interfaz moderna y fácil de usar
- ✅ Funciona 100% offline después de instalada
- ✅ Incluye 6 categorías: Tecnología, Deportes, Economía, etc.

### 🔧 Usar la aplicación

1. **Abrir GHOST NEWS** desde el menú de inicio
2. **Ingresar una URL** de cualquier sitio de noticias
3. **Seleccionar categoría** (Tecnología, Deportes, etc.)
4. **¡Ver el análisis automático!**

## Para Desarrolladores

### 🛠️ Tecnologías

- **Backend**: Python 3.12+ con BeautifulSoup4
- **Frontend**: HTML5, CSS3, JavaScript vanilla  
- **Desktop**: Electron 27.0+ para aplicación Windows
- **Build**: electron-builder con NSIS installer

### 📁 Estructura del Proyecto

```
ghostnews/
├── 📄 tecnologiaInovacion.py    # Motor de extracción principal
├── 📄 servidor_web.py           # Servidor HTTP
├── 📄 index.html               # Interfaz web principal
├── 📄 styles.css               # Estilos CSS
├── 📄 build-windows.bat        # Script de compilación
├── 📂 electron-app/            # Aplicación Desktop
│   ├── 📄 main.js             # Proceso principal Electron
│   ├── 📄 package.json        # Configuración Electron
│   ├── 📂 assets/             # Iconos y recursos
│   └── 📂 build/              # Scripts de build
└── 📄 requirements.txt         # Dependencias Python
```

### 🎯 Características Desktop

- ✅ **Instalador NSIS**: Instalación profesional en Windows
- ✅ **Integración Python**: Servidor embebido automático
- ✅ **Icono Personalizado**: Branding completo
- ✅ **Menu de Inicio**: Acceso directo automático

