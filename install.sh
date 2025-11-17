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
    postgresql-contrib \
    build-essential \
    python3-dev

# Install SDL and multimedia libraries for pygame
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

# Install pygame using apt (Debian package manager)
echo "Installing pygame..."
apt-get install -y python3-pygame

# Start PostgreSQL service
echo "Starting PostgreSQL service..."
systemctl start postgresql
systemctl enable postgresql

echo ""
echo "==== Installation Complete ====" 
echo ""
echo "To run the application:"
echo "1. Start backend (in one terminal):   python3 -m backend.server"
echo "2. Start frontend (in another terminal): python3 main.py"
echo ""
