# Slice — Distributed Prime Search using Cyclic Frequency Sieve

**Collaborative distributed search for very large primes using empirical cyclic frequency analysis.**

---

#Abstract

Slice is a Python-based distributed system to search for very large prime numbers.
It divides the primality test into partitions and internal blocks, allowing multiple machines or users to collaborate manually.

The method uses the empirical Sieve of Cyclic Frequencies, providing a novel and deterministic way to analyze large numbers without traditional divisibility tests.

---

#How It Works

- The number is divided into **N partitions**.
- Each partition is subdivided into **blocks**.
- Each block checks a portion of primality conditions using cyclic frequencies.
- Progress is saved automatically after each block.
- If a block detects compositeness, the process stops and a composite result file is created.
- If interrupted (power outage, shutdown), Slice resumes from the last saved block.

---

#Usage Instructions

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

# Parallel Processing (Multiprocessing Manual)

- Slice supports **manual parallelism**: run multiple partitions at once, each in a separate terminal window.
- Example with a 4-core CPU:
    - Terminal 1: `partition 0`
    - Terminal 2: `partition 1`
    - Terminal 3: `partition 2`
    - Terminal 4: `partition 3`

Each partition uses one CPU core independently.

The program displays your available cores automatically:
```text
You have 8 CPU cores available.
You can run up to 8 processes at the same time for best performance.
```

# Important: "No composite detected" ≠ "Number is Prime"

- If a partition completes without finding a composite, it **only means no compositeness was detected in that partition**.
- You must complete all partitions to conclude anything about the number's primality.
