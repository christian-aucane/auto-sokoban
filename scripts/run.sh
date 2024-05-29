#!/bin/bash

# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    # Check if we are on Windows
    if [[ "$OS" == "Windows_NT" ]]; then
        # Activate virtual environment for Windows
        source venv/Scripts/activate
        # Run the application with python
        python src/main.py
    else
        # Activate virtual environment for Unix-based systems (Linux, macOS)
        source venv/bin/activate
        # Run the application with python3
        python3 src/main.py
    fi
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi
