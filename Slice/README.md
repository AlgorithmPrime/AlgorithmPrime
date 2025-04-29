# 🧩 Slice — Distributed Prime Search using Cyclic Frequency Sieve

**Collaborative distributed search for very large primes using empirical cyclic frequency analysis.**

---

## 📚 Abstract

Slice is a Python-based distributed system to search for very large prime numbers.
It divides the primality test into partitions and internal blocks, allowing multiple machines or users to collaborate manually.

The method uses the empirical Sieve of Cyclic Frequencies, providing a novel and deterministic way to analyze large numbers without traditional divisibility tests.

---

## 🚀 How It Works

- The number is divided into **N partitions**.
- Each partition is subdivided into **blocks**.
- Each block checks a portion of primality conditions using cyclic frequencies.
- Progress is saved automatically after each block.
- If a block detects compositeness, the process stops and a composite result file is created.
- If interrupted (power outage, shutdown), Slice resumes from the last saved block.

---

## 🛠 Usage Instructions

```bash
python slice.py
```

You will be asked:

- Number to analyze (e.g., `2**127-1`)
- Number of partitions (e.g., `30`)
- Partition ID to process (e.g., `0` to `29`)
- Block size (e.g., `100000`)

Example:

```bash
python slice.py
Enter the number to analyze (e.g., 2**127-1): 2**89-1
Enter number of partitions (e.g., 30): 4
Enter partition ID (0 to 3): 0
Enter block size (e.g., 100000): 100000
```

---

## 🖥️ Parallel Processing (Multiprocessing Manual)

- Slice supports **manual parallelism**: run multiple partitions at once, each in a separate terminal window.
- Example with a 4-core CPU:
    - Terminal 1: `partition 0`
    - Terminal 2: `partition 1`
    - Terminal 3: `partition 2`
    - Terminal 4: `partition 3`

Each partition uses one CPU core independently.

The program displays your available cores automatically:
```text
🖥️ You have 8 CPU cores available.
ℹ️ You can run up to 8 processes at the same time for best performance.
```

---

## 💾 Progress and Recovery System

- Progress is saved in a file named `partition_X_progress.txt`.
- If the program stops unexpectedly, Slice resumes from the last saved block.
- If a block detects compositeness, Slice immediately creates a file `partition_X_composite.txt` and stops the execution.

✅ This guarantees minimal loss in case of power outages.

---

## ⚡ What Happens If Power Loss Occurs?

- Already completed blocks are saved.
- The program resumes automatically at next start.
- If composite was detected before the crash, the file `partition_X_composite.txt` already exists to inform you.

✅ You will not lose important results.

---

## 📈 Notes on Speed Variation

- Some partitions may complete faster than others.
- Later partitions (near the limit) typically have less work to do.
- This is natural due to how divisibility density decreases with larger numbers.

✅ No action is needed — it is normal behavior.

---

## ❗ Important: "No composite detected" ≠ "Number is Prime"

- If a partition completes without finding a composite, it **only means no compositeness was detected in that partition**.
- You must complete all partitions to conclude anything about the number's primality.

---

## 📝 License

This project is licensed under the MIT License — free for anyone to use, modify, and distribute with credit to the original author.

---

## 👤 Credits

- Project Creator: Héctor Cárdenas Campos
- Year: 2025

---

---

# 🧩 Slice — Búsqueda Distribuida de Primos usando Criba de Frecuencias Cíclicas

**Búsqueda colaborativa distribuida de números primos gigantes usando análisis empírico de frecuencias cíclicas.**

---

## 📚 Resumen

Slice es un sistema distribuido en Python para buscar números primos extremadamente grandes.
Divide la prueba de primalidad en particiones y bloques internos, permitiendo colaboración manual entre múltiples computadoras.

El método utiliza la Criba Empírica de Frecuencias Cíclicas, ofreciendo un enfoque original y determinista para analizar números grandes sin pruebas clásicas de divisibilidad.

---

## 🚀 Cómo Funciona

- El número se divide en **N particiones**.
- Cada partición se subdivide en **bloques**.
- Cada bloque analiza una parte de las condiciones de primalidad usando frecuencias cíclicas.
- El progreso se guarda automáticamente tras cada bloque.
- Si se detecta un compuesto, se crea un archivo de resultado y se detiene la ejecución.
- Si hay una interrupción, Slice reanuda desde el último bloque guardado.

---

## 🛠 Instrucciones de Uso

```bash
python slice.py
```

Se solicitará:

- Número a analizar (ej.: `2**127-1`)
- Número de particiones (ej.: `30`)
- ID de partición (ej.: `0` a `29`)
- Tamaño de bloque (ej.: `100000`)

Ejemplo:

```bash
python slice.py
Introduce el número a analizar: 2**89-1
Introduce el número de particiones: 4
Introduce el ID de partición (0 a 3): 0
Introduce el tamaño de bloque: 100000
```

---

## 🖥️ Procesamiento Paralelo (Multiproceso Manual)

- Slice permite paralelismo manual ejecutando múltiples particiones simultáneamente, cada una en una ventana de terminal distinta.
- Ejemplo con CPU de 4 núcleos:
    - Terminal 1: `partition 0`
    - Terminal 2: `partition 1`
    - Terminal 3: `partition 2`
    - Terminal 4: `partition 3`

✅ Cada partición usa un núcleo independiente.

---

## 💾 Sistema de Progreso y Recuperación

- El progreso se guarda en un archivo llamado `partition_X_progress.txt`.
- Slice reanuda desde el último bloque en caso de apagón.
- Si se detecta compuesto, se crea `partition_X_composite.txt` automáticamente.

---

## ⚡ ¿Qué pasa si se va la luz?

- Los bloques completados ya estarán guardados.
- Al reiniciar, Slice continuará desde donde se quedó.
- Si un compuesto fue detectado, ya existirá el archivo correspondiente.

---

## 📈 Notas sobre la Variabilidad de Velocidad

- Algunas particiones pueden terminar más rápido que otras.
- Particiones cercanas al límite suelen requerir menos trabajo.
- Esto es completamente normal.

---

## ❗ Importante: "No se detectó compuesto" ≠ "El número es primo"

- Si una partición termina sin encontrar un compuesto, **solo indica que en esa partición no se detectó compositeness**.
- Todas las particiones deben completarse para sacar conclusiones.

---

## 📝 Licencia

Proyecto licenciado bajo MIT — uso libre, siempre dando crédito al autor original.

---

## 👤 Créditos

- Creador del Proyecto: Héctor Cárdenas Campos
- Año: 2025

---