#!/usr/bin/env python3
"""
Generador de Mapas de Procesos Detallados (Script 2 - Versión Final con Gestión de Servicios y Sanitización Avanzada)
"""

import os
import sys
import json
import requests
import re
import subprocess
import time
import logging
import signal
import atexit
from pathlib import Path
from datetime import datetime

# Variables para registro de errores
ERRORES_FILE = "errores_mermaid.json"
INFORME_FILE = "informe_mejoras.md"
lista_errores = []

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO_DEFAULT = "qwen2.5-coder:7b"
NUM_THREADS = 4 
CONTEXT_SIZE = 2048
MMDC_TIMEOUT = 1200  # 20 minutos de timeout para mmdc

# Configuración de Logging Profundo
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("proceso_detallado.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class Colores:
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    NEGRITA = '\033[1m'
    FIN = '\033[0m'

def log_info(msg): logging.info(f"{Colores.CYAN}[INFO]{Colores.FIN} {msg}")
def log_exito(msg): logging.info(f"{Colores.VERDE}[OK]{Colores.FIN} {msg}")
def log_error(msg): logging.error(f"{Colores.ROJO}[ERROR]{Colores.FIN} {msg}")
def log_advertencia(msg): logging.warning(f"{Colores.AMARILLO}[AVISO]{Colores.FIN} {msg}")
def log_paso(msg): logging.info(f"\n{Colores.MAGENTA}{Colores.NEGRITA}{msg}{Colores.FIN}")
def log_debug(msg): logging.debug(f"{Colores.AMARILLO}[DEBUG]{Colores.FIN} {msg}")

# ============================================================================
# GESTIÓN AUTOMÁTICA DE SERVICIOS (OLLAMA)
# ============================================================================
def gestionar_ollama(accion):
    try:
        if accion == 'start':
            log_info("Iniciando el servicio de Ollama...")
            subprocess.run(['sudo', 'systemctl', 'start', 'ollama'], capture_output=True, check=True)
            time.sleep(2)
            log_info("Servicio de Ollama iniciado correctamente.")
        elif accion == 'stop':
            log_info("Deteniendo el servicio de Ollama para liberar RAM...")
            # Gracias a la regla sudoers, esto ya no pedirá contraseña ni se colgará
            subprocess.run(['sudo', 'systemctl', 'stop', 'ollama'], capture_output=True, check=True)
            log_info("Servicio de Ollama detenido correctamente.")
    except subprocess.CalledProcessError as e:
        log_advertencia(f"Error al gestionar el servicio de Ollama ({accion}): {e}")
    except Exception as e:
        log_advertencia(f"Excepción al gestionar Ollama: {e}")

def cleanup():
    log_info("\n[EJECUTANDO LIMPIEZA] Finalizando script y liberando recursos...")
    gestionar_ollama('stop')  # <--- AHORA SÍ SE EJECUTA DE FORMA SEGURA

# Registrar limpieza para señales de terminación (Ctrl+C, pkill, etc.)
def signal_handler(sig, _frame):
    log_info(f"\n[SEÑAL RECIBIDA: {sig}] Iniciando apagado seguro...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # pkill

# ============================================================================
# REGISTRO DE ERRORES EN TIEMPO REAL
# ============================================================================
def registrar_error_mermaid(modulo_nombre, mermaid_code, error_stderr, linea_error):
    """Registra un error de Mermaid en la lista global y lo guarda al instante"""
    global lista_errores
    
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "modulo": modulo_nombre,
        "linea_error": linea_error,
        "mermaid_code": mermaid_code[:500],  # Primeros 500 chars para no saturar
        "error_message": error_stderr[:300] if error_stderr else "Sin detalle"
    }
    lista_errores.append(error_entry)
    
    # Guardar inmediatamente en archivo (por si el script se corta o se tilde)
    try:
        with open(ERRORES_FILE, 'w', encoding='utf-8') as f:
            json.dump(lista_errores, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log_error(f"No se pudo guardar errores en JSON: {e}")

# ============================================================================
# COMUNICACIÓN CON OLLAMA
# ============================================================================
def consultar_ia(prompt, modelo, timeout=1200):
    inicio_total = time.time()
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": modelo, 
                "prompt": prompt, 
                "stream": True, 
                "keep_alive": "5m",  # Libera la RAM a los 5 min sin necesidad de sudo
                "options": {
                    "num_ctx": CONTEXT_SIZE,
                    "num_thread": NUM_THREADS,
                    "num_predict": 1200,
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "repeat_penalty": 1.2
                }
            },
            stream=True, timeout=timeout
        )
        response.raise_for_status()
        
        respuesta_completa = ""
        tokens = 0
        primer_token_time = None
        
        for linea in response.iter_lines():
            if linea:
                try:
                    datos = json.loads(linea.decode('utf-8'))
                    if 'response' in datos:
                        if primer_token_time is None:
                            primer_token_time = time.time()
                        
                        chunk = datos['response']
                        respuesta_completa += chunk
                        tokens += 1
                        
                        if tokens % 100 == 0:
                            tiempo_actual = time.time()
                            velocidad = tokens / (tiempo_actual - primer_token_time)
                            print(f"\r{Colores.VERDE}[GENERANDO]{Colores.FIN} Tokens: {tokens} | Velocidad: {velocidad:.1f} tok/s", end='', flush=True)
                except json.JSONDecodeError:
                    continue
        
        tiempo_total = time.time() - inicio_total
        velocidad_final = tokens / tiempo_total if tiempo_total > 0 else 0
        print(f"\n{Colores.VERDE}[COMPLETADO]{Colores.FIN} {tokens} tokens en {tiempo_total:.1f}s ({velocidad_final:.1f} tok/s)", flush=True)
        return respuesta_completa
        
    except Exception as e:
        log_error(f"Error en comunicación con Ollama: {e}")
        return None

