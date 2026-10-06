#!/usr/bin/env python3
"""
Analizador de proyectos C++ con IA local (Ollama) - Con progreso en tiempo real
Uso: ./analizar_proyecto_cpp.py <directorio_proyecto> [modelo]
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO_DEFAULT = "deepseek-coder:6.7b"
TOKENS_MAXIMOS = 6000
NUM_THREADS = 3  # Límite de hilos de CPU (ajusta según nproc - 1)
ARCHIVOS_RELEVANTES = {'.cpp', '.h', '.hpp', '.c', '.cc', '.cxx', '.hxx'}

# ============================================================================
# COLORES PARA TERMINAL
# ============================================================================
class Colores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    CYAN = '\033[96m'
    NEGRITA = '\033[1m'
    FIN = '\033[0m'

# ============================================================================
# FUNCIONES DE LOG
# ============================================================================
def log_info(mensaje):
    print(f"{Colores.CYAN}[INFO]{Colores.FIN} {mensaje}")

def log_exito(mensaje):
    print(f"{Colores.VERDE}[OK]{Colores.FIN} {mensaje}")

def log_advertencia(mensaje):
    print(f"{Colores.AMARILLO}[AVISO]{Colores.FIN} {mensaje}")

def log_error(mensaje):
    print(f"{Colores.ROJO}[ERROR]{Colores.FIN} {mensaje}")

def log_progreso(actual, total, mensaje):
    porcentaje = (actual / total) * 100
    barra = "█" * int(porcentaje / 2) + "░" * (50 - int(porcentaje / 2))
    print(f"\r{Colores.AZUL}[PROGRESO]{Colores.FIN} [{barra}] {porcentaje:5.1f}% ({actual}/{total}) {mensaje}", end='', flush=True)
    if actual == total:
        print()

# ============================================================================
# ESCANEO DE ARCHIVOS
# ============================================================================
def obtener_archivos_proyecto(directorio):
    """Escanea recursivamente el proyecto"""
    log_info(f"Escaneando proyecto en: {directorio}")
    archivos = []
    
    for root, dirs, files in os.walk(directorio):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build', 'Debug', 'Release', '.svn', 'bin', 'obj'}]
        
        for file in files:
            if Path(file).suffix in ARCHIVOS_RELEVANTES:
                ruta_completa = os.path.join(root, file)
                archivos.append(ruta_completa)
    
    log_exito(f"Encontrados {len(archivos)} archivos C++")
    return archivos

def leer_archivo(ruta):
    """Lee el contenido de un archivo"""
    try:
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        log_error(f"Error al leer {ruta}: {e}")
        return f"[Error al leer: {e}]"

def contar_tokens(texto):
    """Estimación aproximada de tokens (1 token ≈ 4 caracteres)"""
    return len(texto) // 4

# ============================================================================
# COMUNICACIÓN CON OLLAMA
# ============================================================================
def enviar_a_ollama_stream(prompt, modelo, archivo_salida):
    """Envía el prompt a Ollama con streaming en tiempo real"""
    log_info(f"Conectando con Ollama ({OLLAMA_URL})...")
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": True,
                "keep_alive": 0,
                "options": {
                    "num_ctx": 2048,
                    "num_thread": NUM_THREADS
                }
            },
            stream=True,
            timeout=600
        )
        response.raise_for_status()
        
        log_exito("Conexión establecida. Recibiendo respuesta...")
        log_info("Generando análisis (esto puede tardar varios minutos)...\n")
        
        respuesta_completa = ""
        tokens_recibidos = 0
        inicio = time.time()
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for linea in response.iter_lines():
                if linea:
                    try:
                        datos = json.loads(linea.decode('utf-8'))
                        if 'response' in datos:
                            chunk = datos['response']
                            respuesta_completa += chunk
                            tokens_recibidos += 1
                            f.write(chunk)
                            f.flush()
                            
                            if tokens_recibidos % 50 == 0:
                                elapsed = time.time() - inicio
                                print(f"\r{Colores.VERDE}[GENERANDO]{Colores.FIN} Tokens: {tokens_recibidos} | Tiempo: {elapsed:.0f}s | Tamaño: {len(respuesta_completa)} chars", end='', flush=True)
                    except json.JSONDecodeError:
                        continue
        
        elapsed = time.time() - inicio
        print(f"\n{Colores.VERDE}[COMPLETADO]{Colores.FIN} Generación finalizada en {elapsed:.0f} segundos")
        print(f"Total de tokens generados: {tokens_recibidos}")
        print(f"Tamaño del reporte: {len(respuesta_completa)} caracteres")
        
        return respuesta_completa
        
    except requests.exceptions.Timeout:
        log_error("Timeout - el modelo tardó demasiado")
        return "[ERROR: Timeout]"
    except Exception as e:
        log_error(f"Error en la comunicación con Ollama: {e}")
        return f"[ERROR: {e}]"

# ============================================================================
# ANÁLISIS DE PROYECTO PEQUEÑO (cabe en un solo prompt)
# ============================================================================
def analizar_proyecto(directorio, modelo):
    """Función principal de análisis para proyectos pequeños"""
    print(f"\n{Colores.NEGRITA}{'='*70}{Colores.FIN}")
    print(f"{Colores.NEGRITA}  ANALIZADOR DE PROYECTOS C++ CON IA LOCAL{Colores.FIN}")
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}\n")
    
    log_info(f"Modelo seleccionado: {modelo}")
    log_info(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Paso 1: Escanear archivos
    print(f"{Colores.AZUL}[PASO 1/4]{Colores.FIN} Escaneando archivos del proyecto...")
    archivos = obtener_archivos_proyecto(directorio)
    
    if not archivos:
        log_error("No se encontraron archivos C++ en el proyecto")
        sys.exit(1)
    
    print()
    
    # Paso 2: Leer archivos
    print(f"{Colores.AZUL}[PASO 2/4]{Colores.FIN} Leyendo contenido de archivos...")
    contenido_total = ""
    total_chars = 0
    
    for i, archivo in enumerate(archivos, 1):
        log_progreso(i, len(archivos), f"Leyendo {os.path.basename(archivo)}")
        contenido = leer_archivo(archivo)
        total_chars += len(contenido)
        contenido_total += f"\n\n{'='*60}\n### ARCHIVO: {archivo}\n{'='*60}\n\n{contenido}"
        time.sleep(0.05)
    
    print()
    log_exito(f"Leídos {len(archivos)} archivos ({total_chars} caracteres)")
    
    tokens_totales = contar_tokens(contenido_total)
    log_info(f"Tamaño total estimado: ~{tokens_totales} tokens")
    print()
    
    # Paso 3: Enviar a IA
    print(f"{Colores.AZUL}[PASO 3/4]{Colores.FIN} Enviando análisis a la IA...")
    
    if tokens_totales > TOKENS_MAXIMOS:
        log_advertencia(f"Proyecto muy grande ({tokens_totales} tokens > {TOKENS_MAXIMOS})")
        log_info("Dividiendo en análisis por módulos...")
        print()
        return analizar_por_modulos(archivos, modelo)
    
    prompt = f"""Actúa como un arquitecto de software experto en C++ con 20 años de experiencia.
