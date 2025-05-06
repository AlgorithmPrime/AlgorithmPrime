# ryptanalysis Educational Script

This Python script demonstrates an **experimental approach to integer factorization**, mimicking how a basic cryptanalysis program might attempt to break RSA-style keys. The method relies on structural analysis of numbers of the form `6n ± 1`, inspired by observed patterns in the distribution of prime numbers.

> **Disclaimer:** This tool is intended solely for **educational purposes**. It is not optimized for real cryptographic attacks and should not be used for malicious or production-level purposes.

---

## About

RSA encryption relies on the mathematical difficulty of factoring large semiprime numbers — that is, numbers composed of **exactly two large prime factors**. This script attempts to **recover the prime factors of a given number** `N = p × q` by analyzing frequency-like patterns and exploring numeric relationships in candidates of the form `6n ± 1`.

---

## Intended Use

- Designed to **factor numbers of the form** `N = p × q`, where `p` and `q` are both **prime**.
- Ideal for **semiprimes** ranging from ~10 to ~18 digits.
- It is not guaranteed to work correctly on:
  - Very large numbers (over ~10¹⁸).
  - Numbers with more than two prime factors (e.g. 231, 455, 1001).
  - Prime numbers or perfect powers.

---

## Known Limitations

- **Not suitable for general composite numbers**. The algorithm may return incomplete or misleading results if the number has more than two distinct prime factors.
- May crash with a `MemoryError` if input is too large, due to internal dictionary growth.
- For learning purposes only. The approach is not efficient compared to modern factorization methods.

---

## Performance Notice

- This script is **single-threaded** and not memory-optimized.
- Inputs larger than ~18 digits may lead to **very long execution times** or memory exhaustion.
- On high-performance systems with more RAM and CPU power, the script may handle larger numbers better.

---

## Example Inputs

### Valid RSA-style semiprimes:
| `p` | `q` | `N = p × q` |
|-----|-----|-------------|
| 10007 | 10009 | 100160063 |
| 99999997 | 99999989 | 9999998600000013 |
| 32416190071 | 32416187567 | 1050809297549059047257 |

### Invalid (will fail or misbehave):
- `231` (3 × 7 × 11)
- `455` (5 × 7 × 13)
- `1001` (7 × 11 × 13)

---

## Usage

Run the script using Python 3:

```bash
python cryptanalisis.py


