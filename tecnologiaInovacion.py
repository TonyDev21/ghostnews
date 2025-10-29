#!/usr/bin/env python3
"""
GHOST NEWS - Web Scraping Flexible
Extractor de noticias que funciona con cualquier sitio web de noticias
Refactorizado: Solo usa urllib (estándar) + BeautifulSoup
"""

import urllib.request
import urllib.parse
import csv
import re
from datetime import datetime
from bs4 import BeautifulSoup

# CONFIGURACIÓN GLOBAL
CONFIGURACION = {
    'url_noticias': 'https://tec.com.pe',
    'max_noticias': 20,
    'timeout_segundos': 30,
    'user_agent': 'Mozilla/5.0 (Linux; Ubuntu) AppleWebKit/537.36 GHOST-NEWS/1.0',
    'archivo_html': 'noticias_generadas.html',
    'archivo_csv': 'noticias.csv'
}

# SELECTORES COMUNES PARA DIFERENTES SITIOS
SELECTORES_COMUNES = {
    'articulos': [
        '.elementor-post',  # tec.com.pe
        'article', '.article', '.post', '.story', '.news-item',
        '[data-testid="edinburgh-article"]',  # BBC
        '.media', '.gs-c-promo',  # BBC alternativo
        '.container__item', '.cd__content',  # CNN
        '.story-item', '.flex-module',  # El Comercio
        '.card', '.item', '.entry', '.content-item',
        '[class*="article"]', '[class*="post"]', '[class*="story"]',
        '[class*="news"]', '[class*="item"]',
        'div:has(h2)', 'div:has(h3)', 'section:has(h2)'
    ],
    'titulos': [
        '.elementor-post__title a', 'h1', 'h2', 'h3', 'h4',
        '.title', '.headline', '.media__title',
        '.gs-c-promo-heading__title', '[data-testid="card-headline"]',
        '.cd__headline', '.story-item__title', '.card__title',
        '[class*="title"]', '[class*="headline"]', 'a'
    ],
    'resumenes': [
        '.elementor-post__excerpt p', 'p', '.summary', '.excerpt',
        '.description', '.media__summary', '.gs-c-promo-summary',
        '.cd__description', '.story-item__summary', '.card__summary',
        '[class*="summary"]', '[class*="excerpt"]', '.lead'
    ],
    'imagenes': [
        '.elementor-post__thumbnail img', 'img', '.image img',
        '.photo img', '.media img', '.media__image img',
        '.gs-c-promo-image img', '.cd__image img',
        '.story-item__image img', '.card__media img'
    ]
}

def solicitar_url():
    """Solicita al usuario la URL a analizar"""
    print("🌐 GHOST NEWS - Analizador de Noticias Flexible")
    print("="*60)
    print("Puedes analizar cualquier sitio web de noticias\n")
    
    print("📋 Opciones:")
    print("1. Presiona ENTER para usar la URL por defecto (tec.com.pe)")
    print("2. Ingresa cualquier URL de noticias\n")
    
    print("💡 Ejemplos de URLs que funcionan bien:")
    print("   - https://tec.com.pe")
    print("   - https://www.bbc.com/mundo")
    print("   - https://cnnespanol.cnn.com")
    print("   - https://www.elcomercio.pe")
    print()
    
    url = input("🔗 Ingresa la URL (o ENTER para default): ").strip()
    
    if not url:
        url = CONFIGURACION['url_noticias']
        print(f"✅ Usando URL por defecto: {url}")
    else:
        # Asegurar que tenga protocolo
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        print(f"✅ Usando URL personalizada: {url}")
    
    return url

def obtener_contenido_web(url):
    """Obtiene el contenido HTML de una página web"""
    print(f"🌐 Navegando a: {url}")
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', CONFIGURACION['user_agent'])
        
        with urllib.request.urlopen(req, timeout=CONFIGURACION['timeout_segundos']) as response:
            contenido = response.read().decode('utf-8')
            print("✅ Contenido web obtenido exitosamente")
            return contenido
            
    except Exception as error:
        print(f"❌ Error obteniendo contenido web: {error}")
        return None

