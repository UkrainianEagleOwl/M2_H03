# Multithreaded Folder Sorter and Factorization Package

## Overview
This package combines two powerful Python functionalities: a multithreaded script for sorting files in a directory and a multiprocessed function for factorizing numbers. The folder sorter speeds up the handling of large directories by using threads, while the factorization function leverages multiple CPU cores for quick calculations.

## Features
- **Multithreaded Folder Sorting**:
  - Sorts files in a specified directory into categories based on file extensions.
  - Utilizes multiple threads to handle nested directories and file operations concurrently.
- **Multiprocessed Factorization**:
  - A function `factorize` that takes a list of numbers and returns their factors.
  - Improved performance through parallel computations using multiple CPU cores.

## Folder Sorting
- Speeds up the processing of large directories with many nested folders.
- Performs file moving operations in separate threads to reduce processing time.
- Each subdirectory is processed in a separate thread, maximizing efficiency.

## Factorization Function
- Synchronously factorizes numbers and measures execution time.
- Enhances performance using the multiprocessing approach.
- Dynamically determines the number of cores using `cpu_count()` for optimal parallelization.

## Usage
1. **Folder Sorting**:
   - Run the script from any location using the command:
     ```
     clean-folder [path_to_directory]
     ```
   - Replace `[path_to_directory]` with the target directory path.

2. **Factorization**:
   - Call the `factorize` function with a list of numbers:
     ```python
     results = factorize([128, 255, 99999, 10651060])
     ```
   - Compare the execution time of synchronous vs. multiprocessed versions.

## Installation
Clone the repository and install the package using either:
- `pip install -e .`
- `python setup.py install`

## Testing
- Ensure the folder sorter correctly categorizes files in various directories.
- Validate the factorization function with provided test cases.
