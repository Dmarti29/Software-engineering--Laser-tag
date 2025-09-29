#!/bin/bash

# Photon Laser Tag System Installation Script

echo "==== Installing Photon Laser Tag System ===="
echo "Creating Python virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Ask if user wants to set up the database
echo ""
echo "Do you want to set up the PostgreSQL database now? (y/n)"
read -r setup_db

if [ "$setup_db" = "y" ] || [ "$setup_db" = "Y" ]; then
    # Check if setup_db.sh exists and is executable
    if [ -f "./setup_db.sh" ] && [ -x "./setup_db.sh" ]; then
        echo "Setting up PostgreSQL database..."
        ./setup_db.sh
    else
        echo "setup_db.sh not found or not executable."
        echo "Please make sure setup_db.sh exists and is executable with: chmod +x setup_db.sh"
    fi
fi

echo ""
echo "==== Installation Complete ====" 
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment:   source .venv/bin/activate"
echo "2. Start the application:              python main.py"
echo ""