Analiza el siguiente proyecto C++ completo y genera un REPORTE TÉCNICO detallado.

El proyecto contiene {len(archivos)} archivos.

{contenido_total}

Genera el siguiente REPORTE:

# REPORTE DE ANÁLISIS DE PROYECTO C++

## 1. RESUMEN EJECUTIVO
- Propósito del proyecto (2-3 oraciones)
- Arquitectura general (monolítico, modular, etc.)
- Tecnologías y librerías utilizadas

## 2. ESTRUCTURA DEL PROYECTO
- Lista de archivos principales y su responsabilidad
- Diagrama de dependencias (texto)
- Organización de carpetas

## 3. ANÁLISIS DE COMPONENTES PRINCIPALES
Para cada función/método/clase importante:
- Nombre y ubicación
- Responsabilidad
- Complejidad estimada (baja/media/alta)

## 4. FLUJO DE DATOS
- ¿Cómo se mueven los datos entre componentes?
- Puntos de entrada y salida
- Manejo de errores

## 5. CUELLOS DE BOTELLA Y PROBLEMAS
- Problemas de rendimiento identificados
- Problemas de memoria (fugas, uso excesivo)
- Code smells o anti-patrones

## 6. SEGURIDAD
- Vulnerabilidades potenciales
- Manejo de entradas de usuario
- Validaciones faltantes

## 7. SUGERENCIAS DE MEJORA
- Top 5 mejoras prioritarias (con justificación)
- Refactorizaciones recomendadas
- Optimizaciones de rendimiento

## 8. MÉTRICAS ESTIMADAS
- Líneas de código totales
- Complejidad ciclomática estimada
- Cobertura de comentarios (%)

## 9. CONCLUSIÓN
- Estado general del código
- Recomendación final

