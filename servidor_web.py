#!/usr/bin/env python3
"""
GHOST NEWS - Servidor Web
Servidor web simple que maneja las solicitudes de extracción de noticias
"""

import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import sys

# Importar nuestro extractor de noticias
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tecnologiaInovacion import extraer_noticias_web

class NewsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Maneja solicitudes GET - sirve archivos estáticos"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif self.path == '/styles.css':
            self.serve_file('styles.css', 'text/css')
        elif self.path == '/noticias_generadas.html':
            self.serve_file('noticias_generadas.html', 'text/html')
        else:
            self.send_error(404, "Archivo no encontrado")

    def do_POST(self):
        """Maneja solicitudes POST - procesa URLs de noticias"""
        if self.path == '/api/extract-news':
            self.extract_news()
        else:
            self.send_error(404, "Endpoint no encontrado")

    def serve_file(self, filename, content_type):
        """Sirve un archivo estático"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type + '; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, f"Archivo {filename} no encontrado")

    def extract_news(self):
        """Extrae noticias de la URL proporcionada"""
        try:
            print("Recibida solicitud POST para extraer noticias")
            
            # Leer datos del POST
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url', '')
            print(f"URL recibida: {url}")
            
            if not url:
                print("ERROR: URL vacia")
                self.send_json_error(400, "URL requerida")
                return

            print(f"Procesando URL: {url}")
            
            # Extraer noticias usando nuestro sistema
            noticias = extraer_noticias_web(url)
            
            if not noticias:
                print("ERROR: No se encontraron noticias")
                self.send_json_error(404, "No se encontraron noticias en la URL")
                return

            # Convertir a formato para el frontend
            noticias_list = []
            for key, noticia in noticias.items():
                noticias_list.append({
                    'titulo': noticia['titulo'],
                    'resumen': noticia['resumen'],
                    'enlace': noticia['enlace'],
                    'imagen': noticia.get('imagen', '')
                })

            # Enviar respuesta exitosa
            response = {
                'success': True,
                'count': len(noticias_list),
                'noticias': noticias_list
            }
            
            self.send_json_response(200, response)
            print(f"OK: Enviadas {len(noticias_list)} noticias al frontend")

        except json.JSONDecodeError as e:
            print(f"ERROR JSON: {e}")
            self.send_json_error(400, "JSON inválido")
        except Exception as e:
            print(f"ERROR procesando noticias: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_error(500, f"Error del servidor: {str(e)}")

    def send_json_response(self, status_code, data):
        """Envía una respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(json_data.encode('utf-8'))

    def send_json_error(self, status_code, message):
        """Envía un error en formato JSON"""
        error_data = {
            'success': False,
            'error': message
        }
        self.send_json_response(status_code, error_data)

    def do_OPTIONS(self):
        """Maneja preflight requests para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8080):
    """Ejecuta el servidor web"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, NewsHandler)
    
    print("="*50)
    print(f"GHOST NEWS - Servidor Web Iniciado")
    print("="*50)
    print(f"Servidor corriendo en: http://localhost:{port}")
    print(f"Accede desde tu navegador a: http://localhost:{port}")
    print("="*50)
    print("Endpoints disponibles:")
    print("   GET  /                    - Pagina principal")
    print("   GET  /index.html          - Pagina principal")
    print("   POST /api/extract-news    - Extraer noticias")
    print("="*50)
    print("Presiona Ctrl+C para detener el servidor")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
        httpd.server_close()

if __name__ == '__main__':
    # Cambiar al directorio del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar que existe el archivo principal
    if not os.path.exists('tecnologiaInovacion.py'):
        print("ERROR: No se encuentra tecnologiaInovacion.py")
        print("   Asegurate de ejecutar este servidor desde el directorio del proyecto")
        sys.exit(1)
    
    # Iniciar servidor
    run_server()
