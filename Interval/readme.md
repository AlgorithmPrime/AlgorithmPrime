# Criba Empírica de Frecuencias Cíclicas

Este repositorio contiene dos implementaciones del modelo de **criba empírica de frecuencias cíclicas** desarrollado para la detección de números primos:

- **`interval.py`**: Script optimizado con procesamiento multi-core, diseñado para ejecución local en equipos con Python instalado. Procesa intervalos grandes dividiéndolos en bloques y utilizando multiprocessing. No es compatible con Google Colab.
- **`interval_colab.ipynb`**: Versión adaptada para ejecución interactiva en Google Colaboratory. Procesa los intervalos bloque por bloque, sin multiprocessing. Funciona también en entornos locales como Jupyter Notebook.

## Cómo usar

- **Ejecución local**:
  - Ejecutar `interval.py` desde una terminal o entorno de Python instalado localmente.
  - Requiere Python 3.8 o superior y el módulo estándar `multiprocessing`.

- **Ejecución en Google Colaboratory o Jupyter**:
  - Abrir `interval_colab.ipynb` directamente en Google Colab o en un entorno Jupyter.
  - No se requiere instalación de paquetes adicionales. Recomendado para quienes prefieran trabajar en línea sin necesidad de instalaciones locales.

## Sobre el método

Ambos scripts utilizan una criba basada en patrones cíclicos de frecuencias asociados a números de la forma \(6N \pm 1\), detectando números primos mediante un análisis de colisiones predictivas.

## Autor

Héctor Cárdenas Campos

Estos archivos están en desarrollo experimental y forman parte del proceso de validación del enfoque predictivo dentro de la criba.

---

# Empirical Sieve of Cyclic Frequencies

This repository contains two implementations of the **empirical sieve of cyclic frequencies** model developed for prime number detection:

- **`interval.py`**: Optimized script with multi-core processing, designed for local execution on systems with Python installed. It processes large intervals by dividing them into blocks and using multiprocessing. It is not compatible with Google Colab.
- **`interval_colab.ipynb`**: Adapted version for interactive execution in Google Colaboratory. It processes intervals block by block without multiprocessing. It also works in local environments such as Jupyter Notebook.

## How to Use

- **Local execution**:
  - Run `interval.py` from a terminal or a locally installed Python environment.
  - Requires Python 3.8 or higher and the standard `multiprocessing` module.

- **Execution in Google Colaboratory or Jupyter**:
  - Open `interval_colab.ipynb` directly in Google Colab or a Jupyter environment.
  - No additional packages are required. Recommended for users who prefer to work online without local installations.

## About the Method

Both scripts use a sieve based on cyclic frequency patterns associated with numbers of the form \(6N \pm 1\), detecting prime numbers through predictive collision analysis.

## Author

Héctor Cárdenas Campos

These files are under experimental development and are part of the ongoing validation process of the predictive approach within the sieve model.
