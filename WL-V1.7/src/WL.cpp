//============================================================================
// Name        : WL_UltraLoader.cpp
// Description : Carga en 2 fases: Archivo -> PW_temp (512MB/100k lotes) -> PW (con validación y fallback a PW_errors)
// Compilar    : g++ -O3 -std=c++17 WL_UltraLoader.cpp -lpq -o wl_ultra_loader
//============================================================================

#include <iostream>
#include <chrono>
#include <iomanip>
#include <vector>
#include <string>
#include <cstring>      // Para memchr
#include <fcntl.h>      // Para open()
#include <unistd.h>     // Para read(), close()
#include <sys/stat.h>   // Para stat()
#include <libpq-fe.h>
#include <cstdlib> // Para exit()

// ============================================================================
// FUNCIONES AUXILIARES
// ============================================================================

// Sanitización agresiva en memoria (modifica el string in-place para máxima velocidad)
void sanitize_line(std::string& line) {
    for (char& c : line) {
        unsigned char uc = (unsigned char)c;
        if (uc == '\0') {
            c = ' '; // Reemplazar nulos por espacio
        } else if (uc >= 0xF5 || uc == 0xFE || uc == 0xFF) {
            c = '?'; // Reemplazar bytes UTF-8 inválidos
        }
    }
}

// Sanitización agresiva: reemplaza cualquier byte < 0x20 (incluido \0) o >= 0xF5 por espacio
void aggressive_sanitize(std::string& str) {
    for (char& c : str) {
        unsigned char uc = (unsigned char)c;
        if (uc < 0x20) c = ' ';          // Caracteres de control (incluye \0, \r, \t)
        else if (uc == 0x7F) c = ' ';    // DEL
        else if (uc >= 0xF5) c = ' ';    // Bytes UTF-8 inválidos
    }
}

#include <iostream>
#include <string>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <libpq-fe.h>

