#!/bin/bash

# Get the directory where the script is located
CD_PATH="$(cd "$(dirname "$0")" && pwd)"
cd "$CD_PATH"

echo "========================================"
echo "   Insta360 Date Export Fixer"
echo "========================================"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: python3 is not installed or not in PATH."
    echo "Please visit https://www.python.org/downloads/ to install it."
    read -n 1 -s -r -p "Press any key to exit..."
    exit 1
fi

# Check for exiftool
if ! command -v exiftool &> /dev/null
then
    echo "❌ Error: exiftool is not installed."
    echo "Please install it using 'brew install exiftool' or download from https://exiftool.org/"
    read -n 1 -s -r -p "Press any key to exit..."
    exit 1
fi

echo "Processing files in: $CD_PATH"
echo ""

# Run the python script on the current directory
python3 insta360_date_fixer.py "."

echo ""
echo "========================================"
echo "   Done!"
echo "========================================"
echo ""
read -n 1 -s -r -p "Press any key to close this window..."
