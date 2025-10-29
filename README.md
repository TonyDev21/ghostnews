# GHOST NEWS 👻📰

## ¿Cómo instalar GHOST NEWS en tu computadora Windows?

### 🎯 PARA USUARIOS: Descarga el .exe listo

**✅ OPCIÓN MÁS FÁCIL:** 

1. **Ve a la página de releases:** https://github.com/TonyDev21/ghostnews/releases
2. **Descarga** el archivo `GHOST NEWS Setup.exe` 
3. **Ejecuta** el instalador descargado
4. **¡Listo!** Ya tienes GHOST NEWS instalado

### 📋 Opción 2: Compilar desde el código fuente

**Solo si quieres compilar tú mismo:**

#### Prerrequisitos
- Windows 10/11
- Python 3.8 o superior  
- Node.js 16 o superior

#### Pasos de compilación:

1. **Descargar el proyecto**
   ```bash
   git clone https://github.com/TonyDev21/ghostnews.git
   cd ghostnews
   ```

2. **Instalar dependencias Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Compilar la aplicación Windows**
   ```bash
   cd electron-app
   npm install
   npm run build-win
   ```

4. **Encontrar el .exe**
   - Ve a la carpeta `electron-app/dist/`
   - Ejecuta el instalador `.exe` generado

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

### ❓ Solución de problemas

**Error: "Python no encontrado"**
- Instalar Python desde https://python.org
- Marcar "Add to PATH" durante instalación

**Error: "Node.js no encontrado"**  
- Instalar Node.js desde https://nodejs.org

**No se genera el .exe**
- Verificar que tienes permisos de administrador
- Ejecutar `build-windows.bat` como administrador

### 📞 Soporte

¿Problemas? Contacta a **TonyDev21** o abre un issue en GitHub.

---

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
- ✅ **Aplicación Portable**: Ejecutable sin instalación  
- ✅ **Integración Python**: Servidor embebido automático
- ✅ **Icono Personalizado**: Branding completo
- ✅ **Menu de Inicio**: Acceso directo automático

### 👨‍💻 Autor

**TonyDev21** - [GitHub](https://github.com/TonyDev21)
