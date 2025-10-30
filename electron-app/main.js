const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let pythonProcess;

// Configuración de la aplicación
const isDev = process.env.NODE_ENV === 'development';
const serverPort = 8080;

// Archivo de log para debugging
const logFile = path.join(app.getPath('userData'), 'ghost-news.log');

function log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}\n`;
    console.log(message);
    try {
        fs.appendFileSync(logFile, logMessage);
    } catch (err) {
        console.error('Error escribiendo log:', err);
    }
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: true,
            allowRunningInsecureContent: false
        },
        title: 'GHOST NEWS - Analizador de Noticias',
        show: false,
        autoHideMenuBar: true,
        backgroundColor: '#1a1a1a'
    });

    // Configurar eventos de ventana
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.focus();
        startPythonServer();
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
        stopPythonServer();
    });

    // Interceptar enlaces externos
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    // Cargar pantalla de carga inicial
    mainWindow.loadFile(path.join(__dirname, '..', 'index.html'));
}

function startPythonServer() {
    const pythonPath = findPythonExecutable();
    
    // Determinar la ruta del servidor y directorio de trabajo
    let serverScript, workingDir;
    
    if (!isDev && app.isPackaged) {
        // En producción, los archivos están en resources
        serverScript = path.join(process.resourcesPath, 'servidor_web.py');
        workingDir = process.resourcesPath;
    } else {
        // En desarrollo
        serverScript = path.join(__dirname, '..', 'servidor_web.py');
        workingDir = path.join(__dirname, '..');
    }
    
    log('=== Iniciando servidor Python ===');
    log('isDev: ' + isDev);
    log('app.isPackaged: ' + app.isPackaged);
    log('Python executable: ' + pythonPath);
    log('Server script: ' + serverScript);
    log('Working directory: ' + workingDir);
    log('Process resourcesPath: ' + process.resourcesPath);
    log('__dirname: ' + __dirname);
    
    // Verificar que los archivos existan
    if (!fs.existsSync(pythonPath)) {
        log('ERROR: Python executable no encontrado en: ' + pythonPath);
        showErrorDialog('Error', 'No se encontró el ejecutable de Python en: ' + pythonPath);
        return;
    }
    
    if (!fs.existsSync(serverScript)) {
        log('ERROR: servidor_web.py no encontrado en: ' + serverScript);
        showErrorDialog('Error', 'No se encontró servidor_web.py en: ' + serverScript);
        return;
    }
    
    log('Archivos verificados, iniciando proceso...');
    
    // Iniciar proceso Python con -u para unbuffered output
    pythonProcess = spawn(pythonPath, ['-u', serverScript], {
        cwd: workingDir,
        stdio: ['pipe', 'pipe', 'pipe'],
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8', PYTHONUNBUFFERED: '1' }
    });

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString();
        log('Python stdout: ' + output);
        
        // Detectar cuando el servidor está listo
        if (output.includes('Servidor iniciado') || output.includes('Servidor corriendo')) {
            log('Servidor Python listo, cargando interfaz...');
            setTimeout(() => {
                if (mainWindow && !mainWindow.isDestroyed()) {
                    mainWindow.loadURL(`http://localhost:${serverPort}`);
                }
            }, 1500);
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        const error = data.toString();
        log('Python stderr: ' + error);
        
        // Si hay error crítico, mostrar mensaje
        if (error.includes('Error') || error.includes('Exception')) {
            showErrorDialog('Error del servidor Python', error);
        }
    });

    pythonProcess.on('close', (code) => {
        log(`Proceso Python terminado con código ${code}`);
        if (code !== 0 && mainWindow && !mainWindow.isDestroyed()) {
            showErrorDialog('Servidor cerrado', `El servidor Python se cerró inesperadamente (código ${code})`);
        }
    });

    pythonProcess.on('error', (error) => {
        log('Error al iniciar Python: ' + error.message);
        showErrorDialog('Error de Python', 'No se pudo iniciar el servidor Python: ' + error.message);
    });
}

function findPythonExecutable() {
    // En producción, usar el Python embebido incluido en la app
    if (!isDev && app.isPackaged) {
        const embeddedPython = path.join(process.resourcesPath, 'python-embed', 'python.exe');
        log('Usando Python embebido: ' + embeddedPython);
        return embeddedPython;
    }

    // En desarrollo, buscar Python del sistema
    if (isDev) {
        return process.platform === 'win32' ? 'python' : 'python3';
    }

    // Fallback: buscar Python instalado en el sistema
    const possiblePaths = [
        'python',
        'python3',
        'py',
        path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python312', 'python.exe'),
        path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python311', 'python.exe'),
        path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python310', 'python.exe'),
        path.join(process.env.PROGRAMFILES || '', 'Python312', 'python.exe'),
        path.join(process.env.PROGRAMFILES || '', 'Python311', 'python.exe'),
        'C:\\Python312\\python.exe',
        'C:\\Python311\\python.exe'
    ];

    return 'python';
}

function stopPythonServer() {
    if (pythonProcess && !pythonProcess.killed) {
        console.log('🛑 Deteniendo servidor Python...');
        pythonProcess.kill('SIGTERM');
        
        // Forzar cierre después de 5 segundos
        setTimeout(() => {
            if (pythonProcess && !pythonProcess.killed) {
                pythonProcess.kill('SIGKILL');
            }
        }, 5000);
        
        pythonProcess = null;
    }
}

function showErrorDialog(title, message) {
    const { dialog } = require('electron');
    if (mainWindow && !mainWindow.isDestroyed()) {
        dialog.showErrorBox(title, message);
    }
}

// Eventos de la aplicación
app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    stopPythonServer();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', (event) => {
    console.log('🚪 Aplicación cerrándose...');
    stopPythonServer();
});

// Configurar protocolo para URLs personalizadas
app.setAsDefaultProtocolClient('ghost-news');

// Manejo de errores globales
process.on('uncaughtException', (error) => {
    console.error('💥 Error no capturado:', error);
    showErrorDialog('Error de la aplicación', error.message);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Promesa rechazada no manejada:', reason);
});
