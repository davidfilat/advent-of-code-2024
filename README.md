# Advent of Code 2024

This repository contains my solutions for the Advent of Code 2024 coding challenges.

## Project Structure
- 

- `src/`: Contains the main Python scripts for each day's solutions.
- `resources/`: Contains input files for each day's challenge.
- `src/utils/`: Contains utility functions used across multiple days.
- `tests/`: Contains test files (to be implemented).

## Setup

This project uses Python 3.13 and uv for dependency management.

1. Clone the repository:
   ```
   git clone https://github.com/davidfilat/advent-of-code-2024.git
   cd advent-of-code-2024
   ```

2. Set up the virtual environment and install dependencies:
   ```
   make venv
   ```

## Using the Makefile

This project uses a Makefile to simplify common tasks. Here are some useful commands:

- Set up the virtual environment and install dependencies:
  ```
  make venv
  ```

- Run a specific day's solution:
  ```
  make run day=<day_number>
  ```
  For example, to run Day 1's solution: `make run day=1`

- Lint the code:
  ```
  make lint
  ```

- Format the code:
  ```
  make format
  ```

- Clean up the project (remove virtual environment and cache files):
  ```
  make clean
  ```

- See all available commands:
  ```
  make help
  ```

Always use these Makefile commands to run the code and manage the project for consistency.

## Dependencies

Main dependencies are listed in `pyproject.toml`. They include:

- Python 3.13
- cytoolz

Dev dependencies include ruff for linting and formatting.

## Acknowledgements

- [Advent of Code](https://adventofcode.com/) for creating these challenges.
