#!/bin/bash

# Photon Laser Tag System Installation Script

echo "==== Installing Photon Laser Tag System ===="

# Check for root/sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y \
    python3 \
    python3-tk \
    python3-pil \
    python3-pil.imagetk \
    python3-flask \
    python3-psycopg2 \
    python3-flask-cors \
    python3-requests \
    postgresql \
    postgresql-contrib

# Start PostgreSQL service
echo "Starting PostgreSQL service..."
systemctl start postgresql
systemctl enable postgresql

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

echo ""
echo "==== Installation Complete ====" 
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment:   source .venv/bin/activate"
echo "2. Start the application:              python main.py"
echo ""