def detectar_selectores_inteligente(soup, url):
    """Detecta automáticamente los mejores selectores según el sitio"""
    print("🔍 Detectando estructura del sitio web...")
    
    # Detectores específicos por sitio
    if 'tec.com.pe' in url:
        articulos = soup.select('.elementor-post')
        if articulos:
            print(f"✅ Sitio reconocido: TEC.COM.PE - {len(articulos)} artículos")
            return articulos, 'tec.com.pe específico'
    
    elif 'bbc.com' in url:
        # Múltiples selectores para BBC
        for selector in ['[data-testid="edinburgh-article"]', '.media', '.gs-c-promo', 'article']:
            articulos = soup.select(selector)
            if len(articulos) >= 3:
                print(f"✅ Sitio reconocido: BBC - {len(articulos)} artículos con {selector}")
                return articulos, f'BBC {selector}'
    
    elif 'cnn' in url.lower():
        for selector in ['.container__item', '.cd__content', 'article', '.card']:
            articulos = soup.select(selector)
            if len(articulos) >= 3:
                print(f"✅ Sitio reconocido: CNN - {len(articulos)} artículos")
                return articulos, f'CNN {selector}'
    
    # Detección genérica inteligente
    print("🔍 Aplicando detección genérica...")
    for selector in SELECTORES_COMUNES['articulos']:
        articulos = soup.select(selector)
        if len(articulos) >= 3:
            print(f"✅ Selector efectivo: {selector} - {len(articulos)} elementos")
            return articulos, f'genérico: {selector}'
    
    # Último recurso: buscar elementos con títulos
    print("⚠️ Usando detección de último recurso...")
    elementos_con_titulos = []
    for elemento in soup.find_all(['div', 'section', 'article']):
        # Buscar si tiene algún título
        titulo = elemento.find(['h1', 'h2', 'h3', 'h4', 'a'])
        if titulo and len(titulo.get_text(strip=True)) > 10:
            elementos_con_titulos.append(elemento)
            if len(elementos_con_titulos) >= 20:
                break
    
    if elementos_con_titulos:
        print(f"✅ Detección de último recurso: {len(elementos_con_titulos)} elementos")
        return elementos_con_titulos, 'último recurso'
    
    print("❌ No se pudieron detectar artículos")
    return [], 'sin detección'

def extraer_datos_articulo_flexible(articulo, url_base):
    """Extrae datos de un artículo usando múltiples estrategias"""
    try:
        # TÍTULO - Buscar con múltiples estrategias
        titulo = ""
        enlace = ""
        
        # Estrategia 1: Selectores específicos
        for selector in SELECTORES_COMUNES['titulos']:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text(strip=True)
                if len(texto) > 10:  # Título válido
                    titulo = texto
                    enlace = elemento.get('href', '') if elemento.name == 'a' else ''
                    break
        
        # Estrategia 2: Buscar primer enlace con texto significativo
        if not titulo:
            enlace_elem = articulo.find('a')
            if enlace_elem:
                texto = enlace_elem.get_text(strip=True)
                if len(texto) > 10:
                    titulo = texto
                    enlace = enlace_elem.get('href', '')
        
        # Estrategia 3: Cualquier texto largo
        if not titulo:
            for texto_elem in articulo.find_all(text=True):
                texto = texto_elem.strip()
                if len(texto) > 15 and not texto.startswith(('Ver', 'Leer', 'Más')):
                    titulo = texto[:200]
                    break
        
        if not titulo or len(titulo) < 10:
            return None
        
        # ENLACE - Asegurar URL completa
        if enlace and not enlace.startswith('http'):
            enlace = urllib.parse.urljoin(url_base, enlace)
        
        # RESUMEN - Múltiples estrategias
        resumen = "Resumen no disponible"
        for selector in SELECTORES_COMUNES['resumenes']:
            elem_resumen = articulo.select_one(selector)
            if elem_resumen:
                texto_resumen = elem_resumen.get_text(strip=True)
                if len(texto_resumen) > 20 and texto_resumen.lower() != titulo.lower():
                    resumen = texto_resumen[:300] + "..." if len(texto_resumen) > 300 else texto_resumen
                    break
        
        # IMAGEN - Buscar imagen
        imagen_url = ""
        for selector in SELECTORES_COMUNES['imagenes']:
            img_elem = articulo.select_one(selector)
            if img_elem:
                imagen_url = (img_elem.get('data-src') or 
                             img_elem.get('src') or 
                             img_elem.get('data-lazy-src') or "")
                if imagen_url:
                    if not imagen_url.startswith('http'):
                        imagen_url = urllib.parse.urljoin(url_base, imagen_url)
                    break
        
        return {
            "titulo": titulo,
            "resumen": resumen,
            "imagen": imagen_url,
            "enlace": enlace or url_base
        }
        
    except Exception as error:
        print(f"⚠️ Error procesando artículo: {error}")
        return None