# ============================================================================
# SANITIZACIÓN DE MERMAID (VERSIÓN AVANZADA)
# ============================================================================
# ============================================================================
# SANITIZACIÓN DE MERMAID (VERSIÓN AVANZADA Y LIMPIA)
# ============================================================================
def sanitizar_mermaid(mermaid_code):
    log_debug("Iniciando proceso de sanitización del código Mermaid...")
    lines = mermaid_code.strip().split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.lower().startswith('graph'):
            clean_lines.append('graph TD' if 'td' in line.lower() else 'graph LR')
            continue
            
        if not any(char in line for char in ['[', ']', '(', ')', '-->', '---', 'subgraph', 'end', 'classDef', '{', '}']):
            continue
            
        # 0. CORRECCIÓN ESPECÍFICA: Eliminar artefactos C++ como argv[""] que rompen Mermaid
        line = line.replace('[""]', '')
        
        # 1. CORRECCIÓN CRÍTICA: Separar 'endsubgraph' en 'end' + 'subgraph'
        line = re.sub(r'\bendsubgraph\b', 'end\nsubgraph', line, flags=re.IGNORECASE)
        
        # 2. CORRECCIÓN CRÍTICA: Separar cualquier cierre de nodo pegado a 'end' o 'subgraph'
        line = re.sub(r'(\]|\})\s*(end|subgraph)', r'\1\n\2', line, flags=re.IGNORECASE)
        line = re.sub(r'\b(end|subgraph)([A-Za-z0-9_])', r'\1\n\2', line, flags=re.IGNORECASE)
        
        # 3. CORRECCIÓN: Limpiar comillas internas en nodos {} y []
        line = re.sub(r'\{([^"{}]*?)"([^"}]*?)"([^"}]*?)\}', 
                     lambda m: '{"' + m.group(1).replace('"','') + m.group(2) + m.group(3).replace('"','') + '"}', line)
        line = re.sub(r'\[([^"\[\]]*?)"([^"\]]*?)"([^"\[\]]*?)\]', 
                     lambda m: '["' + m.group(1).replace('"','') + m.group(2) + m.group(3).replace('"','') + '"]', line)
        
        # 4. CORRECCIÓN: Texto sin comillas dentro de diamantes {}
        line = re.sub(r'\{([^"{}]*?)\}', lambda m: '{"' + m.group(1).replace('"', '').replace('\n', ' ').strip() + '"}', line)
        
        # 5. CORRECCIÓN: Texto sin comillas dentro de corchetes []
        if '[' in line and ']' in line:
            line = re.sub(r'\[([^\[\]]*)\]', lambda m: '["' + m.group(1).replace('"', '').replace('\n', ' ').strip() + '"]', line)
            
        # 6. CORRECCIÓN SUAVE: Asegurar espacios en flechas
        if '-->' in line or '<--' in line:
            line = re.sub(r'-->', ' --> ', line)
            line = re.sub(r'<--', ' <-- ', line)
            
        # 7. FILTRO DE SEGURIDAD: Descartar líneas huérfanas o rotas
        if line.startswith('|'):
            continue
            
        if '-->' in line or '<--' in line:
            parts = line.split('-->') if '-->' in line else line.split('<--')
            left_side = parts[0].strip()
            if left_side and not re.match(r'^[A-Za-z0-9_]+$', left_side) and '[' not in left_side and '{' not in left_side:
                continue
                
        clean_lines.append(line)
        
    if not clean_lines or not clean_lines[0].lower().startswith('graph'):
        clean_lines.insert(0, 'graph TD')
        
    log_debug(f"Sanitización completada. Líneas limpias: {len(clean_lines)}")
    return '\n'.join(clean_lines)
