## 📋 Documentación Técnica

### 1. Propósito y Responsabilidad
El módulo de captura de paquetes se encarga de abrir archivos de captura de redes en formato de archivo de WLAN (Wireshark) y leer los paquetes de la red. También se encarga de procesar los paquetes y extraer información relevante. Esta herramienta permite a los usuarios analizar la actividad de las redes a nivel de paquetes, lo que es útil para identificar problemas, mejorar la seguridad o entender cómo se comunican diferentes dispositivos en una red.

### 2. Código Comentado (con explicación de funciones y parámetros)

```cpp
// Función para abrir un archivo de captura de red en formato de archivo de WLAN
FILE *wi_open(const char *filename) {
    // Abre el archivo en modo lectura binaria
    FILE *file = fopen(filename, "rb");
    // Verifica si la apertura fue exitosa
    if (file == NULL) {
        // Si no se pudo abrir, imprime un mensaje de error y retorna NULL
        perror("Error al abrir archivo");
        return NULL;
    }
    // Retorna el descriptor de archivo
    return file;
}

// Función para leer un paquete de la red a través del descriptor de archivo
uint8_t *wi_read(FILE *file, size_t *size) {
    // Lee un paquete desde el archivo
    uint8_t *packet = (uint8_t *)malloc(*size);
    if (fread(packet, 1, *size, file) != *size) {
        // Si no se pudo leer el paquete, imprime un mensaje de error y libera la memoria
        perror("Error al leer paquete");
        free(packet);
        return NULL;
    }
    // Retorna el paquete leído
    return packet;
}

// Función para cerrar el descriptor de archivo correspondiente a un archivo de captura de redes
void wi_close(FILE *file) {
    // Cierra el archivo
    fclose(file);
}

// Función para procesar un paquete en formato binario y convertirlo en un formato más legible y fácil de trabajar
void process_packet(uint8_t *packet, size_t size) {
    // Procesa el paquete y extrae información relevante
    // ...
}
```

### 3. Interfaz Pública

```cpp
// Función para abrir un archivo de captura de red
FILE *wi_open(const char *filename);

// Función para leer un paquete de la red
uint8_t *wi_read(FILE *file, size_t *size);

// Función para cerrar el descriptor de archivo
void wi_close(FILE *file);

// Función para procesar un paquete
void process_packet(uint8_t *packet, size_t size);
```

### 4. Dependencias Internas

- **Biblioteca de Wireshark**: Para leer archivos de captura de redes y procesar paquetes.
- **Biblioteca C**: Para manejar archivos y memoria dinámica.

### 5. Diagrama de Interdependencias

```mermaid
graph TD
    A[wi_open] -->|retorna FILE*| B[FILE*]
    B[FILE*] -->|llama a| C[fopen]
    C[fopen] -->|retorna NULL| D[Error al abrir archivo]
    D[Error al abrir archivo] -->|imprime mensaje de error| E[wi_open]
    E[wi_open] -->|retorna NULL| F[Error al leer paquete]
    F[Error al leer paquete] -->|imprime mensaje de error| G[free(packet)]
    G[free(packet)] -->|libera memoria| H[wi_open]
    H[wi_open] -->|retorna NULL| I[Error al leer paquete]
    I[Error al leer paquete] -->|imprime mensaje de error| J[free(packet)]
    J[free(packet)] -->|libera memoria| K[wi_open]
    K[wi_open] -->|retorna NULL| L[Error al cerrar archivo]
    L[Error al cerrar archivo] -->|imprime mensaje de error| M[wi_open]
    M[wi_open] -->|retorna NULL| N[Error al procesar paquete]
    N[Error al procesar paquete] -->|imprime mensaje de error| O[process_packet]
    O[process_packet] -->|procesa paquete| P[extrae información relevante]
    P[extrae información relevante] -->|retorna| Q[Interfaz Pública]
```