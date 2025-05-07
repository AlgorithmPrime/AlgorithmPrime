import time

def explore_frequencies(X):
    from math import isqrt

    if X % 3 not in [1, 2]:
        return [], [], [], False

    freq1 = {}
    freq2 = {}
    freq3 = {}
    collisions = []

    for n in range(1, isqrt(X) + 1):
        f1 = 6 * n - 1
        if X % f1 == 0:
            collisions.append(('f1', f1))
            break

        f2 = 6 * n + 1
        if X % f2 == 0:
            collisions.append(('f2', f2))
            break

        f3 = 6 * n + 5
        if X % f3 == 0:
            collisions.append(('f3', f3))
            break

        freq1[n] = f1
        freq2[n] = f2
        freq3[n] = f3

    is_prime = len(collisions) == 0
    return freq1, freq2, collisions, is_prime


def factorize_fully(X):
    print("\nAnalyzing number:", X)
    start_time = time.time()

    factors = []
    remaining = X

    while True:
        _, _, collisions, is_prime = explore_frequencies(remaining)
        if is_prime:
            factors.append(remaining)
            break
        elif collisions:
            f = collisions[0][1]
            factors.append(f)
            remaining //= f
        else:
            break

    elapsed = time.time() - start_time
    print(f"⏱️ Time taken: {elapsed:.4f} seconds")
    print(f"🧩 Prime factors found: {' × '.join(map(str, factors))}")

    if len(factors) > 2:
        print("\n⚠️ Warning: More than two prime factors found.")
        print("This script is intended for numbers of the form N = p × q (RSA-style semiprimes).")
    elif len(factors) == 2:
        print("✅ Likely RSA semiprime structure.")
    else:
        print("❌ Could not factor completely or input is already prime.")


if __name__ == "__main__":
    print("🔐 Educational Cryptanalysis Script")
    print("Designed to factor numbers of the form N = p × q, as used in RSA.")
    print("⚠️ Inputting numbers with more than two prime factors may produce incorrect or unexpected results.\n")

    try:
        X = int(input("Enter a number to analyze: "))
        factorize_fully(X)
    except ValueError:
        print("❌ Invalid input. Please enter an integer.")
