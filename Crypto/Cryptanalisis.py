import math

def explore_frequencies(X):
    """Explora frecuencias cíclicas para X en la forma 6n ± 1, deteniéndose en la primera colisión."""
    if X % 3 not in [1, 2]:
        print(f"{X} no está en la forma 6n ± 1.")
        return [], [], [], False
    c_target = (X - 4) // 3 if X % 3 == 1 else (X - 5) // 3
    limit = math.isqrt(X)
    c_values = []
    f3_values = []
    collisions = []
    is_prime = True
    for c in range(limit + 1):
        f3 = 3 * c + (5 if c % 2 == 0 else 4)
        if f3 > limit:
            break
        c_values.append(c)
        f3_values.append(f3)
        if c == c_target:
            continue
        f1 = 4 * c + (7 if c % 2 == 0 else 5)
        f2 = 2 * c + 3
        total = f1 + f2
        valA = c_target - c - f1
        valB = c_target - c - total
        if valA >= 0 and valA % total == 0:
            print(f"Colisión en c={c}: f3(c)={f3}, k={valA // total}")
            collisions.append((c, f3))
            is_prime = False
            break  # Detenerse en la primera colisión
        if valB >= 0 and valB % total == 0:
            print(f"Colisión en c={c}: f3(c)={f3}, k={valB // total}")
            collisions.append((c, f3))
            is_prime = False
            break  # Detenerse en la primera colisión
    print(f"{X} es {'primo' if is_prime else 'compuesto'}.")
    return c_values, f3_values, collisions, is_prime

# Preguntar al usuario por un número
try:
    X = int(input("Ingresa un número X para analizar (forma 6n±1): "))
    c_values, f3_values, collisions, is_prime = explore_frequencies(X)
    if collisions:
        factor = collisions[0][1]  # f3(c) de la primera colisión
        other_factor = X // factor
        print(f"Factores encontrados: {factor} y {other_factor}")
    elif is_prime:
        print(f"{X} es primo.")
    else:
        print("No se encontraron factores dentro del límite.")
except ValueError:
    print("Por favor, ingresa un número entero válido.")