def generar_imagen_mermaid(mermaid_code, ruta_salida_img, ruta_salida_mmd):
    try:
        log_debug(f"Escribiendo código Mermaid en archivo: {ruta_salida_mmd}")
        with open(ruta_salida_mmd, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        tamaño_archivo = os.path.getsize(ruta_salida_mmd)
        log_debug(f"Tamaño del archivo .mmd generado: {tamaño_archivo} bytes")
        
        log_info("Iniciando renderizado con Mermaid CLI (mmdc)...")
        log_debug(f"Comando: mmdc -i {ruta_salida_mmd} -o {ruta_salida_img} -b white")
        
        start_mmdc = time.time()
        
        env = os.environ.copy()
        env['PUPPETEER_SKIP_CHROMIUM_DOWNLOAD'] = '1'
        
        proceso = subprocess.run(
            ['mmdc', '-i', str(ruta_salida_mmd), '-o', str(ruta_salida_img), '-b', 'white'],
            capture_output=True, 
            text=True, 
            timeout=MMDC_TIMEOUT,
            env=env
        )
        
        end_mmdc = time.time()
        tiempo_transcurrido = end_mmdc - start_mmdc
        
        log_debug(f"mmdc finalizó en {tiempo_transcurrido:.2f}s. Returncode: {proceso.returncode}")
        
        # === LOG FORENSE Y REGISTRO DE ERROR ===
        if proceso.returncode != 0:
            log_error(f"mmdc falló (código {proceso.returncode}).")
            log_error("--- INICIO DEL CÓDIGO MERMAID QUE FALLÓ ---")
            log_error(mermaid_code)
            log_error("--- FIN DEL CÓDIGO MERMAID QUE FALLÓ ---")
            if proceso.stderr.strip():
                log_error(f"mmdc STDERR:\n{proceso.stderr}")
            
            # Registrar error para análisis (se guarda al instante)
            linea_error = "Desconocida"
            if "line" in proceso.stderr.lower():
                match = re.search(r'line (\d+)', proceso.stderr, re.IGNORECASE)
                if match:
                    linea_error = match.group(1)
            
            registrar_error_mermaid(ruta_salida_img.stem, mermaid_code, proceso.stderr, linea_error)
            return False
            
        if proceso.returncode == 0 and os.path.exists(ruta_salida_img):
            tamaño_img = os.path.getsize(ruta_salida_img)
            log_exito(f"Renderizado exitoso en {tiempo_transcurrido:.2f}s. Imagen: {tamaño_img} bytes")
            return True
        else:
            log_error(f"mmdc reportó éxito pero no se encontró la imagen.")
            return False
            
    except subprocess.TimeoutExpired:
        log_error(f"mmdc excedió el límite de {MMDC_TIMEOUT}s.")
        return False
    except FileNotFoundError:
        log_error("No se encontró 'mmdc'. Instala: sudo npm install -g @mermaid-js/mermaid-cli")
        return False
    except Exception as e:
        log_error(f"Error inesperado al generar imagen: {str(e)}", exc_info=True)
        return False

# ============================================================================
# LECTURA DE RESULTADOS
# ============================================================================
def leer_resultados_funcionales(directorio):
    log_debug(f"Escaneando directorio: {directorio}")
    resultados = {'modulos': []}
    dir_path = Path(directorio)
    
    for archivo in sorted(dir_path.glob("func_modulo_*.md")):
        with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
            resultados['modulos'].append({
                'archivo': archivo,
                'nombre': archivo.stem.replace('func_', ''),
                'contenido': f.read()
            })
    
    log_info(f"Encontrados {len(resultados['modulos'])} módulos funcionales para mapear")
    return resultados

# ============================================================================
# GENERACIÓN DEL MAPA DE PROCESOS POR MÓDULO
# ============================================================================

# ============================================================================
# GENERACIÓN DEL MAPA DE PROCESOS POR MÓDULO
# ============================================================================

def limpiar_reintentos_fallidos(nombre_modulo, dir_salida):
    """Si el módulo falló en una ejecución anterior, borra sus restos para un intento limpio"""
    if not os.path.exists(ERRORES_FILE):
        return
        
    try:
        with open(ERRORES_FILE, 'r', encoding='utf-8') as f:
            errores = json.load(f)
        
        # Si el módulo está en la lista de errores históricos, limpiamos sus archivos viejos
        if any(e['modulo'] == nombre_modulo for e in errores):
            log_advertencia(f"🧹 Limpiando restos de ejecución fallida previa para: {nombre_modulo}")
            for archivo in dir_salida.glob(f"MAPA_PROCESO_{nombre_modulo}_*.*"):
                archivo.unlink() # Borra el .mmd o .png corrupto
    except Exception:
        pass # Si no se puede leer el JSON, continuamos normal


def generar_mapa_proceso(modulo_info, modelo):
    nombre_modulo = modulo_info['nombre']
    contenido = modulo_info['contenido']
    dir_salida = Path(modulo_info['archivo']).parent
    
    # 1. LIMPIEZA INTELIGENTE: Borra archivos si este módulo falló antes
    limpiar_reintentos_fallidos(nombre_modulo, dir_salida)
    
    # 2. VERIFICAR SI YA EXISTE EL MAPA (y es válido, > 1KB)
    archivo_img = dir_salida / f"MAPA_PROCESO_{nombre_modulo}_1.png"
    
    if archivo_img.exists() and archivo_img.stat().st_size > 1000:
        log_exito(f"⏭️  SKIP: {nombre_modulo} ya fue generado exitosamente ({archivo_img.name})")
        return True
    # ======================================
       
    log_paso(f"🗺️  MAPEANDO PROCESOS: {nombre_modulo}")
    log_debug(f"Longitud del contenido del módulo a procesar: {len(contenido)} caracteres")
       
    prompt_mapa = f"""You are a strict Mermaid diagram generator. Analyze this C++ module and output ONLY a valid `graph TD`.

MODULE:
{contenido}

STRICT RULES (VIOLATING THESE BREAKS THE DIAGRAM):
1. Start with `graph TD`
2. Use `subgraph "Name"` and `end` for grouping.
3. Node IDs must be simple letters/numbers (e.g., A, B1, Step1).
4. Labels with spaces, (), ., or : MUST be in double quotes: `A["Function(param)"]`
5. Conditions use double curly braces: `B{{"Is valid?"}}`
6. Arrows MUST have spaces: `A --> B` or `A -->|Yes| B`
7. NO markdown text outside the ```mermaid ... ``` block.
8. MAXIMUM 30 nodes. Keep it high-level.

Example:
```mermaid
graph TD
    subgraph "Init"
        A["Start()"] --> B{{"Check params"}}
    end
    B -->|Valid| C["Process()"]
    B -->|Invalid| D["Error()"]

Generate ONLY the Mermaid code block. No extra explanations."""

    respuesta = consultar_ia(prompt_mapa, modelo, timeout=1200)
    
    if not respuesta:
        log_error(f"Falló la generación del mapa para {nombre_modulo}")
        return False
    
    patron = r"```mermaid\s*(.*?)\s*```"
    coincidencias = re.findall(patron, respuesta, re.DOTALL | re.IGNORECASE)
    
    if not coincidencias:
        respuesta_stripped = respuesta.strip()
        if respuesta_stripped.startswith("```mermaid"):
            log_advertencia("La IA se cortó por límite de tokens. Forzando cierre del bloque.")
            diagrama_forzado = respuesta_stripped
            if not diagrama_forzado.endswith("```"):
                diagrama_forzado += "\n```"
            coincidencias = [diagrama_forzado]
        else:
            log_advertencia(f"No se encontró bloque mermaid en la respuesta para {nombre_modulo}")
            log_debug(f"Respuesta cruda:\n{respuesta[:500]}...")
            return False
    
    for i, diagrama in enumerate(coincidencias, 1):
        diagrama_limpio = sanitizar_mermaid(diagrama)
        
        dir_salida = Path(modulo_info['archivo']).parent
        archivo_img = dir_salida / f"MAPA_PROCESO_{nombre_modulo}_{i}.png"
        archivo_mmd = dir_salida / f"MAPA_PROCESO_{nombre_modulo}_{i}.mmd"
        
        if generar_imagen_mermaid(diagrama_limpio, archivo_img, archivo_mmd):
            log_exito(f"Mapa de procesos generado exitosamente: {archivo_img.name}")
        else:
            log_advertencia(f"Falló el renderizado, pero el código fuente se guardó en: {archivo_mmd.name}")
            
    return True

# ============================================================================
# GENERACIÓN DE INFORME DE MEJORAS
# ============================================================================

def generar_informe_mejoras():
    """Analiza los errores registrados y genera recomendaciones para mejorar el código"""
    global lista_errores
    
    log_info("Generando informe de mejoras basado en errores registrados...")
    
    if not lista_errores:
        informe = """# 📊 Informe de Mejoras - Generador de Mapas de Procesos

## ✅ Resumen Ejecutivo
**¡Excelente!** No se registraron errores de sintaxis Mermaid durante la ejecución.

## 🎯 Conclusión
El sistema de sanitización actual es efectivo. No se requieren modificaciones inmediatas.

## 📈 Estadísticas
- Total de módulos procesados: Exitosos
- Tasa de éxito: 100%
- Errores de sintaxis: 0

## 🔮 Próximas Optimizaciones Sugeridas
1. **Aumentar NUM_THREADS** si la CPU tiene más núcleos disponibles
2. **Reducir CONTEXT_SIZE** a 1024 si se necesita más velocidad (puede afectar calidad)
3. **Implementar caché de prompts** para módulos idénticos
"""
    else:
        # Analizar patrones de errores
        patrones = {}
        for error in lista_errores:
            msg = error['error_message'].lower()
            if 'end' in msg and 'subgraph' in msg:
                patrones['endsubgraph_pegado'] = patrones.get('endsubgraph_pegado', 0) + 1
            if 'pipe' in msg or '|' in msg:
                patrones['pipe_huerfano'] = patrones.get('pipe_huerfano', 0) + 1
            if 'diamond' in msg or '{' in msg:
                patrones['diamante_sin_id'] = patrones.get('diamante_sin_id', 0) + 1
            if 'quote' in msg or '"' in msg:
                patrones['comillas_internas'] = patrones.get('comillas_internas', 0) + 1
        
        recomendaciones = []
        if patrones.get('endsubgraph_pegado', 0) > 0:
            recomendaciones.append(f"**{patrones['endsubgraph_pegado']} errores de `endsubgraph` pegado**: Agregar regex `re.sub(r'\\bendsubgraph\\b', 'end\\nsubgraph', line)`")
        if patrones.get('pipe_huerfano', 0) > 0:
            recomendaciones.append(f"**{patrones['pipe_huerfano']} errores de pipes huérfanos**: Filtrar líneas que empiecen con `|` sin nodo previo")
        if patrones.get('diamante_sin_id', 0) > 0:
            recomendaciones.append(f"**{patrones['diamante_sin_id']} diamantes sin ID**: Inyectar ID automático `N1` antes de `{{`")
        if patrones.get('comillas_internas', 0) > 0:
            recomendaciones.append(f"**{patrones['comillas_internas']} comillas internas**: Escapar o eliminar comillas dentro de labels")
        
        informe = f"""# 📊 Informe de Mejoras - Generador de Mapas de Procesos

## ⚠️ Resumen Ejecutivo
Se detectaron **{len(lista_errores)} errores de sintaxis Mermaid** durante la ejecución.

## 📈 Estadísticas
- Total de módulos procesados: {len(lista_errores)} con errores
- Tasa de éxito: Requiere revisión
- Errores de sintaxis: {len(lista_errores)}

## 🔍 Patrones Detectados

"""
        for patron, cantidad in patrones.items():
            informe += f"- **{patron.replace('_', ' ').title()}**: {cantidad} ocurrencias\n"
        
        informe += "\n## 🛠️ Recomendaciones de Código\n\n"
        for i, rec in enumerate(recomendaciones, 1):
            informe += f"{i}. {rec}\n\n"
        
        informe += """## 📁 Archivos de Error
Revisa el archivo `errores_mermaid.json` para ver el código Mermaid exacto que falló.

## 🔄 Próxima Ejecución
1. Aplica las recomendaciones de código arriba
2. Elimina los archivos PNG generados (si quieres regenerar todos)
3. Ejecuta el script nuevamente
"""
    
    # Guardar informe
    try:
        with open(INFORME_FILE, 'w', encoding='utf-8') as f:
            f.write(informe)
        log_exito(f"Informe de mejoras guardado en: {INFORME_FILE}")
    except Exception as e:
        log_error(f"No se pudo guardar el informe: {e}")

# ============================================================================
# FLUJO PRINCIPAL
# ============================================================================

def main():
    # 1. INICIAR SERVICIO AUTOMÁTICAMENTE
    gestionar_ollama('start')
    
    logging.info("="*70)
    logging.info("  GENERADOR DE MAPAS DE PROCESOS (VERSIÓN FINAL)")
    logging.info("="*70)
    
    if len(sys.argv) < 2:
        log_error("Debes especificar el directorio")
        print(f"Uso: {sys.argv[0]} <directorio_resultados_script_1> [modelo]")
        sys.exit(1)
    
    directorio = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else MODELO_DEFAULT
    
    if not os.path.isdir(directorio):
        log_error(f"El directorio no existe: {directorio}")
        sys.exit(1)
    
    log_info(f"Modelo seleccionado: {modelo}")
    log_info(f"Fecha y hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    resultados = leer_resultados_funcionales(directorio)
    if not resultados['modulos']:
        log_error("No se encontraron archivos 'func_modulo_*.md'. Ejecuta primero el Script 1.")
        sys.exit(1)
    
    log_paso(f"📄 PROCESANDO {len(resultados['modulos'])} MÓDULOS")
    exitosos = 0
    
    for i, modulo in enumerate(resultados['modulos'], 1):
        log_info(f"\n{Colores.AZUL}[MÓDULO {i}/{len(resultados['modulos'])}]{Colores.FIN}")
        modulo_start = time.time()
        
        if generar_mapa_proceso(modulo, modelo):
            exitosos += 1
            
        modulo_end = time.time()
        log_info(f"--> Módulo {i} finalizado en {modulo_end - modulo_start:.2f} segundos totales.")
            
    # === GENERAR INFORME DE MEJORAS ANTES DE CERRAR ===
    generar_informe_mejoras()
    # ==================================================
    
    log_exito(f"Proceso finalizado: {exitosos}/{len(resultados['modulos'])} mapas generados exitosamente.")
    logging.info("="*70)

if __name__ == "__main__":
    main()

