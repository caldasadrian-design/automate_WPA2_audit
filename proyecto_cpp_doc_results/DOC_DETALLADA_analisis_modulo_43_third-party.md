## 📋 Documentación Técnica

### 1. Propósito y Responsabilidad
Este módulo se encarga de proporcionar definiciones y funciones específicas para el protocolo 802.11 y el manejo de duraciones de los frames en la capa física. Este módulo se encarga de establecer las constantes necesarias para las duraciones de los frames en la capa física, como el tamaño mínimo y máximo de un frame RTS, el tamaño mínimo y máximo de fragmentación de un frame TX, y las duraciones específicas para PHY en DSSS (Direct Sequence Spread Spectrum). También se definieron estructuras para manejar las duraciones de los frames en tiempo real.

### 2. Código Comentado (con explicación de funciones y parámetros)
```cpp
// Definición de constantes para las duraciones de los frames en la capa física
#define RTS_MIN_LEN 64 // Longitud mínima de un frame RTS
#define RTS_MAX_LEN 2312 // Longitud máxima de un frame RTS
#define TX_MIN_LEN 256 // Longitud mínima de fragmentación de un frame TX
#define TX_MAX_LEN 2304 // Longitud máxima de fragmentación de un frame TX
#define PHY_DSSS_SHORT_DUR 16 // Duración de un PHY en DSSS (longitud corta)
#define PHY_DSSS_LONG_DUR 32 // Duración de un PHY en DSSS (longitud larga)
```

### 3. Interfaz Pública
```cpp
// Estructura para manejar las duraciones de los frames en tiempo real
struct Duration {
    uint32_t min;
    uint32_t max;
};

// Función para obtener la duración mínima y máxima de un frame RTS
Duration getRtsDuration() {
    return {RTS_MIN_LEN, RTS_MAX_LEN};
}

// Función para obtener la duración mínima y máxima de un frame TX
Duration getTxDuration() {
    return {TX_MIN_LEN, TX_MAX_LEN};
}

// Función para obtener las duraciones específicas de PHY en DSSS
Duration getPhyDssdDuration() {
    return {PHY_DSSS_SHORT_DUR, PHY_DSSS_LONG_DUR};
}
```

### 4. Dependencias Internas
Este módulo depende de otros módulos específicos del sistema operativo para definiciones comunes, como el tamaño de los buffers de datos y los tamaños de los headers de frame.

### 5. Diagrama de Interdependencias

```mermaid
graph LR
    A[Modulo Actual (v1.0)] -->|"llama a"| B[Librería Externa (tkip)]
    C[Otro Módulo] -->|"usa datos de"| A
```

IMPORTANTE: El diagrama debe estar dentro de un bloque ```mermaid ... ``` y cumplir estrictamente las reglas de comillas y sintaxis.