Responde en español, de forma técnica pero clara."""
    
    archivo_salida = f"analisis_{Path(directorio).name}_{modelo.replace(':', '_').replace('.', '_')}.txt"
    respuesta = enviar_a_ollama_stream(prompt, modelo, archivo_salida)
    
    print()
    print(f"{Colores.AZUL}[PASO 4/4]{Colores.FIN} Guardando reporte...")
    log_exito(f"Reporte guardado en: {archivo_salida}")
    
    print(f"\n{Colores.NEGRITA}{'='*70}{Colores.FIN}")
    print(f"{Colores.NEGRITA}  ANÁLISIS COMPLETADO{Colores.FIN}")
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}")
    print(f"{Colores.VERDE}✓ Archivos analizados: {len(archivos)}{Colores.FIN}")
    print(f"{Colores.VERDE}✓ Tamaño del reporte: {len(respuesta)} caracteres{Colores.FIN}")
    print(f"{Colores.VERDE}✓ Archivo de salida: {archivo_salida}{Colores.FIN}")
    print()
    
    return archivo_salida

# ============================================================================
# ANÁLISIS POR MÓDULOS (para proyectos grandes)
# ============================================================================
def analizar_por_modulos(archivos, modelo):
    """Divide el análisis en módulos"""
    print(f"\n{Colores.AMARILLO}[MODO MÓDULOS]{Colores.FIN} Analizando proyecto grande por módulos...\n")
    
    modulos = {}
    for archivo in archivos:
        carpeta = os.path.dirname(archivo)
        if carpeta not in modulos:
            modulos[carpeta] = []
        modulos[carpeta].append(archivo)
    
    log_info(f"Proyecto dividido en {len(modulos)} módulos")
    print()
    
    reporte_completo = "# REPORTE DE ANÁLISIS DE PROYECTO C++ (ANÁLISIS POR MÓDULOS)\n\n"
    reporte_completo += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    reporte_completo += f"Modelo: {modelo}\n\n"
    
    modulos_exitosos = 0
    modulos_fallidos = 0
    
    for i, (modulo, archivos_modulo) in enumerate(modulos.items(), 1):
        print(f"{Colores.AZUL}[MÓDULO {i}/{len(modulos)}]{Colores.FIN} {modulo}")
        log_info(f"Archivos en este módulo: {len(archivos_modulo)}")
        
        contenido_modulo = ""
        for j, archivo in enumerate(archivos_modulo, 1):
            log_progreso(j, len(archivos_modulo), f"Leyendo {os.path.basename(archivo)}")
            contenido = leer_archivo(archivo)
            contenido_modulo += f"\n\n### {archivo}\n{contenido}"
            time.sleep(0.05)
        
        print()
        
        prompt = f"""Analiza este módulo del proyecto C++:

{contenido_modulo}

Proporciona:
1. Responsabilidad del módulo
2. Funciones/clases principales
3. Dependencias
4. Problemas identificados
5. Sugerencias de mejora"""
        
        archivo_salida_modulo = f"analisis_modulo_{i}_{Path(modulo).name if modulo else 'root'}.txt"
        log_info(f"Enviando módulo {i} a la IA...")
        
        respuesta = enviar_a_ollama_stream(prompt, modelo, archivo_salida_modulo)
        
        # === CORRECCIÓN: Validar error DENTRO del bucle for ===
        if respuesta.startswith("[ERROR"):
            log_error(f"El módulo {i} falló o excedió el tiempo. Se omitirá.")
            modulos_fallidos += 1
            continue  # ← Aquí SÍ funciona porque estamos dentro del for
        # ================================================================
        
        reporte_completo += f"\n\n{'='*60}\n## MÓDULO {i}: {modulo}\n{'='*60}\n\n{respuesta}\n"
        log_exito(f"Módulo {i} completado")
        modulos_exitosos += 1
        print()
    
    # Análisis global final (solo si hubo módulos exitosos)
    if modulos_exitosos > 0:
        print(f"{Colores.AZUL}[ANÁLISIS GLOBAL]{Colores.FIN} Generando resumen final...")
        prompt_global = f"""Basándote en los análisis de {modulos_exitosos} módulos exitosos, genera un RESUMEN GLOBAL del proyecto:
1. Arquitectura general
2. Top 5 problemas críticos
3. Top 5 mejoras prioritarias
4. Conclusión final"""
        
        archivo_salida_global = f"analisis_global_resumen.txt"
        resumen = enviar_a_ollama_stream(prompt_global, modelo, archivo_salida_global)
        reporte_completo += f"\n\n{'='*60}\n## RESUMEN GLOBAL\n{'='*60}\n\n{resumen}\n"
    
    # Guardar reporte completo
    archivo_salida = f"analisis_modular_completo.txt"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(reporte_completo)
    
    log_exito(f"Reporte completo guardado en: {archivo_salida}")
    print()
    
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}")
    print(f"{Colores.NEGRITA}  ANÁLISIS MODULAR COMPLETADO{Colores.FIN}")
    print(f"{Colores.NEGRITA}{'='*70}{Colores.FIN}")
    print(f"{Colores.VERDE}✓ Módulos exitosos: {modulos_exitosos}{Colores.FIN}")
    if modulos_fallidos > 0:
        print(f"{Colores.ROJO}✗ Módulos fallidos: {modulos_fallidos}{Colores.FIN}")
    print(f"{Colores.VERDE}✓ Reporte completo: {archivo_salida}{Colores.FIN}")
    print()
    
    return archivo_salida

# ============================================================================
# PUNTO DE ENTRADA (UN SOLO BLOQUE)
# ============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Colores.ROJO}Error: Debes especificar un directorio{Colores.FIN}")
        print(f"Uso: {sys.argv[0]} <directorio_proyecto> [modelo]")
        print(f"Ejemplo: {sys.argv[0]} /home/adri/eclipse-workspace-cpp/WL-V1.7")
        sys.exit(1)
    
    directorio = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else MODELO_DEFAULT
    
    if not os.path.isdir(directorio):
        log_error(f"El directorio no existe: {directorio}")
        sys.exit(1)
    
    analizar_proyecto(directorio, modelo)