// ============================================================================
// FASE 1: CARGA DEL ARCHIVO A PW_TEMP (Optimizada para HDD 5400 RPM)
// ============================================================================
void load_file_to_temp(PGconn* conn, const std::string& input_file) {
    std::cout << "\n--- FASE 1: Leyendo archivo y cargando en PW_temp ---\n";

    int fd = open(input_file.c_str(), O_RDONLY);
    if (fd == -1) {
        std::cerr << "[ERROR] Fallo al abrir archivo: " << input_file << std::endl;
        PQfinish(conn);
        exit(1);
    }

    struct stat st;
    if (fstat(fd, &st) == -1) {
        std::cerr << "[ERROR] Fallo al obtener el tamaño del archivo." << std::endl;
        close(fd);
        PQfinish(conn);
        exit(1);
    }

    uint64_t file_size = st.st_size;
    std::cout << "Tamaño del archivo: " << (file_size / (1024.0 * 1024.0 * 1024.0)) << " GB\n";

    // Desactivar validación estricta de UTF-8
    PQexec(conn, "SET client_encoding = 'SQL_ASCII'");

    const size_t READ_BUF_SIZE = 512 * 1024 * 1024; // 512 MB
    const uint64_t BATCH_LINES = 20000;             // ¡CLAVE! Lotes pequeños para HDD

    std::vector<char> read_buf(READ_BUF_SIZE);
    std::vector<std::string> line_buffer;
    line_buffer.reserve(BATCH_LINES);

    std::string leftover;
    std::string current_line;
    current_line.reserve(256);

    uint64_t total_lines_processed = 0;
    uint64_t total_bytes_read = 0;
    uint64_t batch_count = 0;
    uint64_t null_bytes_found = 0;

    auto start_time = std::chrono::high_resolution_clock::now();

    ssize_t bytes_read;
    while ((bytes_read = read(fd, read_buf.data(), READ_BUF_SIZE)) > 0) {
        total_bytes_read += bytes_read;
        size_t start = 0;

        if (!leftover.empty()) {
            char* first_nl = (char*)memchr(read_buf.data(), '\n', bytes_read);
            if (first_nl) {
                size_t len = first_nl - read_buf.data();
                current_line = leftover + std::string(read_buf.data(), len);
                start = len + 1;
                leftover.clear();
            } else {
                leftover.append(read_buf.data(), bytes_read);
                continue;
            }
        }

        while (start < (size_t)bytes_read) {
            char* next_nl = (char*)memchr(read_buf.data() + start, '\n', bytes_read - start);

            if (next_nl) {
                size_t len = next_nl - (read_buf.data() + start);
                current_line.assign(read_buf.data() + start, len);
                start += len + 1;

                // Sanitización
                bool has_null = false;
                for (size_t i = 0; i < current_line.size(); ++i) {
                    unsigned char uc = (unsigned char)current_line[i];
                    if (uc == '\0') {
                        current_line[i] = ' ';
                        has_null = true;
                        null_bytes_found++;
                    } else if (uc < 0x20 && uc != '\n' && uc != '\r' && uc != '\t') {
                        current_line[i] = ' ';
                    } else if (uc == 0x7F || uc >= 0xF5) {
                        current_line[i] = '?';
                    }
                }

                line_buffer.push_back(std::move(current_line));
                total_lines_processed++;

                // === ESTRATEGIA HDD: Procesar y hacer COMMIT en cada lote pequeño ===
                if (line_buffer.size() >= BATCH_LINES) {
                    batch_count++;

                    // 1. BEGIN
                    PGresult* begin_res = PQexec(conn, "BEGIN");
                    PQclear(begin_res);

                    // 2. COPY
                    PGresult* copy_res = PQexec(conn, "COPY \"PW_temp\" (pw) FROM STDIN WITH (FORMAT csv, QUOTE E'\\x01')");
                    if (PQresultStatus(copy_res) == PGRES_COPY_IN) {
                        std::string batch_text;
                        size_t estimated = 0;
                        for (const auto& line : line_buffer) estimated += line.size() + 3;
                        batch_text.reserve(estimated);
                        for (const auto& line : line_buffer) batch_text += "\x01" + line + "\x01\n";

                        PQputCopyData(conn, batch_text.c_str(), static_cast<int>(batch_text.size()));
                        PQputCopyEnd(conn, NULL);

                        PGresult* res_end = PQgetResult(conn);
                        if (PQresultStatus(res_end) != PGRES_COMMAND_OK) {
                            std::cerr << "\n[ERROR CRÍTICO] Lote " << batch_count << " rechazado: " << PQerrorMessage(conn) << std::endl;
                            PQclear(res_end); PQexec(conn, "ROLLBACK"); close(fd); PQfinish(conn); exit(1);
                        }
                        PQclear(res_end);
                    } else {
                        std::cerr << "\n[ERROR] Fallo COPY: " << PQerrorMessage(conn) << std::endl;
                        PQclear(copy_res); PQexec(conn, "ROLLBACK"); close(fd); PQfinish(conn); exit(1);
                    }
                    PQclear(copy_res);

                    // 3. COMMIT (Esto libera la memoria y ordena el disco)
                    PGresult* commit_res = PQexec(conn, "COMMIT");
                    if (PQresultStatus(commit_res) != PGRES_COMMAND_OK) {
                        std::cerr << "\n[ERROR] Fallo COMMIT: " << PQerrorMessage(conn) << std::endl;
                        PQclear(commit_res); close(fd); PQfinish(conn); exit(1);
                    }
                    PQclear(commit_res);

                    line_buffer.clear();

                    // Progreso cada 50 lotes (1 millón de líneas)
                    if (batch_count % 50 == 0) {
                        auto now = std::chrono::high_resolution_clock::now();
                        double elapsed = std::chrono::duration<double>(now - start_time).count();
                        double mb = total_bytes_read / (1024.0 * 1024.0);
                        double speed = (elapsed > 0) ? (mb / elapsed) : 0.0;
                        double progress_pct = (total_bytes_read * 100.0) / file_size;
                        double remaining = file_size - total_bytes_read;
                        double eta = (speed > 0) ? (remaining / (speed * 1024.0 * 1024.0)) : 0.0;

                        int h = (int)(eta / 3600);
                        int m = (int)((eta - h * 3600) / 60);
                        int s = (int)(eta - h * 3600 - m * 60);

                        std::cout << "  -> Lotes: " << batch_count
                                  << " | Líneas: " << total_lines_processed
                                  << " | " << std::fixed << std::setprecision(1) << progress_pct << "%"
                                  << " | " << speed << " MB/s"
                                  << " | ETA: " << h << "h " << m << "m " << s << "s\n";
                    }
                }
            } else {
                leftover.assign(read_buf.data() + start, bytes_read - start);
                break;
            }
        }
    }

    // Procesar el último lote restante
    if (!leftover.empty()) {
        line_buffer.push_back(leftover);
        total_lines_processed++;
    }

    if (!line_buffer.empty()) {
        batch_count++;
        PGresult* begin_res = PQexec(conn, "BEGIN"); PQclear(begin_res);
        PGresult* copy_res = PQexec(conn, "COPY \"PW_temp\" (pw) FROM STDIN WITH (FORMAT csv, QUOTE E'\\x01')");
        if (PQresultStatus(copy_res) == PGRES_COPY_IN) {
            std::string batch_text;
            for (const auto& line : line_buffer) batch_text += "\x01" + line + "\x01\n";
            PQputCopyData(conn, batch_text.c_str(), static_cast<int>(batch_text.size()));
            PQputCopyEnd(conn, NULL);
            PQclear(PQgetResult(conn));
        }
        PQclear(copy_res);
        PGresult* commit_res = PQexec(conn, "COMMIT"); PQclear(commit_res);
    }

    close(fd);

    auto end_time = std::chrono::high_resolution_clock::now();
    double total_seconds = std::chrono::duration<double>(end_time - start_time).count();

    std::cout << "\n--- FASE 1 completada ---\n";
    std::cout << "Total líneas: " << total_lines_processed << "\n";
    std::cout << "Total lotes: " << batch_count << "\n";
    std::cout << "Tiempo: " << (int)total_seconds << " segundos\n";
}
// ============================================================================
// FASE 2: VALIDACIÓN Y TRANSFERENCIA DE PW_TEMP A PW
// ============================================================================
void transfer_and_validate(PGconn* conn) {
    std::cout << "\n--- FASE 2: Validando y transfiriendo de PW_temp a PW ---\n";

    // Usar transacción para atomicidad y velocidad
    PQexec(conn, "BEGIN");

    // Preparar sentencias para el fallback (mucho más rápido que construir SQL crudo)
    PQexec(conn, "PREPARE insert_pw AS INSERT INTO \"PW\" (pw) VALUES ($1) ON CONFLICT (pw) DO NOTHING");
    PQexec(conn, "PREPARE insert_error AS INSERT INTO \"PW_errors\" (line_number, error_type, raw_data, strategy) VALUES ($1, $2, $3, $4)");

    // Declarar cursor para leer PW_temp en lotes manejables
    PGresult* res = PQexec(conn, "DECLARE cur NO SCROLL CURSOR FOR SELECT line_number, pw FROM \"PW_temp\"");
    if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        std::cerr << "Error declarando cursor: " << PQerrorMessage(conn) << "\n";
        PQclear(res); PQexec(conn, "ROLLBACK"); return;
    }
    PQclear(res);

    uint64_t total_transferred = 0;
    uint64_t total_errors = 0;
    const int FETCH_SIZE = 10000;

    while (true) {
        std::string fetch_query = "FETCH " + std::to_string(FETCH_SIZE) + " FROM cur";
        res = PQexec(conn, fetch_query.c_str());
        int rows = PQntuples(res);

        if (rows == 0) {
            PQclear(res);
            break; // Fin del cursor
        }

        // Intento 1: Inserción masiva del lote (asumiendo que la mayoría estará limpia)
        std::string bulk_insert = "INSERT INTO \"PW\" (pw) VALUES ";
        for (int i = 0; i < rows; ++i) {
            // Escapar comillas simples manualmente para velocidad en el bulk
            std::string val = PQgetvalue(res, i, 1);
            size_t pos = 0;
            while ((pos = val.find("'", pos)) != std::string::npos) {
                val.replace(pos, 1, "''");
                pos += 2;
            }
            bulk_insert += "('" + val + "')";
            if (i < rows - 1) bulk_insert += ",";
        }
        bulk_insert += " ON CONFLICT (pw) DO NOTHING";

        PGresult* bulk_res = PQexec(conn, bulk_insert.c_str());
        if (PQresultStatus(bulk_res) == PGRES_COMMAND_OK) {
            total_transferred += rows;
            PQclear(bulk_res);
        } else {
            // Intento 2: Fallback fila por fila solo si el lote masivo falló
            std::cerr << "  [WARN] Lote masivo falló, aplicando fallback fila por fila...\n";
            PQclear(bulk_res);

            for (int i = 0; i < rows; ++i) {
                std::string line_num = PQgetvalue(res, i, 0);
                std::string pw_val = PQgetvalue(res, i, 1);

                // Usar la sentencia preparada para insertar en PW
                const char* param_vals[1] = { pw_val.c_str() };
                PGresult* row_res = PQexecPrepared(conn, "insert_pw", 1, param_vals, NULL, NULL, 0);

                if (PQresultStatus(row_res) != PGRES_COMMAND_OK) {
                    // Falló incluso a nivel de fila. Registrar en PW_errors
                    total_errors++;
                    std::string err_msg = PQerrorMessage(conn);
                    // Limpiar el mensaje de error para que no rompa el INSERT de log
                    size_t pos = 0;
                    while ((pos = err_msg.find("'", pos)) != std::string::npos) {
                        err_msg.replace(pos, 1, "''");
                        pos += 2;
                    }

                    const char* err_params[4] = { line_num.c_str(), "INSERT_CONSTRAINT_FAIL", pw_val.c_str(), err_msg.c_str() };
                    PGresult* log_res = PQexecPrepared(conn, "insert_error", 4, err_params, NULL, NULL, 0);
                    PQclear(log_res);
                } else {
                    total_transferred++;
                }
                PQclear(row_res);
            }
        }

        if (total_transferred % 100000 == 0) {
            std::cout << "  Progreso Fase 2: " << total_transferred << " transferidos | Errores: " << total_errors << "\n";
        }
    }

    // Confirmar transacción y limpiar
    PQexec(conn, "COMMIT");
    PQexec(conn, "DEALLOCATE insert_pw");
    PQexec(conn, "DEALLOCATE insert_error");
    PQexec(conn, "CLOSE cur");

    std::cout << "Fase 2 completada. Transferidos: " << total_transferred << " | Errores registrados: " << total_errors << "\n";
}

