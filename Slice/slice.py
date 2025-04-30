import math
import multiprocessing
import time
import os
import zipfile
from datetime import datetime

# Crear las carpetas necesarias si no existen
def setup_folders():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("logs_zipped"):
        os.makedirs("logs_zipped")

# Guardar el log del progreso de una partición
def save_partition_log(partition_id, blocks_completed, elapsed_time):
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"logs/partition_{partition_id}_{fecha}.txt"
    with open(log_filename, "w") as f:
        f.write(f"Partition: {partition_id}\n")
        f.write(f"Fecha: {fecha}\n")
        f.write(f"Bloques completados: {blocks_completed}\n")
        f.write(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos\n")
    return log_filename

# Empaquetar los logs en un archivo ZIP y limpiar los archivos originales
def package_and_cleanup_logs():
    zip_filename = f"logs_zipped/logs_package_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("logs"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "logs")
                zipf.write(file_path, arcname)
    # Limpiar archivos de texto después de empaquetar
    for file in os.listdir("logs"):
        os.remove(os.path.join("logs", file))
    print(f"[INFO] Logs empaquetados y limpiados: {zip_filename}")

# Función de predicción de números primos (sin cambios)
def is_prime_frequency(X: int) -> bool:
    if X < 2:
        return False
    if X in (2, 3):
        return True
    if X % 2 == 0 or X % 3 == 0:
        return False
    if X % 5 == 0 or X % 7 == 0:
        return False
    if X % 6 == 1:
        cX = (X - 4) // 3
    else:
        cX = (X - 5) // 3
    limit = math.isqrt(X)
    c = 0
    while True:
        a_c = 3 * c + (5 if c % 2 == 0 else 4)
        if a_c > limit:
            break
        if c == cX:
            c += 1
            continue
        f2 = 2 * c + 3
        f1 = 4 * c + (7 if c % 2 == 0 else 5)
        total = f1 + f2
        valA = cX - c - f1
        if valA >= 0 and valA % total == 0:
            return False
        valB = cX - c - total
        if valB >= 0 and valB % total == 0:
            return False
        c += 1
    return True

# Procesar un bloque de trabajo
def process_block(number: int, start_c: int, end_c: int, cX: int, limit: int) -> bool:
    c = start_c
    while c <= end_c:
        a_c = 3 * c + (5 if c % 2 == 0 else 4)
        if a_c > limit:
            break
        if c == cX:
            c += 1
            continue
        f2 = 2 * c + 3
        f1 = 4 * c + (7 if c % 2 == 0 else 5)
        total = f1 + f2
        valA = cX - c - f1
        if valA >= 0 and valA % total == 0:
            return False
        valB = cX - c - total
        if valB >= 0 and valB % total == 0:
            return False
        c += 1
    return True

# Reemplazo seguro con reintentos
def safe_replace(tmp_file, final_file, retries=5, delay=0.1):
    for i in range(retries):
        try:
            os.replace(tmp_file, final_file)
            return
        except PermissionError as e:
            if i == retries - 1:
                raise e
            time.sleep(delay)

# Función para obtener el tamaño recomendado del bloque
def get_recommended_block_size(number):
    min_block_size = 100
    max_block_size = 1000000

    if number < 1000:
        recommended_block_size = min_block_size
    else:
        recommended_block_size = int(math.log(number, 10) * 10000)

    recommended_block_size = min(max_block_size, max(min_block_size, recommended_block_size))
    
    return recommended_block_size

# Código principal
if __name__ == '__main__':
    multiprocessing.freeze_support()
    setup_folders()

    try:
        number = eval(input("Ingresa el número a analizar (por ejemplo, 2**127 - 1): "))
        partitions = int(input("Ingresa el número de particiones (por ejemplo, 30): "))
        partition_id = int(input(f"Ingresa el ID de partición (0 a {partitions-1}): "))

        # Calcular tamaño recomendado de bloque
        recommended_block_size = get_recommended_block_size(number)
        print(f"El tamaño recomendado de bloque es: {recommended_block_size}")

        block_size = int(input(f"Ingresa el tamaño del bloque (puedes usar el recomendado {recommended_block_size}): "))
    except Exception as e:
        print(f"Entrada inválida: {e}")
        exit(1)

    progress_file = f"partition_{partition_id}_progress.txt"
    start_time = time.time()

    limit = math.isqrt(number)
    total_work = limit
    partition_work = total_work // partitions
    partition_start = partition_id * partition_work
    partition_end = partition_start + partition_work if partition_id != partitions - 1 else total_work

    total_blocks = (partition_end - partition_start) // block_size + 1
    current_block = 0

    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            lines = f.read().splitlines()
        try:
            saved_number = lines[0].split(":")[1].strip()
            saved_block_size = int(lines[1].split(":")[1].strip())
            saved_partitions = int(lines[2].split(":")[1].strip())
            last_completed_block = int(lines[3].split(":")[1].strip())

            if str(number) != saved_number or block_size != saved_block_size or partitions != saved_partitions:
                print("⚠️ ¡Se detectó un conflicto en el archivo de progreso! Aborting para evitar corrupción.")
                exit(1)

            current_block = last_completed_block + 1
        except Exception as e:
            print(f"⚠️ No se pudo analizar el archivo de progreso: {e}")
            exit(1)

    if number % 6 == 1:
        cX = (number - 4) // 3
    else:
        cX = (number - 5) // 3

    composite_found = False
    try:
        for block_num in range(current_block, total_blocks):
            block_start = partition_start + block_num * block_size
            block_end = min(block_start + block_size - 1, partition_end)

            print(f"Procesando Partición {partition_id}, Bloque {block_num+1}/{total_blocks}... ", end="")
            block_ok = process_block(number, block_start, block_end, cX, limit)

            if not block_ok:
                print("COMPUESTO ❌")
                composite_found = True
                with open(f"partition_{partition_id}_composite.txt", "w") as f:
                    f.write(f"Partición {partition_id} detectada como compuesta.")
                break  # Si se encuentra compuesto, terminamos el análisis

            print("Hasta ahora no es compuesto ✅")

            tmp_file = f"{progress_file}.tmp"
            with open(tmp_file, "w") as f:
                f.write(f"number: {number}\n")
                f.write(f"block_size: {block_size}\n")
                f.write(f"partitions: {partitions}\n")
                f.write(f"last_completed_block: {block_num}\n")

            safe_replace(tmp_file, progress_file)

    except KeyboardInterrupt:
        print("\n🛑 Interrupción detectada (Ctrl+C). Progreso guardado con éxito.")
        exit(0)

    elapsed = time.time() - start_time

    save_partition_log(partition_id, total_blocks, elapsed)

    if (partition_id + 1) % 100 == 0:
        package_and_cleanup_logs()

    # Mensaje final según el estado
    if composite_found:
        print(f"✅ ¡Partición {partition_id} COMPLETADA! Número COMPUESTO detectado.")
    else:
        print(f"✅ ¡Partición {partition_id} COMPLETADA con éxito! La primalidad depende del resultado de todos los bloques.")

    print(f"Tiempo total de ejecución: {elapsed:.2f} segundos")