def extraer_noticias_web(url):
    """Función principal de extracción de noticias"""
    print("🔍 Iniciando extracción de noticias...")
    
    # 1. Obtener contenido
    contenido_html = obtener_contenido_web(url)
    if not contenido_html:
        return {}
    
    # 2. Parsear HTML
    print("Analizando contenido HTML...")
    soup = BeautifulSoup(contenido_html, 'html.parser')
    
    # 3. Detectar estructura
    articulos, metodo_deteccion = detectar_selectores_inteligente(soup, url)
    
    if not articulos:
        print("❌ No se encontraron artículos en la página")
        return {}
    
    print(f"📰 Procesando {min(len(articulos), CONFIGURACION['max_noticias'])} artículos...")
    
    # 4. Extraer datos
    noticias = {}
    contador = 1
    titulos_vistos = set()
    
    for articulo in articulos:
        if contador > CONFIGURACION['max_noticias']:
            break
        
        datos = extraer_datos_articulo_flexible(articulo, url)
        
        if datos and datos["titulo"]:
            # Evitar duplicados
            titulo_normalizado = re.sub(r'[^\w\s]', '', datos["titulo"].lower())
            if titulo_normalizado not in titulos_vistos:
                print(f"✅ Noticia {contador}: {datos['titulo'][:60]}...")
                noticias[f"Noticia_TIC{contador}"] = datos
                titulos_vistos.add(titulo_normalizado)
                contador += 1
    
    print(f"🎯 Extracción completada: {len(noticias)} noticias únicas")
    return noticias

def generar_archivo_html(noticias):
    """Genera archivo HTML con las noticias"""
    print("🌐 Generando archivo HTML...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST NEWS - Noticias Tecnológicas</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>👻 GHOST NEWS</h1>
            <p>Noticias tecnológicas extraídas automáticamente</p>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <div class="stats">
                <h2>📊 Últimas {len(noticias)} noticias</h2>
                <p>Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</p>
            </div>

            <div class="news-grid">
"""
    
    for noticia_id, datos in noticias.items():
        imagen_html = f'<img src="{datos["imagen"]}" alt="Imagen de noticia" onerror="this.style.display=\'none\'">' if datos["imagen"] else '<div class="no-image">📰</div>'
        
        html_content += f"""
                <article class="news-card">
                    <div class="news-image">
                        {imagen_html}
                    </div>
                    <div class="news-content">
                        <h3 class="news-title">
                            <a href="{datos['enlace']}" target="_blank">{datos['titulo']}</a>
                        </h3>
                        <p class="news-summary">{datos['resumen']}</p>
                        <div class="news-footer">
                            <a href="{datos['enlace']}" target="_blank" class="read-more">Leer más →</a>
                        </div>
                    </div>
                </article>
"""
    
    html_content += """
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>© 2024 GHOST NEWS - Powered by Python + BeautifulSoup</p>
        </div>
    </footer>
</body>
</html>"""
    
    try:
        with open(CONFIGURACION['archivo_html'], 'w', encoding='utf-8') as archivo:
            archivo.write(html_content)
        print(f"✅ HTML generado: {CONFIGURACION['archivo_html']}")
        return True
    except Exception as error:
        print(f"❌ Error generando HTML: {error}")
        return False

def generar_archivo_csv(noticias):
    """Genera archivo CSV con las noticias"""
    print("📊 Generando archivo CSV...")
    
    try:
        with open(CONFIGURACION['archivo_csv'], 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Título', 'Resumen', 'Enlace', 'Imagen'])
            
            for noticia_id, datos in noticias.items():
                writer.writerow([
                    noticia_id,
                    datos['titulo'],
                    datos['resumen'],
                    datos['enlace'],
                    datos['imagen']
                ])
        
        print(f"✅ CSV generado: {CONFIGURACION['archivo_csv']} ({len(noticias)} noticias)")
        return True
    except Exception as error:
        print(f"❌ Error generando CSV: {error}")
        return False

def mostrar_resumen(noticias, html_ok, csv_ok):
    """Muestra resumen de la ejecución"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("="*60)
    print(f"🔍 Noticias extraídas: {len(noticias)}")
    print(f"📝 Archivo HTML: {'✅' if html_ok else '❌'}")
    print(f"📋 Archivo CSV: {'✅' if csv_ok else '❌'}")
    
    if noticias:
        print(f"\n📰 Últimas noticias:")
        for i, (_, datos) in enumerate(list(noticias.items())[:3], 1):
            print(f"   {i}. {datos['titulo'][:50]}...")
    
    print("="*60)

def main():
    """Función principal"""
    print("🚀 GHOST NEWS - Web Scraping Flexible")
    print("   (Solo urllib + BeautifulSoup - funciona con cualquier sitio de noticias)")
    print("="*60)
    
    # 1. Solicitar URL
    url = solicitar_url()
    
    # 2. Extraer noticias
    noticias = extraer_noticias_web(url)
    
    if not noticias:
        print("❌ No se encontraron noticias para procesar. Finalizando.")
        return False
    
    # 3. Generar archivos
    html_generado = generar_archivo_html(noticias)
    csv_generado = generar_archivo_csv(noticias)
    
    # 4. Mostrar resumen
    mostrar_resumen(noticias, html_generado, csv_generado)
    
    if html_generado and csv_generado:
        print("\n🎉 ¡Proceso completado exitosamente!")
        print("💡 Proyecto optimizado: funciona con cualquier sitio de noticias")
    else:
        print("\n⚠️ Proceso completado con algunos errores")
    
    return True

if __name__ == "__main__":
    main()
