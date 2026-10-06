## 📋 Documentación Técnica

### 1. Propósito y Responsabilidad

El módulo está diseñado para manejar la lógica del cifrado y la fuerza bruta de las redes inalámbricas. Se encarga de insertar claves de cifrado en un AVL (Árbol Binario de Búsqueda Balanceado) para búsquedas eficientes. También maneja la creación y gestión de hilos para ataques de fuerza bruta multihilo.

### 2. Código Comentado (con explicación de funciones y parámetros)

```cpp
// Función principal que inicia el programa
int main() {
    // Llama a la función get_first_target() para obtener el primer objetivo
    get_first_target();

    // Crea y ejecuta hilos para ataques de fuerza bruta
    create_and_run_threads();

    // Ejecuta la función perform_wep_crack() para ataques contra redes WEP
    perform_wep_crack();

    // Ejecuta la función perform_wpa_crack() para ataques contra redes WPA
    perform_wpa_crack();

    // Guarda la sesión de la prueba en un archivo
    session_save_thread();

    // Cierra el programa de forma adecuada
    clean_exit();
}
```

### 3. Interfaz Pública

- `get_first_target()`: Obtiene el primer objetivo para la prueba.
- `c_avl_insert()`: Inserta una clave de cifrado en el AVL.
- `c_avl_size()`: Obtiene el tamaño del AVL.
- `perform_wep_crack()`: Realiza ataques de fuerza bruta contra redes WEP.
- `perform_wpa_crack()`: Realiza ataques de fuerza bruta contra redes WPA.
- `session_save_thread()`: Guarda la sesión de la prueba en un archivo.
- `clean_exit()`: Cierra el programa de forma adecuada.

### 4. Dependencias Internas

```cpp
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
```

### 5. Diagrama de Interdependencias

```mermaid
graph TD
    A[main()] -->|"llama a"| B[get_first_target()]
    B -->|"llama a"| C[c_avl_insert()]
    C -->|"llama a"| D[c_avl_size()]
    A -->|"llama a"| E[perform_wep_crack()]
    A -->|"llama a"| F[perform_wpa_crack()]
    A -->|"llama a"| G[session_save_thread()]
    A -->|"llama a"| H[clean_exit()]
```

Esto es una representación simplificada del diagrama de interdependencias del módulo. El diagrama en sí, debe seguir las reglas de sintaxis de Mermaid proporcionadas.