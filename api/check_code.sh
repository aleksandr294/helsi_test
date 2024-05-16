#!/bin/bash

# Check code with Black

echo "Checking code with Black"
black --check .

# Check code style with Ruff
echo "Checking code style with Ruff..."
ruff check .

# Check type errors with MyPy
echo "Checking type errors with MyPy..."
mypy .

# Run tests
echo Run tests
python manage.py test
