#!/usr/bin/env python3
"""
Documentador Modular de Proyectos C++ con IA Local
Toma los resultados de analizar_proyecto_cpp.py y genera:
1. Documentación detallada por módulo con comentarios de código
2. Diagramas Mermaid de interdependencias por módulo
3. Diagrama global de interdependencias del proyecto completo
"""

import os
import sys
import json
import requests
import re
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO_DEFAULT = "qwen2.5-coder:3b"
NUM_THREADS = 3
CONTEXT_SIZE = 4096

class Colores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    NEGRITA = '\033[1m'
    FIN = '\033[0m'

def log_info(msg): print(f"{Colores.CYAN}[INFO]{Colores.FIN} {msg}", flush=True)
def log_exito(msg): print(f"{Colores.VERDE}[OK]{Colores.FIN} {msg}", flush=True)
def log_error(msg): print(f"{Colores.ROJO}[ERROR]{Colores.FIN} {msg}", flush=True)
def log_advertencia(msg): print(f"{Colores.AMARILLO}[AVISO]{Colores.FIN} {msg}", flush=True)
def log_paso(msg): print(f"\n{Colores.MAGENTA}{Colores.NEGRITA}{msg}{Colores.FIN}", flush=True)

# ============================================================================
# COMUNICACIÓN CON OLLAMA
# ============================================================================
def consultar_ia(prompt, modelo, timeout=300):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": True,
                "keep_alive": 0,
                "options": {
                    "num_ctx": CONTEXT_SIZE,
                    "num_thread": NUM_THREADS
                }
            },
            stream=True,
            timeout=timeout
        )
        response.raise_for_status()
        
        respuesta_completa = ""
        tokens = 0
        
        for linea in response.iter_lines():
            if linea:
                try:
                    datos = json.loads(linea.decode('utf-8'))
                    if 'response' in datos:
                        chunk = datos['response']
                        respuesta_completa += chunk
                        tokens += 1
                        if tokens % 50 == 0:
                            print(f"\r{Colores.VERDE}[GENERANDO]{Colores.FIN} Tokens: {tokens} | Tamaño: {len(respuesta_completa)} chars", end='', flush=True)
                except json.JSONDecodeError:
                    continue
        
        print(f"\n{Colores.VERDE}[COMPLETADO]{Colores.FIN} {tokens} tokens generados", flush=True)
        return respuesta_completa
        
    except requests.exceptions.Timeout:
        log_error("Timeout - la IA tardó demasiado")
        return None
    except Exception as e:
        log_error(f"Error en comunicación con Ollama: {e}")
        return None

# ============================================================================
# EXTRACCIÓN Y SANITIZACIÓN DE MERMAID
# ============================================================================
def extraer_mermaid(texto):
    patron = r"```mermaid\s*(.*?)\s*```"
    return re.findall(patron, texto, re.DOTALL | re.IGNORECASE)

def sanitizar_mermaid(mermaid_code):
    """Corrige agresivamente alucinaciones estructurales de la IA en Mermaid"""
    lines = mermaid_code.strip().split('\n')
    clean_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # 1. Forzar que la declaración del gráfico sea 100% limpia
        if line.lower().startswith('graph'):
            if 'td' in line.lower():
                clean_lines.append('graph TD')
            elif 'lr' in line.lower():
                clean_lines.append('graph LR')
            else:
                clean_lines.append('graph TD')
            continue # Ignora cualquier texto extra que la IA haya puesto en esta línea
            
        # 2. Ignorar líneas que son claramente texto explicativo de la IA y no sintaxis
        if not any(char in line for char in ['[', ']', '(', ')', '-->', '---', 'subgraph', 'end']):
            continue
            
        # 3. Limpiar nodos con caracteres especiales (puntos, dos puntos, comas, paréntesis)
        if '[' in line and ']' in line:
            line = re.sub(r'\[([^\[\]"]*[\(\),\.:][^\[\]"]*)\]', r'["\1"]', line)
            
        # 4. Corregir etiquetas de enlace rotas o mal formadas (ej: -->|(texto...) )
        if '-->' in line or '<--' in line:
            # Si hay un número impar de pipes '|', significa que la etiqueta de la flecha quedó abierta
            if line.count('|') % 2 != 0:
                line = re.sub(r'\|[^|]*$', r'|"relacion"|', line)
            else:
                # Asegurar que el texto entre pipes tenga comillas si no las tiene
                line = re.sub(r'\|([^"|][^|]*)\|', r'|" \1 "|', line)
                
        clean_lines.append(line)
        
    # Garantía final: si por algún motivo quedó vacío o sin encabezado, forzar uno válido
    if not clean_lines or not clean_lines[0].lower().startswith('graph'):
        clean_lines.insert(0, 'graph TD')
        
    return '\n'.join(clean_lines)

