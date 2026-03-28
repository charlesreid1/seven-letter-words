#!/bin/bash
set -e

mkdir -p output

# Run all .py files in the current directory
for script in *.py; do
    # Remove the .py extension for the output filename
    base="${script%.py}"
    echo "Running ${script} ..."
    vpp/bin/python "${script}" > "output/${base}.txt" 2>&1
done

echo "Done. Output files in output/"
