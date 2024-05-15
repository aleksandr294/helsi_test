#!/bin/bash

# Check code with Black

echo "Checking code with Black"
black .

# Check code style with Ruff
echo "Checking code style with Ruff..."
ruff check .

# Check type errors with MyPy
echo "Checking type errors with MyPy..."
mypy .