# ============================================================================
# GENERACIÓN DE IMÁGENES
# ============================================================================
def generar_imagen_mermaid(mermaid_code, ruta_salida_img, ruta_salida_mmd):
    try:
        with open(ruta_salida_mmd, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        log_info("Renderizando diagrama con Mermaid CLI...")
        
        proceso = subprocess.run(
            ['mmdc', '-i', str(ruta_salida_mmd), '-o', str(ruta_salida_img), '-b', 'white'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if proceso.returncode == 0:
            return True
        else:
            log_error(f"mmdc falló: {proceso.stderr}")
            return False
            
    except FileNotFoundError:
        log_error("No se encontró 'mmdc'. Instala: sudo npm install -g @mermaid-js/mermaid-cli")
        return False
    except subprocess.TimeoutExpired:
        log_error("Timeout en renderizado (60s)")
        return False
    except Exception as e:
        log_error(f"Error al generar imagen: {e}")
        return False

# ============================================================================
# LECTURA DE RESULTADOS
# ============================================================================
def leer_resultados_analisis(directorio):
    resultados = {'modulos': [], 'reporte_completo': None, 'archivos_cpp': []}
    dir_path = Path(directorio)
    
    reporte_completo = dir_path / "analisis_modular_completo.txt"
    if reporte_completo.exists():
        with open(reporte_completo, 'r', encoding='utf-8', errors='ignore') as f:
            resultados['reporte_completo'] = f.read()
        log_exito(f"Leído reporte completo: {reporte_completo.name}")
    
    for archivo in sorted(dir_path.glob("analisis_modulo_*.txt")):
        with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
            resultados['modulos'].append({
                'archivo': archivo,
                'contenido': f.read(),
                'nombre': archivo.stem
            })
    
    log_info(f"Encontrados {len(resultados['modulos'])} módulos analizados")
    
    for archivo in dir_path.rglob("*.cpp"):
        resultados['archivos_cpp'].append(archivo)
    for archivo in dir_path.rglob("*.h"):
        resultados['archivos_cpp'].append(archivo)
    
    log_info(f"Encontrados {len(resultados['archivos_cpp'])} archivos C++")
    return resultados

# ============================================================================
# DOCUMENTACIÓN POR MÓDULO
# ============================================================================
def documentar_modulo(modulo_info, modelo):
    nombre_modulo = modulo_info['nombre']
    contenido_analisis = modulo_info['contenido']
    
    log_paso(f"📄 DOCUMENTANDO MÓDULO: {nombre_modulo}")
    BT = "```"
    
    prompt_doc = f"""Eres un experto en documentación de código C++ y en sintaxis Mermaid. Basándote en el siguiente análisis, genera documentación técnica.

ANÁLISIS DEL MÓDULO:
{contenido_analisis}

Genera en formato Markdown:
## 📋 Documentación Técnica
### 1. Propósito y Responsabilidad
### 2. Código Comentado (con explicación de funciones y parámetros)
### 3. Interfaz Pública
### 4. Dependencias Internas
### 5. Diagrama de Interdependencias

REGLAS ESTRICTAS PARA EL DIAGRAMA MERMAID (¡CRUCIAL!):
1. Inicia siempre con `graph TD` o `graph LR`.
2. Si el texto de un nodo contiene paréntesis '()', corchetes '[]', comas ',', puntos '.', dos puntos ':' o símbolos de código, DEBES envolverlo obligatoriamente en comillas dobles.
   - ❌ INCORRECTO: `A[socket(AF_INET, SOCK_DGRAM)] --> B[Procesar]`
   - ✅ CORRECTO: `A["socket(AF_INET, SOCK_DGRAM)"] --> B["Procesar"]`
3. Cada relación (flecha) debe estar en una línea nueva y separada.
4. No incluyas texto explicativo, comentarios o saltos de línea sueltos dentro del bloque {BT}mermaid. Solo nodos y flechas.

Sintaxis de ejemplo válida:
{BT}mermaid
graph LR
    A["Módulo Actual (v1.0)"] -->|"llama a"| B["Librería Externa (tkip)"]
    C["Otro Módulo"] -->|"usa datos de"| A
{BT}

IMPORTANTE: El diagrama debe estar dentro de un bloque {BT}mermaid ... {BT} y cumplir estrictamente las reglas de comillas y sintaxis."""

    log_info("Consultando IA para documentación detallada...")
    respuesta_doc = consultar_ia(prompt_doc, modelo)
    
    if not respuesta_doc:
        log_error(f"Falló la documentación del módulo {nombre_modulo}")
        return False
    
    dir_salida = Path(modulo_info['archivo']).parent
    archivo_doc = dir_salida / f"DOC_DETALLADA_{nombre_modulo}.md"
    
    with open(archivo_doc, 'w', encoding='utf-8') as f:
        f.write(respuesta_doc)
    
    log_exito(f"Documentación guardada: {archivo_doc.name}")
    
    diagramas = extraer_mermaid(respuesta_doc)
    
    if diagramas:
        for i, diagrama in enumerate(diagramas, 1):
            # APLICAR LIMPIEZA ANTES DE RENDERIZAR
            diagrama_limpio = sanitizar_mermaid(diagrama)
            
            archivo_img = dir_salida / f"DIAGRAMA_{nombre_modulo}_{i}.png"
            archivo_mmd = dir_salida / f"DIAGRAMA_{nombre_modulo}_{i}.mmd"
            
            if generar_imagen_mermaid(diagrama_limpio, archivo_img, archivo_mmd):
                log_exito(f"Diagrama {i} generado: {archivo_img.name}")
            else:
                log_advertencia(f"Código Mermaid {i} guardado (revisar sintaxis): {archivo_mmd.name}")
    
    # ¡CRÍTICO! Faltaba este return en tu versión anterior
    return True

# ============================================================================
# DIAGRAMA GLOBAL
# ============================================================================
def generar_diagrama_global(resultados, modelo):
    log_paso("🌐 GENERANDO DIAGRAMA GLOBAL DE INTERDEPENDENCIAS")
    
    resumen_modulos = "\n".join([f"### {m['nombre']}\n{m['contenido'][:500]}..." for m in resultados['modulos']])
    BT = "```"
    
    prompt_global = f"""Eres un arquitecto de software experto. Genera un DIAGRAMA GLOBAL de interdependencias.

RESUMEN DE MÓDULOS:
{resumen_modulos}

Genera un diagrama Mermaid completo mostrando todos los módulos, dependencias y flujo de datos. Usa subgraphs para agrupar por capas.
RECUERDA: Envuelve en comillas dobles cualquier texto de nodo que tenga paréntesis, comas, puntos o dos puntos.

Sintaxis:
{BT}mermaid
graph TD
    subgraph "Capa de Lógica"
        A["Modulo 1"] --> B["Modulo 2"]
    end
{BT}

El diagrama debe estar dentro de un bloque {BT}mermaid ... {BT} y ser sintácticamente válido."""

    log_info("Consultando IA para diagrama global...")
    respuesta_global = consultar_ia(prompt_global, modelo, timeout=600)
    
    if not respuesta_global:
        log_error("Falló la generación del diagrama global")
        return False
    
    dir_salida = Path(resultados['modulos'][0]['archivo']).parent if resultados['modulos'] else Path(".")
    archivo_global = dir_salida / "DIAGRAMA_GLOBAL_INTERDEPENDENCIAS.md"
    
    with open(archivo_global, 'w', encoding='utf-8') as f:
        f.write(respuesta_global)
    log_exito(f"Documento global guardado: {archivo_global.name}")
    
    diagramas = extraer_mermaid(respuesta_global)
    if diagramas:
        for i, diagrama in enumerate(diagramas, 1):
            # APLICAR LIMPIEZA TAMBIÉN AL DIAGRAMA GLOBAL
            diagrama_limpio = sanitizar_mermaid(diagrama)
            
            archivo_img = dir_salida / f"DIAGRAMA_GLOBAL_{i}.png"
            archivo_mmd = dir_salida / f"DIAGRAMA_GLOBAL_{i}.mmd"
            
            if generar_imagen_mermaid(diagrama_limpio, archivo_img, archivo_mmd):
                log_exito(f"Diagrama global {i} generado: {archivo_img.name}")
            else:
                log_advertencia(f"Código Mermaid global guardado: {archivo_mmd.name}")
    return True

# ============================================================================
# RESUMEN EJECUTIVO
# ============================================================================
def generar_resumen_ejecutivo(resultados, modelo):
    log_paso("📊 GENERANDO RESUMEN EJECUTIVO DEL PROYECTO")
    
    prompt_resumen = f"""Eres un líder técnico. Genera un RESUMEN EJECUTIVO del proyecto C++.
Estadísticas: {len(resultados['modulos'])} módulos, {len(resultados['archivos_cpp'])} archivos C++.

Genera:
## 📊 Resumen Ejecutivo
1. Visión General
2. Arquitectura
3. Módulos Críticos
4. Puntos de Riesgo
5. Recomendaciones Estratégicas"""

    log_info("Consultando IA para resumen ejecutivo...")
    respuesta_resumen = consultar_ia(prompt_resumen, modelo)
    
    if not respuesta_resumen:
        log_error("Falló la generación del resumen ejecutivo")
        return False
    
    dir_salida = Path(resultados['modulos'][0]['archivo']).parent if resultados['modulos'] else Path(".")
    archivo_resumen = dir_salida / "RESUMEN_EJECUTIVO_PROYECTO.md"
    
    with open(archivo_resumen, 'w', encoding='utf-8') as f:
        f.write(respuesta_resumen)
    log_exito(f"Resumen ejecutivo guardado: {archivo_resumen.name}")
    return True

# ============================================================================
# FLUJO PRINCIPAL
# ============================================================================
def main():
    print(f"\n{Colores.NEGRITA}{'='*70}{Colores.FIN}", flush=True)
    print(f"{Colores.NEGRITA}  DOCUMENTADOR MODULAR CON DIAGRAMAS DE INTERDEPENDENCIA{Colores.FIN}", flush=True)
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}\n", flush=True)
    
    if len(sys.argv) < 2:
        print(f"{Colores.ROJO}Error: Debes especificar el directorio{Colores.FIN}", flush=True)
        print(f"Uso: {sys.argv[0]} <directorio_resultados> [modelo]", flush=True)
        sys.exit(1)
    
    directorio = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else MODELO_DEFAULT
    
    if not os.path.isdir(directorio):
        log_error(f"El directorio no existe: {directorio}")
        sys.exit(1)
    
    log_info(f"Modelo seleccionado: {modelo}")
    log_info(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    log_paso("📂 PASO 1: Leyendo resultados del análisis previo")
    resultados = leer_resultados_analisis(directorio)
    
    if not resultados['modulos']:
        log_error("No se encontraron módulos analizados. Ejecuta primero analizar_proyecto_cpp.py")
        sys.exit(1)
    
    log_paso(f"📄 PASO 2: Documentando {len(resultados['modulos'])} módulos")
    exitosos = 0
    fallidos = 0
    
    for i, modulo in enumerate(resultados['modulos'], 1):
        print(f"\n{Colores.AZUL}[MÓDULO {i}/{len(resultados['modulos'])}]{Colores.FIN}", flush=True)
        if documentar_modulo(modulo, modelo):
            exitosos += 1
        else:
            fallidos += 1
    
    log_exito(f"Módulos documentados: {exitosos} exitosos, {fallidos} fallidos")
    
    log_paso("🌐 PASO 3: Generando diagrama global")
    generar_diagrama_global(resultados, modelo)
    
    log_paso("📊 PASO 4: Generando resumen ejecutivo")
    generar_resumen_ejecutivo(resultados, modelo)
    
    print(f"\n{Colores.NEGRITA}{'='*70}{Colores.FIN}", flush=True)
    print(f"{Colores.NEGRITA}  DOCUMENTACIÓN COMPLETADA{Colores.FIN}", flush=True)
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}", flush=True)
    print(f"{Colores.VERDE}✓ Módulos documentados: {exitosos}{Colores.FIN}", flush=True)
    print(f"{Colores.VERDE}✓ Archivos generados en: {directorio}{Colores.FIN}", flush=True)

if __name__ == "__main__":
    main()

