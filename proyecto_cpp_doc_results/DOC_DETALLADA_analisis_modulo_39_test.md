## 📋 Documentación Técnica

### 1. Propósito y Responsabilidad
Este módulo tiene la responsabilidad de capturar y procesar paquetes de red entrantes para detectar y responder a los mensajes de eco.

### 2. Código Comentado (con explicación de funciones y parámetros)

```cpp
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/icmp.h>

int main() {
    // Abre el dispositivo de red
    pcap_t *handle = pcap_open_live("eth0", BUFSIZ, 1, 1000, NULL);
    if (handle == NULL) {
        fprintf(stderr, "Error al abrir el dispositivo de red\n");
        return 1;
    }

    // Compila el filtro para capturar paquetes ICMP
    const char *filter = "icmp";
    struct bpf_program fp;
    if (pcap_compile(handle, &fp, filter, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Error al compilar el filtro\n");
        pcap_close(handle);
        return 1;
    }

    if (pcap_setfilter(handle, &fp) == -1) {
        fprintf(stderr, "Error al establecer el filtro\n");
        pcap_close(handle);
        return 1;
    }

    // Ejecuta el bucle de captura de paquetes
    pcap_loop(handle, -1, receive_packet, NULL);

    // Cierra el dispositivo de red
    pcap_close(handle);

    return 0;
}

void receive_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    // Verifica si el paquete es un mensaje de eco
    if (packet[20] == 8) { // ICMP type 8 is Echo Request
        // Responde al mensaje de eco
        reply_icmp_echo(packet, header->len);
    }
}

void reply_icmp_echo(const u_char *packet, int len) {
    // Crea y envía un paquete de respuesta ICMP
    struct ip *ip_header = (struct ip *)(packet + 14);
    struct icmp *icmp_header = (struct icmp *)(packet + 14 + ip_header->ihl * 4);

    // Crea un nuevo paquete ICMP de respuesta
    struct icmp *icmp_reply = (struct icmp *)(malloc(sizeof(struct icmp) + len - 28));
    icmp_reply->icmp_type = 0; // ICMP type 0 is Echo Reply
    icmp_reply->icmp_code = 0;
    icmp_reply->icmp_cksum = 0;
    icmp_reply->icmp_id = icmp_header->icmp_id;
    icmp_reply->icmp_seq = icmp_header->icmp_seq + 1;

    // Calcula el checksum
    icmp_reply->icmp_cksum = checksum(icmp_reply, len - 28);

    // Copia los datos del paquete de origen al paquete de respuesta
    memcpy(icmp_reply + 1, packet + 14, len - 14);

    // Envía el paquete de respuesta
    pcap_sendpacket(handle, (const u_char *)icmp_reply, len);
}

// Función para calcular el checksum de un paquete ICMP
uint16_t checksum(void *data, int len) {
    uint32_t sum = 0;
    uint16_t *ptr = (uint16_t *)data;
    while (len > 1) {
        sum += *ptr++;
        len -= 2;
    }
    if (len == 1) {
        sum += *(uint8_t *)ptr;
    }
    sum = (sum >> 16) + (sum & 0xffff);
    sum = ~sum & 0xffff;
    return sum;
}
```

### 3. Interfaz Pública

El módulo es un programa en línea de comandos que utiliza la biblioteca pcap para capturar paquetes de red. El programa utiliza una función principal llamada `main` que abre el dispositivo de red, compila y aplica el filtro para capturar paquetes ICMP, y ejecuta el bucle de captura de paquetes. También tiene dos funciones principales: `receive_packet` y `reply_icmp_echo`. `receive_packet` es llamada por `pcap_loop` para cada paquete capturado. Verifica si el paquete es un mensaje de eco y, en caso afirmativo, responde al mismo. `reply_icmp_echo` crea y envía un paquete de respuesta ICMP.

### 4. Dependencias Internas

El módulo depende de la biblioteca pcap para capturar paquetes de red y de la biblioteca netinet para manipular encabezados de red.

### 5. Diagrama de Interdependencias

```mermaid
graph TD
    A[Main Module (v1.0)] -->|llama a| B[libpcap]
    A -->|llama a| C[libnetinet]
```