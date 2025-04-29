# Script: slice.py
# Description: Distributed prime search using cyclic frequency sieve (with safe progress validation)
# Author: Héctor Cárdenas Campos + Assistance

import math
import multiprocessing
import time
import os

# Display number of CPU cores
cpu_count = multiprocessing.cpu_count()
print(f"🖥️ You have {cpu_count} CPU cores available.")
print(f"ℹ️ You can run up to {cpu_count} processes at the same time for best performance.\n")

# Prime prediction function
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

# Check a block of work
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

if __name__ == '__main__':
    multiprocessing.freeze_support()

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

    # Default start block
    current_block = 0

    # Check existing progress and verify data
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
                print(f"Progress file: number={saved_number}, block_size={saved_block_size}, partitions={saved_partitions}")
                print(f"Current input: number={number}, block_size={block_size}, partitions={partitions}")
                exit(1)

            current_block = last_completed_block + 1
        except Exception as e:
            print(f"⚠️ Could not parse progress file: {e}")
            exit(1)

    # Precompute cX
    if number % 6 == 1:
        cX = (number - 4) // 3
    else:
        cX = (number - 5) // 3

    # Start processing
    for block_num in range(current_block, total_blocks):
        block_start = partition_start + block_num * block_size
        block_end = min(block_start + block_size - 1, partition_end)

        print(f"Processing Partition {partition_id}, Block {block_num+1}/{total_blocks}... ", end="")
        block_ok = process_block(number, block_start, block_end, cX, limit)

        if not block_ok:
            print("FAIL ❌")
            print(f"❌ {number} is composite based on block {block_num+1}.")
            with open(f"partition_{partition_id}_composite.txt", "w") as f:
                f.write(f"Partition {partition_id} detected as composite.")
            exit(0)

        print("So far not composite ✅")

        # Save progress with verification data
        with open(progress_file, "w") as f:
            f.write(f"number: {number}\n")
            f.write(f"block_size: {block_size}\n")
            f.write(f"partitions: {partitions}\n")
            f.write(f"last_completed_block: {block_num}\n")

    # After all blocks are processed
    print("🎉 All blocks processed successfully. Partition completed with NO errors detected.")
    elapsed = time.time() - start_time
    print(f"✅ Partition {partition_id} COMPLETED successfully!")
    print(f"Total execution time: {elapsed:.2f} seconds")