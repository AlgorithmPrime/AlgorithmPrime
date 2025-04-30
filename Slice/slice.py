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
        f.write(f"Tiempo total de ejecucion: {elapsed_time:.2f} segundos\n")
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

# Código principal
if __name__ == '__main__':
    multiprocessing.freeze_support()
    setup_folders()

    try:
        number = eval(input("Enter the number to analyze (e.g., 2**127 - 1): "))
        partitions = int(input("Enter number of partitions (e.g., 30): "))
        partition_id = int(input(f"Enter partition ID (0 to {partitions-1}): "))
        block_size = int(input("Enter block size (e.g., 1000000): "))
    except Exception as e:
        print(f"Invalid input: {e}")
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
                print("⚠️ Progress file mismatch detected! Aborting to prevent corruption.")
                exit(1)

            current_block = last_completed_block + 1
        except Exception as e:
            print(f"⚠️ Could not parse progress file: {e}")
            exit(1)

    if number % 6 == 1:
        cX = (number - 4) // 3
    else:
        cX = (number - 5) // 3

    # Iniciar el procesamiento de bloques
    try:
        for block_num in range(current_block, total_blocks):
            block_start = partition_start + block_num * block_size
            block_end = min(block_start + block_size - 1, partition_end)

            print(f"Processing Partition {partition_id}, Block {block_num+1}/{total_blocks}... ", end="")
            block_ok = process_block(number, block_start, block_end, cX, limit)

            if not block_ok:
                print("FAIL ❌")
                with open(f"partition_{partition_id}_composite.txt", "w") as f:
                    f.write(f"Partition {partition_id} detected as composite.")
                exit(0)

            print("So far not composite ✅")

            # Guardar progreso de forma segura
            tmp_file = f"{progress_file}.tmp"
            with open(tmp_file, "w") as f:
                f.write(f"number: {number}\n")
                f.write(f"block_size: {block_size}\n")
                f.write(f"partitions: {partitions}\n")
                f.write(f"last_completed_block: {block_num}\n")

            # Reemplazo seguro con reintento
            safe_replace(tmp_file, progress_file)

    except KeyboardInterrupt:
        print("\n🛑 Interrupción detectada (Ctrl+C). Progreso guardado con éxito.")
        exit(0)

    elapsed = time.time() - start_time

    # Guardar log de la partición
    save_partition_log(partition_id, total_blocks, elapsed)

    # Después de cada 100 particiones, empaquetar y limpiar logs
    if (partition_id + 1) % 100 == 0:
        package_and_cleanup_logs()

    print(f"✅ Partition {partition_id} COMPLETED successfully!")
    print(f"Total execution time: {elapsed:.2f} seconds")
