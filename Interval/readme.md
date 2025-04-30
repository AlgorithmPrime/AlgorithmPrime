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


These files are under experimental development and are part of the ongoing validation process of the predictive approach within the sieve model.