// ============================================================================
// FASE 3: LIMPIEZA
// ============================================================================
void cleanup_temp(PGconn* conn) {
    std::cout << "\n--- FASE 3: Limpiando tabla temporal ---\n";
    PGresult* res = PQexec(conn, "TRUNCATE TABLE \"PW_temp\"");
    if (PQresultStatus(res) == PGRES_COMMAND_OK) {
        std::cout << "PW_temp truncada correctamente.\n";
    } else {
        std::cerr << "[ADVERTENCIA] Fallo al truncar PW_temp: " << PQerrorMessage(conn) << "\n";
    }
    PQclear(res);
}

// ============================================================================
// MAIN
// ============================================================================
int main() {
    const std::string input_file = "/home/adri/CRC-Sessions/Diccionarios/wl.txt";
    const char* conninfo = "dbname=WL user=postgres password=postgres host=localhost port=5432";

    std::cout << "Conectando a PostgreSQL...\n";
    PGconn* conn = PQconnectdb(conninfo);
    if (PQstatus(conn) != CONNECTION_OK) {
        std::cerr << "Error de conexión: " << PQerrorMessage(conn) << std::endl;
        return 1;
    }

    auto total_start = std::chrono::high_resolution_clock::now();

    // Ejecutar las 3 fases
    load_file_to_temp(conn, input_file);
    transfer_and_validate(conn);
    cleanup_temp(conn);

    PQfinish(conn);

    auto total_end = std::chrono::high_resolution_clock::now();
    double total_time = std::chrono::duration<double>(total_end - total_start).count();

    std::cout << "\n===================================================\n";
    std::cout << "PROCESO COMPLETADO EXITOSAMENTE\n";
    std::cout << "Tiempo total: " << std::fixed << std::setprecision(2) << total_time << " segundos\n";
    std::cout << "===================================================\n";

    return 0;
}
