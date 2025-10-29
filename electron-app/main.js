const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

// Configuración de la aplicación
const isDev = process.env.NODE_ENV === 'development';
const serverPort = 8080;

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
    const serverScript = path.join(__dirname, '..', 'servidor_web.py');
    
    console.log('🐍 Iniciando servidor Python...');
    console.log('Python executable:', pythonPath);
    console.log('Server script:', serverScript);
    
    // Iniciar proceso Python
    pythonProcess = spawn(pythonPath, [serverScript], {
        cwd: path.join(__dirname, '..'),
        stdio: ['pipe', 'pipe', 'pipe'],
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' }
    });

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString();
        console.log('📡 Python stdout:', output);
        
        // Detectar cuando el servidor está listo
        if (output.includes('Servidor iniciado') || output.includes('serving at')) {
            console.log('✅ Servidor Python listo');
            setTimeout(() => {
                if (mainWindow && !mainWindow.isDestroyed()) {
                    mainWindow.loadURL(`http://localhost:${serverPort}`);
                }
            }, 1500);
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        const error = data.toString();
        console.error('❌ Python stderr:', error);
        
        // Si hay error crítico, mostrar mensaje
        if (error.includes('Error') || error.includes('Exception')) {
            showErrorDialog('Error del servidor Python', error);
        }
    });

    pythonProcess.on('close', (code) => {
        console.log(`🔴 Proceso Python terminado con código ${code}`);
        if (code !== 0 && mainWindow && !mainWindow.isDestroyed()) {
            showErrorDialog('Servidor cerrado', `El servidor Python se cerró inesperadamente (código ${code})`);
        }
    });

    pythonProcess.on('error', (error) => {
        console.error('💥 Error al iniciar Python:', error);
        showErrorDialog('Error de Python', 'No se pudo iniciar el servidor Python. Asegúrate de que Python esté instalado.');
    });
}

function findPythonExecutable() {
    // Posibles rutas de Python en Windows
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

    // En desarrollo usar python del sistema
    if (isDev) {
        return process.platform === 'win32' ? 'python' : 'python3';
    }

    // En producción, buscar Python instalado
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
