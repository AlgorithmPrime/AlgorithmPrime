import math
import matplotlib.pyplot as plt

def explore_frequencies(X):
    """Explora frecuencias cíclicas para X en la forma 6n ± 1, detectando colisiones."""
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
        if valB >= 0 and valB % total == 0:
            print(f"Colisión en c={c}: f3(c)={f3}, k={valB // total}")
            collisions.append((c, f3))
            is_prime = False
    print(f"{X} es {'primo' if is_prime else 'compuesto'}.")
    return c_values, f3_values, collisions, is_prime

def plot_frequencies(X, c_values, f3_values, collisions):
    """Genera un gráfico de f3(c) y colisiones con submuestreo dinámico y zoom."""
    plt.figure(figsize=(8, 6))
    
    # Dynamic subsampling: target ~10,000 points
    target_points = 10000
    step = max(1, len(c_values) // target_points)
    plt.plot(c_values[::step], f3_values[::step], 'b-', label='$f_3(c)$')
    
    # Plot collisions
    if collisions:
        x_vals, y_vals = zip(*collisions)
        plt.scatter(x_vals, y_vals, color='red', label='Colisiones')
        
        # Zoom to region containing collisions
        max_collision_c = max(x_vals)
        max_collision_f3 = max(y_vals)
        x_margin = max_collision_c * 0.1  # 10% margin
        y_margin = max_collision_f3 * 0.1
        plt.xlim(0, max_collision_c + x_margin)
        plt.ylim(0, max_collision_f3 + y_margin)
    
    plt.xlabel('Índice $c$')
    plt.ylabel('$f_3(c)$')
    plt.title(f'Frecuencias y Colisiones para $X={X}$')
    plt.legend(loc='upper left')  # Fixed legend location
    plt.grid(True)
    plt.savefig(f'f3_X{X}.png', dpi=300)
    plt.show()

# Preguntar al usuario por un número
try:
    X = int(input("Ingresa un número X para analizar (forma 6n±1): "))
    c_values, f3_values, collisions, is_prime = explore_frequencies(X)
    if c_values:  # solo continuar si el número es válido
        # Preguntar si desea generar el gráfico
        plot_choice = input("¿Desea generar y guardar el gráfico? (y/n): ").strip().lower()
        if plot_choice in ['y', 'yes']:
            plot_frequencies(X, c_values, f3_values, collisions)
        else:
            print("Gráfico no generado.")
except ValueError:
    print("Por favor, ingresa un número entero válido.")