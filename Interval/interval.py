# Script: interval.py
# Description: Prime detection using empirical cyclic frequency sieve (block-based, multi-core, optional save)
# Author: Héctor Cárdenas Campos

import math
import multiprocessing
import time

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

def process_block(block_start: int, block_end: int) -> list[int]:
    primes = []
    for num in range(block_start, block_end + 1):
        if num < 2:
            continue
        if num in (2, 3):
            primes.append(num)
            continue
        if num % 2 == 0 or num % 3 == 0:
            continue
        if is_prime_frequency(num):
            primes.append(num)
    return primes

if __name__ == '__main__':
    multiprocessing.freeze_support()
    try:
        start_range = eval(input("Enter starting number (you may use expressions like 2**10): "))
        end_range = eval(input("Enter ending number (e.g. 2**10 + 100): "))
        block_size = int(input("Enter block size (e.g. 1000): "))
    except Exception as e:
        print(f"Invalid input: {e}")
        exit(1)

    tasks = []
    for block_start in range(start_range, end_range + 1, block_size):
        block_end = min(block_start + block_size - 1, end_range)
        tasks.append((block_start, block_end))

    start_time = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.starmap(process_block, tasks)

    all_primes = [p for sublist in results for p in sublist]
    all_primes.sort()

    elapsed = time.time() - start_time
    print(f"\nTotal execution time: {elapsed:.2f} seconds")
    print(f"Number of primes found: {len(all_primes)}")

    if all_primes:
        print("\n✅ List of all primes found:")
        for prime in all_primes:
            print(prime)

    # Preguntar si desea guardar los resultados
    save = input("\nDo you want to save the list to 'primes_found.txt'? (y/n): ").lower()
    if save == 'y':
        try:
            with open("primes_found.txt", "w") as f:
                f.write(f"Total primes found: {len(all_primes)}\n\n")  # Escribe primero el total
                for p in all_primes:
                    f.write(f"{p}\n")  # Luego cada primo en una nueva línea
            print("📁 File saved as 'primes_found.txt'")
        except Exception as e:
            print(f"⚠️ Could not save file: {e}")
