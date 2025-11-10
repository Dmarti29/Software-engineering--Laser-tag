#!/bin/bash
set -e

# Photon Laser Tag System Installation Script
echo "==== Installing Photon Laser Tag System ===="

# Ensure we're in the script's directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

# Check for root/sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

# Install core system dependencies
echo "Installing base system dependencies..."
apt-get update
apt-get install -y \
    python3 \
    python3-venv \
    python3-tk \
    python3-pil \
    postgresql \
    postgresql-contrib \
    build-essential \
    python3-dev

# --- SDL and multimedia libraries for pygame ---
echo "Installing SDL and multimedia dependencies for pygame..."
apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libx11-dev \
    libxext-dev \
    libxrandr-dev

# Start PostgreSQL
echo "Starting PostgreSQL service..."
systemctl start postgresql
systemctl enable postgresql

# Optional: Create database and user
echo "Setting up PostgreSQL user and database (if not existing)..."
sudo -u postgres psql <<EOF
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'photon_user') THEN
      CREATE USER photon_user WITH PASSWORD 'photon_pass';
   END IF;
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'photon_db') THEN
      CREATE DATABASE photon_db OWNER photon_user;
   END IF;
END
\$\$;
EOF

# Virtual environment setup
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

source .venv/bin/activate

# Upgrade pip and install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# --- Test pygame installation ---
echo "Testing pygame installation..."
python3 - <<'EOF'
try:
    import pygame
    pygame.init()
    print("Pygame initialized successfully ✅")
except Exception as e:
    print("Pygame installation failed ❌")
    print(e)
EOF

echo ""
echo "==== Installation Complete ===="
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment:   source .venv/bin/activate"
echo "2. Start the application:              python main.py"
echo ""